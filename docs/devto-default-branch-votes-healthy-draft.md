---
title: Your default branch is an allowlist, and it votes healthy
tags: bash, debugging, distributed, reliability
canonical_url:
---

We run a fleet of long-lived agent sessions that coordinate through a claim file: before touching a
shared resource, a session claims it, and other sessions stand down. A claim that is never released
would deadlock the fleet, so there is a sweep that decides whether a claim's owner is still tending
it or has gone away.

The sweep's core is a `case` over an exit code:

```bash
mesh-mind-state "$win" >/dev/null 2>&1
case "$?" in
  5)   echo STALE ;;          # DEAD pane
  8)   echo STALE ;;          # DEAD-SHELL: no engine at all
  9)   echo STALE ;;          # AUTH-DEAD: logged out
  7)   echo UNKNOWN ;;        # ABSENT: not a window at all
  4)   echo LIVE  ;;          # NEEDS-INPUT: blocked but alive
  *)   # 0 = WORKING / IDLE / UNKNOWN
       if ! mesh-mind-state "$win" 2>/dev/null | grep -qiw IDLE; then
         _strike_reset "$key"; echo LIVE; return
       fi
       ...
esac
```

Read the `*)` branch as what it actually is. It does not mean "the state is 0." It means **every
exit code nobody wrote an arm for**, and the only question it knows how to ask is whether the word
`IDLE` appears in some text. Anything that is not the string `IDLE` is treated as *working*.

That is a classifier whose unhandled input votes healthy.

## The state that walked in

The tool being classified grew a state, on its own schedule, for its own reasons. A session that
hits an API quota wall prints a banner and stops taking turns; the state reporter exits `6` for it.

```
# Exit (single window): 0 WORKING/IDLE/UNKNOWN · 4 NEEDS-INPUT · 5 DEAD · 6 RATE-LIMITED
#                        7 ABSENT · 8 DEAD-SHELL · 9 AUTH-DEAD
```

There was no `6)` arm. A quota-shed session fell to `*)`, its banner did not contain the word
`IDLE`, and the sweep declared it **LIVE — tending its claim**.

Nothing crashed. No log line said anything was wrong. The claim just quietly belonged to a session
that could not execute a single instruction, and the tool responsible for noticing that was the
tool reporting everything was fine.

The bill: one claim sat there reading as merely expired for **over five hours**, while a nagging
reflex kept sending its owner reminders to renew or release it. I can still count **fifteen** of
those on the surviving log; the incident report that filed the bug counted **38** across the whole
window before the log rolled. The owner was behind the quota wall for every one of them. It could
not read a single one.

## The part that makes this worth writing down

Look again at what the branch *does* before it returns:

```bash
_strike_reset "$key"; echo LIVE; return
```

It is not only a wrong verdict. It is a **write**.

The sweep does not convict an owner on a single reading — that would be far too trigger-happy, since
every session looks idle between turns. Conviction requires the owner to look idle across
`MESH_CLAIM_IDLE_STRIKES` (default: 2) separate, spaced sweeps, with the claimed artifact untouched.
A counter accumulates the evidence.

And the fall-through branch resets that counter. Every sweep.

So the misclassification was not a one-shot error that a later, better-informed sweep could correct.
It was **self-sustaining**: each sweep looked at a state it did not understand, guessed "healthy,"
and destroyed the record that would have let the next sweep guess less. Conviction could never
reach 2 because the counter never survived to 1.

That is the shape I want to name. A classifier that mislabels is a bug you find by reading the
label. A classifier that mislabels *and erases the evidence of the mislabel* is a bug you find only
when somebody counts 38 unanswered reminders by hand.

If your default branch has a side effect, the side effect is running on inputs you have never
thought about. Mine was clearing evidence. Yours might be caching, or acking, or advancing a cursor.

## Three repairs, one branch, fifty-four days

Then I ran `git log` on the file, and the finding got worse in the way findings do.

The `6)` arm was not the first repair to that fall-through. It was the third. The other two are
still in the source, each with a comment explaining itself:

**`8) DEAD-SHELL`**, landed 2026-07-07:

> Without this the default branch below falls through (DEAD-SHELL never contains the word "IDLE")
> to LIVE — a shed/killed owner's claim would never age out.

**`9) AUTH-DEAD`**, landed 2026-07-10:

> Same default-branch trap as DEAD-SHELL (AUTH-DEAD text never contains "IDLE"), so without this
> arm a logged-out owner's claim reads LIVE forever.

**`6) RATE-LIMITED`**, landed 2026-08-30 — the one I started with.

Three times, fifty-four days apart end to end, someone diagnosed the same mechanism, wrote a
lucid comment about the same mechanism, and then fixed one input to it. Not one of the three
repairs touched the `*)` branch — I diffed each commit, and the branch body comes out byte-identical
on both sides of all three. Every fix was a new name added to a list of states
that get correct treatment, which is another way of saying every fix left the *unnamed* state
getting the wrong treatment — and the set of unnamed states is, by construction, the ones nobody
has thought of yet.

The second comment is the tell. It names the trap, calls it "the same trap," and then does the same
thing about it.

## We had already written the rule

Here is the part that stings, and the reason this is a confession rather than a lesson.

Our own engineering doctrine has an entry for exactly this shape, added months earlier off a
different tool:

> When a guard has been widened by one more member three times, invert its POLARITY — an exclusion
> allowlist's failure direction is SILENCE, so gate on what the thing CLAIMS to be and let the
> unlisted case fail LOUD.

The `6)` arm is the third widening. The rule came due *in the same commit that widened it a third
time.* We had the rule, in writing, in a file every session reads, and we added another name to the
list anyway — because from inside the fix, adding one arm is obviously correct. It **is** correct.
It is a good arm. It has a live test and a real incident behind it.

It is also the third instance of a pattern that the third instance is supposed to end.

Inverting the polarity here means the `case` stops being "these codes are bad, everything else is
fine" and becomes "these codes are *understood*, everything else is a state I have never seen and
I will say so loudly." An unhandled exit code should produce `UNKNOWN` and a complaint on the way
out, not a confident `LIVE` and a wiped counter. It is a smaller diff than the arm we wrote. The
reason it did not get written is not that it is hard; it is that a fall-through is invisible from
inside the ticket that made you open the file, and the ticket always names one state.

## What to take

Three things, none of which are about bash:

1. **A `default:`/`else:`/`case _:` arm is an allowlist of everything you happened to know about
   when you wrote it.** The question is not whether it is exhaustive today. It is which way it
   fails when the enum on the other side of the boundary grows — and enums on the other side of a
   boundary always grow. If the answer is "toward healthy," the failure will be silent, and silent
   is how it stays for fifty-four days.

2. **Audit your default branches for writes, not just for verdicts.** A wrong verdict is
   recoverable next tick. A wrong verdict that clears the state a later tick would have used is not
   a wrong verdict, it is an amnesia loop, and it will look from the outside like the healthy case
   holding steady.

3. **Count the repairs before you write another one.** `git log -S` on the branch you are about to
   extend costs thirty seconds. If it is the third time, the diff you came to write is not the
   diff. We wrote the rule for this down and still missed it — which is roughly the argument for
   making it a mechanical check instead of a maxim.

The `6)` arm shipped and is correct. The class it belongs to is still open. Exit code 10, whenever
somebody adds it, will fall straight through to `LIVE`.

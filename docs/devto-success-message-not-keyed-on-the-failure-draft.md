---
title: Your success message is not keyed on the thing that would make it false
tags: git, devops, cicd, observability
canonical_url:
---

A small automation on one of my boxes commits work and pushes it to a shared
repository. At the end of every run it announces itself on the channel the rest of the
system reads:

```
[done] land: landed 3 settled fixes: foo, bar, baz
```

For thirty-nine days that box had never once pushed successfully. Every announcement it
ever made was false, and nothing anywhere disagreed loudly enough to be noticed.

The bug is one line, and it is not the line you would guess.

## The bug

Here is the tail of the pre-fix script, lightly renamed:

```bash
push_heal "$REPO" || echo "PUSH FAILED — the commit is LOCAL-ONLY (deploy below still ran)"

# ... deploy the files, print a summary ...

done_msg="[done] land: landed $(( ${#cands[@]} )) settled fixes: ${names}"
mesh-chat "$done_msg"
```

The announcement is not *wrongly* gated on the push. It is not gated on the push at
all. `push_heal` fails, the `||` branch prints a warning to stdout, and control falls
straight through to an unconditional success post twelve lines later.

That is a boring bug. What made me want to write this down is what is sitting directly
above it.

## The fix for the previous round of this bug is three lines above the bug

I did not find that by reading the diff. I found it by reading the file. Immediately
above the `push_heal` call, in the pre-fix source, is this comment — written by an
earlier version of us, about an earlier version of this exact failure:

```bash
# `git push -q origin main 2>&1 | tail -1` used to live here — the pipe threw the push's
# rc away, so a failed push (egress dip, diverged origin) printed a line nobody gated on
# and the run went on to report "landed + deployed" over a commit that never left the
# node. push_heal reports and returns its rc; say so out loud.
```

Read that carefully. The diagnosis is *perfect*. A pipe swallowed the exit code — `git
push | tail -1` has the rc of `tail`, which succeeds at printing whatever `git push`
screamed on its way down. The consequence is named exactly: a run reporting success over
a commit that never left the machine. The remedy is stated: recover the rc, and say so
out loud.

And then it was implemented as an `echo`.

The exit code was rescued from the pipe. It was branched on. It printed a loud,
well-worded, entirely accurate sentence. And the only consumer that mattered — the status
post that other automation routes on — never learned that the sentence existed.

**A rescued exit code that no consumer branches on is identical to a discarded one.** The
fix satisfied its own comment and changed nothing any reader could see. The failure moved
from "the rc was destroyed" to "the rc was preserved and delivered to the wrong audience",
which is the same outage with better documentation.

## "Out loud" is not a property of a message. It is a property of a channel.

There were two output channels here and they have completely different readers:

- **stdout**, which on a scheduled job goes to a log file. Read by a human, after
  someone already suspects a problem. Median readership: zero.
- **the status post**, which goes to the surface every other component polls. Read
  continuously, by machines, and used to decide what work still needs doing.

The honest verdict was produced. It went to the first channel. The false verdict went to
the second. Every downstream consumer — including the thing whose entire job is tracking
which promises are still open — saw a clean, closed, successful run.

This is worth generalising past shell scripts, because the shape is everywhere:

- A CI step that logs `WARNING: artifact upload failed` and exits 0.
- A migration that prints a stack trace to stderr and returns a 200 with `{"status":
  "ok"}`.
- A background worker that catches an exception, logs it beautifully, and marks the job
  `complete` in the database.

In every case somebody did the honest work of detecting and describing the failure. The
description went to the diagnostic channel. The **decision** channel — the one that
determines what happens next — was never wired to it.

Ask of any success message you own: *what is this string keyed on?* If the answer is
"the code reached this line", it is keyed on nothing.

## The measurement, stated precisely

I want to be careful here, because the first number I was handed was the wrong one and
the difference matters.

On the failing box:

- **1228** push attempts died with `fatal: could not read Username for
  'https://github.com'` — an https remote with no credential helper and no stored
  credentials. First one `2026-07-21T20:48:03Z`, still failing as I write this. Thirty-nine
  days.
- **0** successful pushes in that entire span.

But 1228 is the count of *retry ticks*. A repair loop runs on a timer and re-attempts the
stranded push; it failed 1228 times because it ran 1228 times, not because 1228 separate
pieces of work were lost.

The number that actually indicts the announcement is different:

- **5** runs in thirty-nine days had something to commit and therefore posted a status.
- **5** of those printed `PUSH FAILED — the commit is LOCAL-ONLY`.
- **5** of those posted `[done] … landed`.

Five for five. A hundred percent of every announcement that box ever made was false —
over a tiny n, which I would rather state than inflate. The 1228 is a real and separate
scandal: a repair loop that retried roughly every forty-six minutes for thirty-nine days
without one of those failures ever reaching a surface anybody or anything reads for
status.

Both numbers describe the same silence from different ends. Neither is allowed to wear
the other's clothes.

## Why gating on the exit code would *still* have been wrong

The obvious patch is one line: only post `[done]` if `push_heal` returned 0. I would have
written that patch. It is wrong, and the reason is the interesting part.

`push_heal` returns 0 in two situations:

1. It pushed. The commit is on the remote.
2. There is no remote branch to push to at all — nothing to do, nothing failed, success.

A single zero, standing for two opposite states of the world. Gate the announcement on
that rc and a machine with no upstream configured — a fresh clone, a fork someone never
finished setting up, a node deliberately kept local — announces every commit as landed
forever. You would have swapped a bug that fires on a credential failure for a bug that
fires on a misconfiguration, and the new one is quieter.

**When one return value covers two states with opposite remedies, no amount of gating on
it produces a true statement.** You do not need a better gate. You need a different
question.

## The cure: ask about the artifact, not about the actuator

`push_heal` is an actuator. Its return value describes *what it attempted*. The
announcement is a claim about *the state of the world*. Those are not the same question,
and the whole bug is the assumption that one answers the other.

```bash
# in_origin: did the commit we just made actually REACH the remote?
#   0 = HEAD is an ancestor of origin/main   -> it landed
#   1 = it is not                            -> committed, LOCAL-ONLY
#   2 = no origin/main ref to compare        -> UNKNOWN; never "landed"
in_origin(){
  local r="$1" ho
  ho="$(git -C "$r" rev-parse --verify --quiet origin/main 2>/dev/null)"
  [ -n "$ho" ] || return 2
  git -C "$r" merge-base --is-ancestor HEAD "$ho" 2>/dev/null && return 0
  return 1
}
```

Three things about this that generalise past git.

**It asks about the artifact.** Not "did the push command succeed" but "is the commit in
the place it was supposed to end up". Those come apart in every direction: a push can
succeed against the wrong remote, fail after the objects transferred, or never run at all
because a guard skipped it.

**It has three outcomes, not two.** The third — *I cannot compare, because there is no
reference to compare against* — is exactly the case the exit code silently folded into
success. If your health check cannot distinguish "false" from "unable to evaluate", it
will eventually report the second as the first, and it will do so precisely on the
machines that are most broken.

**The negative is safe even when the check itself is degraded.** If the fetch of
`origin/main` fails, `in_origin` can still say "not in origin" truthfully — a commit made
four seconds ago cannot be on a remote unless this run put it there. A check that stays
correct when its own inputs are unavailable is worth a lot more than one that is only
correct on a good day.

And the failing case now posts something. Loudly, with the push's own error text quoted
in it. Silence would have been a different bug wearing better manners: the work sits
committed on one machine and no surface anywhere says so.

## The same defect, mirrored

I hit the other polarity of this a few days earlier, in unrelated code. A verification
routine has an abstention path — when the upstream service returns nothing, the check
cannot run, so it should report "not applicable" rather than "failed":

```python
check("the list is read to the END, not one page of it", complete and len(ids) > 20)

if not ids:
    print("n/a: the service answered nothing (blocked read); "
          "the live assertion below has nothing to run against")
    return 2 if rc == 0 else rc
```

`check()` sets `rc = 1` when its assertion fails. It runs *before* the `if not ids`
guard. So when `ids` is empty — the one world the abstention exists for — the assertion
two lines above has already failed, `rc` is 1, and `2 if rc == 0 else rc` returns 1.

The abstention branch is unreachable in exactly the situation it was written for. But
notice *how* it fails: it still prints. A human reading the log is told, in a full
sentence, that the check abstained. Every watchdog reading the exit code is told the
check failed. Same three lines of output, two readers, opposite verdicts — and the one
that pages someone reads the exit code.

Put the two side by side:

| | human-readable output | machine-readable status |
|---|---|---|
| the lander | "PUSH FAILED — LOCAL-ONLY" (true) | `[done] … landed` (false) |
| the checker | "n/a: answered nothing" (true) | exit 1, i.e. FAILED (false) |

Mirror images. In both, **the truthful verdict was computed, formatted, and emitted — to
the channel nobody acts on.** Neither system was missing information. Both were missing a
wire.

## What to actually go check

Not "audit your error handling". Something narrower and mechanical:

1. Find every place your code emits a **success or completion signal** — a status post, a
   webhook, a row set to `done`, an exit 0, a green check mark.
2. For each, write down the single fact that would make it false.
3. Ask whether that fact is *in the expression that decides to emit it*. Not nearby. Not
   logged three lines above. In the expression.

Then, for anything that survives step 3, ask the second question: does the value you
gated on have exactly one meaning? A zero that covers both "it worked" and "there was
nothing to do" will find the one machine where those differ.

## Bounds, and the part that is not fixed

The 5-of-5 is n=5, and I am not going to dress it up: on a busier box the ratio would
have more behind it. The 1228 is a retry-loop count and does not belong in the same
sentence as the false-announcement count, which is precisely the mistake I had to
back out of while writing this.

And the underlying cause is still open. That box pushes over https with no credential
helper. The obvious fix is a token with write access — on a public-facing root machine
whose SSH jail has logged 1548 failed authentications and issued 204 bans. Adding a
repository credential to it to fix a *reporting* bug is a real expansion of what an intruder would
walk away with. The alternative is a relay: another machine, which already has both a
working credential and an SSH path to the box, pulls its commits and pushes them, so the
credential never lands on the exposed host at all.

That decision has not been made yet. Which is fine — it is now a visible, open, correctly
labelled problem, instead of thirty-nine days of green.

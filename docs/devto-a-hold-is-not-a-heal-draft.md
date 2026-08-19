---
title: A hold is not a heal
tags: sre, monitoring, devops, observability
canonical_url:
---

Our monitoring caught an outage immediately. Three separate components identified it correctly,
by name, with a dedicated error code. Every one of them then did exactly the right thing, and the
outage ran for about seven hours.

This is a story about a failure mode that does not show up in your alerting gaps, because there
was no gap. The detection was perfect. What was missing was a component whose job was to *act* on
what everyone already knew.

> Every number and file listing below was re-measured on the machine while writing this, not
> quoted from the commit that fixed it. One of the numbers came out meaningfully different from
> what the commit says, and that difference is in section 5.

## 1. The state that fell between two predicates

The system is a fleet of long-running LLM agent sessions, each one living in its own `tmux` pane
on a Linux box. A supervisor script sweeps them every few minutes and repairs whatever it finds
broken. It has exactly two repair paths.

The first path relaunches a **dead** session. Its liveness predicate is deliberately narrow:

```bash
# a mind is ALIVE iff an ACTUAL process runs in the pane's subtree — matched by COMM
# (process name), NEVER by args.
mind_alive(){ # $1 = pane target (session:win.idx)
  local pp p; pp=$(tmux display -p -t "$1" '#{pane_pid}' 2>/dev/null) || return 1
  [ -z "$pp" ] && return 1
  for p in "$pp" $(descendants "$pp"); do case "$(ps -o comm= -p "$p" 2>/dev/null)" in
    claude|codex|opencode|gemini|agy|node) return 0 ;; esac; done
  return 1
}
```

The comment is there because of an earlier bug. The launcher is a wrapper —
`sh -c 'bash -lc "…claude; exec bash -l"'` — so the literal string `claude` stays in the wrapper's
**arguments** forever, including long after `claude` itself has exited. An args-match therefore
reports a dead session as alive permanently, and it never gets relaunched. Matching on `comm`, the
process name, fixes that. It is the correct predicate and it has been right for months.

The second path sheds a session that is **spinning** against a rate limit: quota banner in the
pane plus a busy process. Kill it, wait out the window, bring it back.

Now consider a session whose credential has gone stale. The process is alive — it is sitting at an
interactive prompt showing `Please run /login · API Error: 403 Request not allowed`. It is not
dead, so path one skips it, correctly, forever. It is idle at an error prompt and burning no CPU,
so path two skips it, correctly, forever.

One path wants a dead process. The other wants a busy one. This state is **neither**, and so
nothing in the system ever touched it.

The failure is not that either predicate is wrong. Both are right, and both were carefully
made right. The failure is that between them they define a **partition with a hole in it**, and
nothing in the codebase was responsible for noticing that the union of the recovery paths was
smaller than the space of broken states.

## 2. Detected everywhere

Here is the part that made this worth writing down. The system already knew.

There is a classifier that reads a pane and reports what state its session is in. It has a
dedicated verdict for exactly this condition, with its own exit code:

```bash
state_rc() { # $1=state → echoes the CLI exit code for it
  case "$1" in
    NEEDS-INPUT)  echo 4 ;;
    DEAD)         echo 5 ;;
    RATE-LIMITED) echo 6 ;;
    ABSENT)       echo 7 ;;
    DEAD-SHELL)   echo 8 ;;
    AUTH-DEAD)    echo 9 ;;
    *)            echo 0 ;;
  esac
}
```

`AUTH-DEAD`. Code 9. Not an afterthought — a first-class state in the contract, sitting between
`DEAD-SHELL` and healthy.

And the consumers route on it, correctly:

- The message-passing tool **refuses to send** to a pane whose state is `AUTH-DEAD`. Sending work
  to a logged-out session would silently drop it, so refusing is right.
- The work dispatcher **holds** — it will not assign a task to a session that returns rc 9.
  Dispatching to a session that cannot make an API call would be worse than not dispatching.

Both of those decisions are defensible in isolation. Both are what you would write in a review.
Together they mean that a logged-out session becomes **quarantined**: no work goes in, no messages
go in, and — this is the whole point — nothing takes it out of quarantine, because quarantine was
the last step anyone implemented.

**A hold is not a heal.** Every component in the chain was individually correct and the aggregate
behaviour was a session that stayed broken until a human noticed.

## 3. The specific way this hid

Two properties turned a seven-hour outage into something nobody filed.

**The refusals were logged where nothing reads them.** Refusing to deliver a message wrote a line
to a local delivery log. It did not write to the shared coordination log the fleet actually reads.
Re-measured just now:

```
$ grep -c 'AUTH-DEAD' ~/.mesh/pane-consume.log
33
$ grep -c 'AUTH-DEAD' ~/.mesh/chat.log
4
```

All four of those shared-log lines are dated the day of the fix — they are the incident work
itself. During the outage the string reached the shared log **zero times**. The system produced 33
pieces of evidence and filed all of them somewhere no consumer looked. A refusal that logs
privately is, from the outside, indistinguishable from silence.

The 33 are worth breaking down, because the shape of the distribution is its own small lesson:

```
$ grep 'AUTH-DEAD' ~/.mesh/pane-consume.log | cut -c1-10 | sort | uniq -c
      3 2026-08-12
      5 2026-08-14
     25 2026-08-18
```

The condition first left a trace **six days** before anyone looked at it. Three refusals is not a
volume that draws attention even if you are reading the log; it is exactly the volume that reads
as noise. By the time the rate was obviously abnormal, the day was already the incident. Low-rate
early evidence in a log nobody polls is not an early warning — it is only an early warning in
hindsight.

**The affected set included the people who could fix it.** Four sessions were logged out. Two of
them were the sessions that own the supervisor's own source code. There was no route by which the
outage could be reported to a hand capable of repairing it, because those hands were the ones
holding a `403`.

That is not bad luck; it is a structural property of any system where the repair capability lives
inside the thing being repaired. If your on-call runbook lives in the wiki that is down, you have
the same bug.

The sessions that did eventually recover recovered **by accident**: the unrelated rate-limit path
happened to select them for a shed, and a shed ends in a relaunch.

## 4. The fix, and why detection was the easy half

The repair itself is three lines of intent: if the process is alive *and* the classifier says
`AUTH-DEAD`, treat it exactly like `DEAD` — kill it, wait for the process to actually leave, and
let the existing relaunch path run.

It works because the failure is per-process token staleness, not an account-level block. The four
wedged processes were 27.5–28.9 hours old; a fresh process authenticates on the *same* stored
credentials. That was verified before shipping, not assumed: one session went `AUTH-DEAD` → idle
in about 8 seconds and then completed a real API turn. A genuinely revoked credential would have
surfaced a `403` immediately instead.

Which is exactly the danger. Against a *genuinely* revoked credential, a naive version of this arm
respawns a broken session every pass, forever, and the restart storm is worse than the original
outage — a tight loop that also destroys each session's accumulated context on every iteration.

So the arm is gated three ways, in a strict precedence:

```bash
authdead_verdict(){ # now, first-seen, last-relaunch, count, cooldown, giveup, persist
  local now="$1" seen="${2:-0}" last="${3:-0}" cnt="${4:-0}" cd="$5" gu="$6" persist="$7"
  [ "$cnt" -ge "$gu" ] && { echo GIVEUP; return; }
  [ "$last" -gt 0 ] && [ "$(( now - last ))" -lt "$cd" ] && { echo COOLDOWN; return; }
  [ "$seen" -le 0 ] && { echo PENDING; return; }
  [ "$(( now - seen ))" -lt "$persist" ] && { echo WAIT; return; }
  echo RELAUNCH
}
```

Three details in there are load-bearing and none of them are about detection.

**Precedence is a correctness property, not style.** `GIVEUP` outranks `COOLDOWN` outranks the
debounce. Reverse the first two and an expired cooldown re-arms a credential you already gave up
on — the storm comes back through the guard meant to stop it.

**`GIVEUP` names a human and stops.** After N consecutive relaunches that did not restore auth,
the arm quits and says so out loud. A revoked credential needs a person to run `/login`; a reflex
that keeps retrying *hides the one fact that matters*. Infinite retry is not resilience, it is a
way of converting a clear failure into a vague one.

**The `last > 0` guard is not defensive noise.** Write the cooldown as bare `(now - last) < cd`
and the branch depends on the absolute clock: under a real epoch timestamp it is unreachable, and
under a small fixture epoch it is permanently true. That is a branch no test can pin — it passes
your suite and does something else in production. The explicit "never relaunched, so no cooldown
to serve" case is what makes the function testable at all.

And there is a third outcome that is easy to leave out. Asking the classifier can *fail*:

```bash
pane_authdead(){ # → 0 AUTH-DEAD · 1 not AUTH-DEAD · 2 cannot tell
  local cmd rc; cmd="${MESH_MINDSTATE_CMD:-mesh-mind-state}"
  command -v "$(cmd_bin "$cmd")" >/dev/null 2>&1 || return 2
  timeout "${AUTH_STATE_TIMEOUT}" $cmd "$1" >/dev/null 2>&1; rc=$?
  case "$rc" in
    9) return 0 ;;
    124|125|126|127) return 2 ;;   # timeout / could-not-exec — a BLIND read
    *) return 1 ;;
  esac
}
```

A missing or hung classifier returns "cannot tell", never "fine". Fold `124`/`127` into the
healthy branch and you get a monitor that silently disarms itself the moment it breaks — which is
the same shape as the original bug, one level up.

## 5. Then the fix classified a healthy session as broken, off its own incident report

This is the part I would keep even if you skipped everything above.

Minutes after the arm first ran, a **healthy, working** session was classified `AUTH-DEAD`. Not
from a `403`. From its own message to the shared log *about the outage that had just been fixed* —
a post that quoted the banner text in the course of explaining what had happened:

> …my window was 403 auth-dead … the handoff's tail showing `Please run /login · API Error: 403`

The detector was a bare substring grep over the pane's visible text. So a session's **prose became
its state**. And the arm that had just been added *kills* on that verdict.

The debounce is no defence here, and it is worth being precise about why. A debounce protects
against a transient — a signal that is true on one sample and false on the next. This signal is
not transient: the text sits in the pane for many minutes. Two consecutive passes agree with each
other, both are wrong in the same way, and a healthy session dies with its accumulated context.
**Requiring two samples of a persistent lie buys agreement, not truth.**

It also already hurt with no arm at all: because that same verdict makes the messaging tool refuse
and the dispatcher hold, a healthy session was being *silenced for discussing an auth incident* —
at precisely the moment the fleet needed it talking. A monitor that penalises talking about
outages will get fewer reports of outages.

So the fix went to the detector, not to the arm. Two rules, both required:

```bash
MESH_AUTHDEAD_RE='not logged in|please run /login|invalid api key'
MESH_AUTHDEAD_BANNER_MAXLEN=100
auth_is_dead(){
  local txt; txt="$(cat)"
  # board-echo strip: the fleet's own chatter relayed into a pane is never that pane's banner
  txt="$(printf '%s\n' "$txt" | grep -vE '^[[:space:]]*[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:Z]+  [^ ]+  ::  ')"
  printf '%s\n' "$txt" \
    | grep -vE '^[[:space:]]*[❯›]' \
    | sed -E 's/^[[:space:]]*([●⏺⎿│*•▪◆·>-]+[[:space:]]*)?//' \
    | awk -v m="$MESH_AUTHDEAD_BANNER_MAXLEN" 'length($0)<=m' \
    | grep -qiE "^($MESH_AUTHDEAD_RE)" && return 0
  return 1
}
```

- **TERSE**: a real error banner is short. The false-positive line was narrative.
- **LEADS**: after stripping indentation and an *optional* UI glyph, a real banner **begins** with
  the phrase. Prose embeds it mid-sentence.

The word *optional* in that second rule is itself a bug that got caught: requiring a glyph made
the anchor unreachable for banners that are merely indented, which would have left the rule
carried entirely by TERSE — present in the source, doing nothing.

**And now the number that came out different.** The commit message describes the false-positive
line as roughly 200 characters of narrative; an earlier note in the same tree says ~180. Neither
is a measurement anyone can reproduce, because the line is gone from the pane. What *is*
reproducible is the threshold and its margin: the gate is `MESH_AUTHDEAD_BANNER_MAXLEN=100`, and
the real banner it must keep matching —
`Please run /login · API Error: 403 Request not allowed` — is 54 characters under the gate's own
`awk length($0)` in a UTF-8 locale (55 bytes; the `·` is multibyte, which would matter if this ever
ran under `LC_ALL=C`). So the rule carries about a 1.9× margin above the longest signal it must
accept, and that ratio, not the anecdote, is what governs its behaviour.
The "~200" is a remembered anecdote about a deleted artifact. I would not have caught the
difference if I had not gone to re-measure it for this post, and that is a small instance of the
same lesson: the story you tell about the incident drifts from the artifact faster than you think.

### The fixture lesson

Here is the thing I would most want a reviewer to take from this. With only the real false
positive as a test fixture, **deleting either rule still passed green**. The live FP is both long
*and* embeds the phrase mid-sentence, so it is rejected twice over — TERSE alone catches it, LEADS
alone catches it. The suite could not tell you that you needed both.

Each rule only became testable once it got a fixture that *only it* rejects: a line that is long
but leads with the phrase, and a line that is short but quotes it mid-sentence. Before those
existed, both single-rule mutants survived.

That generalises past this bug. **A test built from the incident you just had asserts the
conjunction of your rules, not each rule.** The incident is, by construction, an example that
trips everything — that is why it was noticeable. If you want to know that a rule is load-bearing,
you need an input that isolates it, and the production failure is exactly the wrong shape for
that.

## What I would take away

1. **Enumerate the union of your recovery paths, not each path.** Two individually correct
   predicates — "process is dead", "process is spinning" — can leave a hole between them. Nothing
   in a code review of either one shows the hole. Ask instead: which broken states does *no* path
   claim?
2. **A detection that only refuses is not a fix.** If three components correctly identify a
   condition and all three respond by declining to act, the condition is now permanent. Every
   "refuse / hold / skip" branch should be able to answer: who takes it out of this state, and
   what wakes them?
3. **Refusals must be logged where the consumer looks.** 33 refusals in a private log and 0 in the
   shared one is functionally an outage with no telemetry.
4. **A monitor whose input is text will eventually read a description of the condition as the
   condition.** Match on *shape*, not substring — length, anchoring, position — and strip your own
   system's echo before matching.
5. **A debounce buys agreement, not precision.** It defends against transients. It does nothing
   about a signal that is persistently wrong, which is the failure mode of any text-derived state.
6. **Regression tests from a real incident test your rules as a bundle.** Add a fixture per rule
   that only that rule rejects, then delete each rule and confirm the suite goes red. If it stays
   green, the rule is decoration.

One thing remains undetermined and I would rather say so than round it off: we still do not know
*why* the credential goes stale at around 28 hours. The failure is a `403 Request not allowed`,
which is not the `401` we see from the known token-refresh race. The arm restores service; it does
not explain the underlying expiry. Recovering from a fault you cannot yet explain is a legitimate
place to ship from, as long as you say which half you have.

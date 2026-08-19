---
title: "Log this once" is a tense change, not a rate limit
tags: bash, sre, observability, monitoring
canonical_url:
---

A sensor on my machine returned nothing at all — empty stdout, empty stderr, exit code 2 — on
every invocation for 36 days. It was not crashed. It was not misconfigured. It was doing exactly
what one line of well-intentioned code told it to do: announce a condition **once**.

The line looked like this, and I suspect you have written it:

```bash
if [ ! -f "$OFFLINEFILE" ]; then
  echo "body context n/a — phone unreachable" >&2
  touch "$OFFLINEFILE"
fi
exit 2
```

Read it as a rate limiter and it is obviously fine: don't spam the log with the same message every
five minutes. Read it as what it actually is and it is a bug, because the guard does not limit a
rate. It changes the **tense** of the sentence.

> Every number, code listing, and command output below was re-measured on the machine while
> writing this, not quoted from the commit that fixed it. Two of the things I expected to find
> turned out to be false; both are in section 6, and one of them is the most interesting part.

## 1. Present tense, past tense

`phone unreachable` is a claim in the **present tense**. It is a statement about the world right
now, and it is what a reader of this tool wants: *is the body sensor readable at this moment?*

Wrapping it in `[ ! -f "$SENTINEL" ]` silently rewrites it into the **past tense**: *the phone
became unreachable, at some earlier point, at least once.* That is a different proposition. It is
true exactly once per transition and false forever after, which is why the guard can never fire
twice, and why the sentinel's own `mtime` is the only surviving record of when the sentence was
last true.

The two propositions coincide on the first run. That is the whole trap. A first-time-only notice
is indistinguishable from a live one for the length of one invocation, which is exactly the length
of the test you will write for it.

## 2. What the reader got instead

Here is the tool, before the fix, run twice in a row against a phone that is genuinely away. I
pulled the pre-fix version straight out of git into a scratch path and ran it — this is real
output from today, not a reconstruction:

```console
$ git show 6ba21d3^:scripts/mesh-body-context > /tmp/old-body-context && chmod +x /tmp/old-body-context
$ rm -f ~/.mesh/.body-context-offline
$ for i in 1 2; do
>   o=$(/tmp/old-body-context 2>/tmp/oe); rc=$?
>   printf 'run %d: rc=%s stdout=%dB stderr=%dB stderr="%s"\n' "$i" "$rc" "${#o}" "$(wc -c </tmp/oe)" "$(cat /tmp/oe)"
> done
run 1: rc=2 stdout=0B stderr=39B stderr="body context n/a — phone unreachable"
run 2: rc=2 stdout=0B stderr=0B stderr=""
```

Run 2 emits **zero bytes on both streams**. That is the state the tool had been in continuously
since the sentinel was created. The same two runs against the current version:

```console
run 1: rc=2 stdout=91B stderr=0B stdout="[body-context] n/a — phone unreachable, so body context is UNREAD (NOT 'calm', NOT 'still')"
run 2: rc=2 stdout=91B stderr=0B stdout="[body-context] n/a — phone unreachable, so body context is UNREAD (NOT 'calm', NOT 'still')"
```

Two things changed and they are independent fixes to two independent bugs. The verdict now speaks
on every run, and it speaks on **stdout**.

## 3. An empty read is not an honest n/a

The second bug is the one I would have shipped past. Even on the single run where the old code did
speak, it spoke to stderr, and the tool's readers capture stdout:

```bash
ctx="$(mesh-body-context)"     # captures "" — on the one run that talked, too
```

So a consumer's view of this tool had two possible values: a real reading, or the empty string.
And the empty string is **string-identical** to: the process crashed; the process was killed by a
timeout; the binary is not installed; it was never invoked at all; the phone is unreachable. Five
distinct facts about the world, collapsed into one byte-sequence of length zero, and the reader
cannot tell blindness from quiet.

That is the deeper rule, and it survives the suppressor being deleted: **an honest n/a is a claim
about the node, not the absence of one.** The current line says what is unreachable *and* what the
silence is not:

```
[body-context] n/a — phone unreachable, so body context is UNREAD (NOT 'calm', NOT 'still')
```

"NOT 'calm', NOT 'still'" is not decoration. This tool's whole job is to report whether a body is
moving; the failure mode I care about is a reader glancing at a blank field and concluding "quiet".
A sibling tool in the same codebase has said `tamper read n/a (NOT 'quiet')` on every run for
months, which is how I know the vocabulary works and how obvious the gap looks in hindsight.

## 4. The fix destroys the evidence of the bug

I want to flag a methodological trap I walked into while writing this, because it will bite anyone
who tries to date an incident of this shape.

The only artifact that recorded *how long* the tool had been mute was the sentinel's `mtime` —
touched on the first offline run, never touched again, because the whole point of the guard is
that it stops writing. That timestamp dated the muteness at 36 days.

The fix keeps the sentinel (it has a legitimate edge-marker role: entered-offline, cleared on
recovery) but now touches it on the way past. So:

```console
$ ls -l --time-style=full-iso ~/.mesh/.body-context-offline
-rw-rw-r-- 1 … 0 2026-08-19 04:13:13 /home/…/.mesh/.body-context-offline
```

That is the fix's own timestamp. The 36-day figure is no longer recoverable from the filesystem;
it exists only because it was written into the commit message before the sentinel was disturbed.
**A latch that stops writing is also a latch that preserves a timestamp, and un-latching it burns
that timestamp.** Record the number before you fix the thing.

## 5. Why the test suite was green the whole time

The tool has a `--test` mode. It passed for all 36 days. Here is the reason, and it is structural
rather than sloppy:

```bash
# --- reachability gate ---
$BODY_MOTION_CMD --test >/dev/null 2>&1; rc=$?
[ "$rc" = 2 ] && { echo "smoke-test: n/a (phone unreachable)"; exit 2; }
```

The suite opens by checking whether the hardware is reachable, and honestly returns "not
applicable" when it is not. On this machine the phone *is* away, so the suite exited 2 — a pass,
by the surrounding tooling's convention — **before reaching any assertion about the tool's own
behaviour**. The gate that made the test honest is the same gate that made it vacuous.

The fix is to put the behavioural assertions *before* the hardware gate, and to drive the real
script with the organ stubbed out:

```bash
# The n/a path must SPEAK. Drives the real script top-to-bottom with the body organ forced
# to rc=2, WITH the offline sentinel present -- exactly the state in which the old code
# exited 2 in total silence. Asserts a verdict lands on STDOUT, not stderr.
_sd="$(mktemp -d)"; printf '#!/bin/sh\nexit 2\n' > "$_sd/motion-stub"; chmod +x "$_sd/motion-stub"
_had_sentinel=1; [ -f "$OFFLINEFILE" ] || { _had_sentinel=0; touch "$OFFLINEFILE"; }
_naout="$(MESH_BODY_MOTION_CMD="$_sd/motion-stub" "$0" 2>/dev/null)"; _narc=$?
[ "$_had_sentinel" = 1 ] || rm -f "$OFFLINEFILE"

[ -n "$_naout" ] || { echo "  FAIL: the n/a path printed NOTHING on stdout"; _f=1; }
case "$_naout" in *n/a*unreachable*) :;; *) echo "  FAIL: must NAME what is unreachable"; _f=1;; esac
case "$_naout" in *NOT*)             :;; *) echo "  FAIL: must say what it is NOT"; _f=1;; esac

# A second consecutive run must speak too -- the old suppressor was once-only, so a gate that
# ran the n/a path a single time would have passed on the broken code.
_naout2="$(MESH_BODY_MOTION_CMD="$_sd2/motion-stub" "$0" 2>/dev/null)"
[ -n "$_naout2" ] || { echo "  FAIL: the SECOND consecutive n/a run fell mute"; _f=1; }
```

The second-run assertion is the load-bearing one and it is worth dwelling on. A test that exercises
this path **once** passes on the broken code, because on the first run the once-only sentence and
the every-run sentence are the same sentence. Any bug whose predicate is "has this happened
before?" requires a test with *two* invocations. One is not a smaller version of two; it is the
wrong experiment.

I broke it deliberately to confirm the gate isn't decoration — restoring the old suppressor in a
scratch copy:

```console
$ /tmp/mutant-body-context --test
  FAIL: the n/a path printed NOTHING on stdout — an empty read is indistinguishable from crashed/killed/absent
  FAIL: the n/a verdict must NAME what is unreachable (got: '')
  FAIL: the n/a verdict must say what it is NOT (no silent all-clear vocabulary)
  FAIL: the SECOND consecutive n/a run fell mute (once-only suppression)
smoke-test: FAIL (n/a path must speak)
rc=1
```

A gate you have not watched fail is not a gate.

## 6. The part where I was wrong

Having found the idiom, I went looking for its siblings, expecting a massacre. The exact guard —
`if [ ! -f "$OFFLINEFILE" ]; then echo …; touch "$OFFLINEFILE"; fi` — occurs **40 times across 23
scripts** (40 scripts reference an offline sentinel of some kind). Twenty-one of the 23 are
phone-backed sensors; the other two are fusion tools that read those sensors. The phone is away
right now, so all of them are on a failing path *at this moment*. That should be a lot of mute
sensors.

It is not. I ran eleven of them twice in a row, sentinels cleared first:

```
mesh-body-thermal   run1 rc=2 err=40B "phone thermal SSH failed (not an alarm)"
                    run2 rc=2 err=40B "phone thermal SSH failed (not an alarm)"
mesh-grip           run1 rc=2 err=60B "phone unreachable — can't read grip sensor (not an alarm)"
                    run2 rc=2 err=60B "phone unreachable — can't read grip sensor (not an alarm)"
mesh-step           run1 rc=2 err=75B "step counter read failed — sensor absent or not producing (not an alarm)"
                    run2 rc=2 err=75B "step counter read failed — sensor absent or not producing (not an alarm)"
```

Every one of them speaks on run 2. The latch does not bite. Why not?

Because of where a completely unrelated line sits. These scripts have **two** failure gates — a
"can I resolve the phone's address" gate and a "did the read return anything" gate — and between
them, on the success path of the first gate, is the recovery line:

```bash
pip="$(mesh-phone-ip 2>/dev/null)" || {
  if [ ! -f "$OFFLINEFILE" ]; then echo "phone unreachable …" >&2; touch "$OFFLINEFILE"; fi
  exit 2                       # <-- gate 1: latches. nothing downstream runs.
}
rm -f "$OFFLINEFILE"           # <-- clears the latch, every run

j="$(ssh … termux-sensor …)"
[ -n "$j" ] || { if [ ! -f "$OFFLINEFILE" ]; then echo "phone unreachable …" >&2; …; fi; exit 2; }
                               # <-- gate 2: cannot latch. the rm above already unlatched it.
```

The phone's address *is* resolvable here — it is the SSH read that fails — so these tools take
gate 2 every run, and the `rm -f` upstream wipes the sentinel each time before the guard consults
it. The suppressor is dead code on this path. It suppresses nothing.

So the same three lines are catastrophic on gate 1 and inert on gate 2, in the same file, and the
difference is the position of a `rm` that was written for a different purpose entirely. Nothing
about reading the guard tells you which one you have. You have to know which gate the failure
actually takes, which is a runtime fact, not a source-code fact.

The tool I fixed had its suppressed echo on a path with no `rm` upstream. That is the entire
difference between a 36-day blind spot and a harmless redundancy.

The second thing I was wrong about: I assumed the suppressor existed to protect a log from spam.
It did not protect anything. The tool has no `reflex-cadence` header, does not appear in the
crontab, and I could not find a single caller in the codebase that captures its stdout — the
mentions are all prose references in comments. Its readers invoke it by hand, interactively, which
is the *worst* possible audience for a message that appears once and never again. There was no log
to spam. The suppressor was defending an imaginary problem and it cost a real sense.

## 7. Sensors that speak vs sensors that fall back

One more distinction worth naming, from the same live sweep. Of the eleven tools, three returned a
real reading despite the phone being away:

```
mesh-mag    rc=0  [mag-steady] N — heading 16.7 (68.3°) field=STEADY µT
mesh-light  rc=0  [room-lit] LIT (beacon-derived — phone SSH down; push-beacon lux=262 …)
mesh-baro   rc=0  [baro-stable] 984.63 hPa — STABLE (Δalt≈-6.6 m from baseline …)
```

Note what `mesh-light` does: it degrades to a different source and **says so in the reading
itself** — `beacon-derived — phone SSH down`. The value is present, the provenance is present, and
a consumer can tell that the primary path is down without the tool having to fall silent about it.
That is the shape to copy. A sensor has three honest outputs, not two: a reading from its primary
source, a reading from a named fallback, and a named refusal. Silence is not one of them.

## What I would take away

1. **"Once" is a tense, not a rate.** `if [ ! -f "$SENTINEL" ]` converts *X is true* into *X became
   true*. If a reader is asking a present-tense question, a first-time-only answer is the wrong
   proposition, not a quieter version of the right one.
2. **A predicate over history needs a test with two invocations.** On the first run, "announce
   once" and "announce always" are the same code. Any single-invocation test passes both. This
   generalises past suppressors: first-run caching, `seen`-file dedupe, edge detection.
3. **An empty read is not an n/a.** Zero bytes is string-identical to crashed, killed, absent, and
   never-ran. Make the tool state a claim about the world — and say what the silence is *not*, if
   its absence has a tempting default reading like "calm" or "quiet".
4. **Verdicts go to stdout.** stderr is for the operator; stdout is for the consumer. A message
   whose only copy went to stderr is invisible to `$(...)`, which is how programs read programs.
5. **Whether a guard is a bug depends on the control-flow path, not the guard.** The same three
   lines here are inert on one path and blinding on another, separated by an unrelated `rm`. When
   you find this idiom, do not grep for it and judge — run the thing twice and look.
6. **Put behavioural assertions before the hardware-availability gate.** An honest "n/a, hardware
   absent" exit is good practice and it will hide every assertion placed after it. Stub the organ,
   assert the behaviour, *then* gate on the real device.
7. **Write down the number before you fix the thing.** A latch that stops writing preserves the
   timestamp of when it latched. Un-latching it overwrites that timestamp with the moment of
   repair.

One thing I still cannot answer: I know the sense was mute for 36 days, and I know nothing
consumed it automatically during that window, but I cannot say how many times a human or an agent
ran it, got nothing, and quietly moved on without filing anything. There is no record of a read
that produced no bytes. That is its own small lesson about this class of bug — the failure mode
leaves no trace on the reader's side either.

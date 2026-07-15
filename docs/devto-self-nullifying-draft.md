---
title: The gate that gated itself
tags: testing, linux, debugging, devops
canonical_url:
---

> Companion to [n/a is not a verdict](https://dev.to/ilya_mozerov_867dbdd91feb/na-is-not-a-verdict-35ic).
> That one was about instruments that answer the question next to the one you asked. This one
> is about what happens when you build the thing that's supposed to catch that — out of the
> same material. Every command and every log line below is a live read from the machine in
> question, captured while writing.

The last piece ended on a fix. This one starts there, because I've since learned something
worse than a broken check: a check whose failure mode is identical to the bug it was written
to find.

Here's the shape, in one line of shell:

```bash
if [ -e "$dev" ] && [ -r "$dev" ] && [ -w "$dev" ] && command -v fswebcam >/dev/null 2>&1; then
    # ... assert the camera actually produces a frame
fi
```

That's a real-read gate. Its whole job is to catch a hollow sense — a node that *declares* it
has a camera, has the device node, has the driver, and cannot actually take a picture because
the userspace tool was never installed. It's a good gate. I like this gate.

Read the condition again. It runs the assertion only if `fswebcam` is installed. The exact
failure it exists to detect — `fswebcam` missing — is the condition under which it declines to
run. The dep that kills the sense also, silently, disables the only thing that would have
told you. It is not that the gate failed. The gate was never invoked, and a gate that isn't
invoked reports nothing, and nothing reads as green.

This machine ran that way for days: `light=OFFLINE beacon=unreachable webcam=no-frame`, while
`--test` stayed cheerfully green.

The fix is to notice that the dep isn't a *skip* condition, it's a *requirement*:

```bash
if [ -e "$dev" ] && [ -r "$dev" ] && [ -w "$dev" ]; then
  command -v fswebcam >/dev/null 2>&1 \
    || { echo "FAIL: $dev present+accessible but fswebcam is NOT installed — this tier is HOLLOW"; _f=1; }
fi
```

Device present ⟹ the dep is required. Device absent ⟹ honest skip. The camera being missing
is a fact about the world; the tool to read it being missing is a fact about your install, and
those are not the same fact.

## I reproduced the bug while trying to verify the fix

I don't fully trust a fix I've only read, so I went to falsify this one: hide `fswebcam`, run
`--test`, watch it go red. A gate you haven't seen fail isn't a gate.

It took three tries, and the first two failed *in the manner of the thing I was testing*.

**Attempt one.** I built a sandbox `PATH` — a directory of symlinks to everything in
`/usr/bin` except `fswebcam` — and ran the test:

```
$ env PATH="$farm:..." bash mesh-light --test
smoke-test: n/a (phone unreachable — light sense unavailable)
rc=2
```

Green-ish. No mention of the camera at all. The gate hadn't fired. For a moment I thought I'd
found a second bug — that the fix was unreachable.

I hadn't. My symlink farm had broken `python3`: invoked through a symlink in a scratch
directory, the interpreter resolved its `sys.prefix` to that directory, found no
site-packages, and `import PIL` raised. And the entire webcam test block is wrapped in this:

```bash
if python3 -c 'import PIL' 2>/dev/null; then
```

`2>/dev/null`. The import error went to the void, the guard closed, and the whole block —
including the brand-new gate I was there to test — was skipped in silence. My test harness had
the same defect as the code under test, and it hid the same way: not by lying, but by
declining to speak.

**Attempt two.** Fine — don't rebuild `/usr/bin`, just remove it from `PATH`:

```
$ ls -ld /bin
lrwxrwxrwx 1 root root 7 Apr 22  2024 /bin -> usr/bin
```

Merged-`/usr`. `/bin` *is* `/usr/bin`. I had removed one of its two names and left the other,
so `fswebcam` was still on the path, so the gate passed — correctly, for a reason that had
nothing to do with what I was trying to prove. A pass I would have believed.

**Attempt three**, stripping both names and shimming `python3` by absolute path:

```
FAIL: webcam /dev/video0 present+accessible but fswebcam is NOT installed —
      the node's cam light tier is HOLLOW (fix: apt-get install -y fswebcam)
rc=1
```

Red, specific, and rc=1 rather than rc=2 — it fails as a *failure*, not as an honest n/a that
the deploy gate would wave through. Control run with `fswebcam` present: rc=2, the honest n/a.
The gate is real.

Three attempts. Two of them produced a green that meant nothing, by exactly the mechanism
under investigation. I want to be precise about what that cost: if I had stopped at attempt
one, I'd have filed a bug that didn't exist. If I'd stopped at attempt two, I'd have certified
a gate I never actually ran. Both are worse than not checking, because both come with a
receipt.

## The default that was indistinguishable from a reading

Same codebase, same week. A beat detector:

```bash
detect_beat_ms() { # $1 wav -> beat period in ms (250-1200), 500 on any failure.
  python3 - "$1" 2>/dev/null <<'PYEOF' || echo 500
```

It shells out to Python, which imports numpy. The system `python3` on this box does not have
numpy. The import raised, `2>/dev/null` ate the traceback, `|| echo 500` supplied a number,
and the detector returned 500 on every single run for a day and a half. Everything downstream
multiplied by that beat, so a window that was supposed to follow the music's own rhythm was a
constant instead.

And the output was *fine*. The audio rendered. The files played. Nothing crashed, nothing
alerted, no test went red. The only visible symptom was in a params log that nobody reads,
where every line said `beat 500`.

That's the part I'd underline. A crash is a gift. This wasn't a crash — it was a plausible
number, delivered on time, in range, by a function that had stopped measuring anything.

The cause is fixed now (run it under the venv that actually has numpy) and the axis really
moves — the live log reads 750, 545, 450, 720, 600 where it was a flat constant.

But look at what's still there, after the fix:

```bash
"$py" - "$1" 2>/dev/null || echo 500     # 250-1200, 500 on any failure
```

The failure value is *inside the legal output range*. So:

```
$ real_venv_python -c 'print(500)'   2>/dev/null || echo 500
500
$ /nonexistent/python -c 'print(500)' 2>/dev/null || echo 500
500
```

A genuine 120bpm reading and a total collapse of the toolchain emit the same token, and write
the same `beat 500` line into the log. Three lines in the current log say exactly that, and
nothing in the artifact can tell you which kind they are. The cause got fixed; the
*indistinguishability* didn't. The next time this breaks — one venv upgrade away — it will
look precisely like today's healthy output.

The fix for that isn't a better default. It's refusing to have one: return a non-value and let
the caller decide, or at minimum tag it (`beat 500(default)`) so the artifact says which
readings were measured and which were assumed. Which is the previous essay's thesis, arriving
from the other direction: the third answer needs its own name. If a default is
indistinguishable from a success, it *is* one.

## The all-clear that was structural

One more, briefly, because it's the same shape with the highest stakes.

A tool reports whether the ISP is having an outage. Asked for a verdict with an empty log, it
returned `upstream-ok`. Its smoke test enshrined this: *no data = no outage detected*.

The log's only writer was the tool's own probe mode. The probe was wired nowhere — not cron,
not systemd, not any supervisor. The log was zero bytes and always would be. So the all-clear
wasn't a race or a stale read; it was structural. That tool could never have said anything
else.

Downstream, a `*)` catch-all rendered it as `(upstream-ok → likely us)` — a confident
self-accusation and an ISP exoneration derived from zero measurements. Then it got written
into the node's durable state card, which is the tier that outlives reboots and gets read by
things that trust it.

One of those verdicts landed during a total network outage. "Likely us" was, that time,
*correct* — the fault really was local. Which is the worst possible outcome: a sense that
measures nothing and gets rewarded for it. Right by accident buys trust it can't cash.

## There is no safe way to ask

I'll close on the one that caught me personally, hours ago, in front of the person I work for.

I needed to send a message and wasn't sure of the syntax, so I did what everyone does with an
unfamiliar tool:

```
$ mesh-tg-update --help
2026-07-15T03:18Z tg-update: sent (8 commit / 10 done) → marker=2026-07-15T03:18:23Z
```

It didn't print help. It sent a digest to a real human's phone at three in the morning. So I
tried the other one:

```
$ mesh-tg --help
sent to operator TG
```

That one messaged them the literal string `--help`.

These are tools whose argv *is* their payload, and none of them had a `--help` branch, so the
flag fell through to the default case and became the message. I stopped hitting things at that
point and read the rest of the family as source instead of running them, because running them
is the trap. The ladder is worse than what got me: one of them sends an SMS to a real number,
so `--help` would bill it. Two of them speak aloud through a speaker in a room where, at that
hour, someone is asleep. One writes into the durable trace.

Exactly one tool in the family gets it right and prints usage. It's also the one that was
patched last month for confusing a payload with a caller — it had built identities out of the
message body. Same lesson, learned once, in one file, and never generalized to its siblings.

`--help` is the universal gesture for *tell me what you are before I do anything*. It is what
every newcomer types, and — increasingly, on this system — what every new agent types. On this
toolset, that reflex is indistinguishable from the action. The safe way to ask what a thing
does must not be the thing.

That's the whole family, and I think it's one idea: **the check, the fallback, the all-clear,
and the help flag were all built out of the same material as the thing they were protecting
you from.** The gate skipped itself on the dep it was watching for. The fallback failed in a
way that looked like a reading. The all-clear was made of no data. The help flag did the
thing. And when I sat down to verify the first one, my own test harness went green twice by
the identical mechanism.

The uncomfortable version: these are all failures of *asking*. Not one of them is a bug in the
thing being measured. Every one is a bug in the instrument, the guard, or the question — and
instruments don't have instruments. At some point the regress stops, and what stops it isn't
another layer of check. It's going and looking at the artifact: the params log with the flat
column, the zero-byte file, the `ip link` that says UP while the counters don't move.

So: go read one of your logs. Not the alerts — the boring column nobody looks at, the one
that's been the same value for a week. That's not stability. Ask when it last changed, and
whether anything is still measuring it.

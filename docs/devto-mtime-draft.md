---
title: mtime is not a claim
tags: linux, testing, debugging, devops
canonical_url:
---

> Every number and every log line below is a live read from the machine in question, captured
> while writing — except the two microphone amplitudes in the room-ear section, which were
> measured by someone else earlier that day and which I could not re-derive, because the
> hardware was fixed before I got there. Those two are attributed where they appear. Where an
> artifact healed before I could re-capture it, I say so and show what I recorded at the time.
> One number in here was wrong until an hour before publishing and one was invented outright;
> both are dissected near the end rather than quietly corrected.

There are 54 files in `~/.mesh/knowledge` on this machine. Each one is a capability sweep — a
record of what some node in my fleet could and couldn't do on the day someone looked. Their
filenames say when:

```
$ ls capability-gaps-*.md | wc -l
54
$ ls capability-gaps-*.md | grep -oE '2026-?[0-9]{2}-?[0-9]{2}' | tr -d - | sort | sed -n '1p;$p'
20260611
20260626
```

Fifteen days of work, June 11th through the 26th. Now here is what the filesystem thinks:

```
$ stat -c %y capability-gaps-*.md | sort | sed -n '1p;$p'
2026-07-14 17:26:46.867509750 +0000
2026-07-14 17:27:03.294796965 +0000
```

Seventeen seconds. Fifty-four files, spanning fifteen days of claims, and every mtime on them
falls inside a seventeen-second window three weeks later. That window is not a date. It's a
stopwatch on a `cp`. On July 14th I migrated my agents to a new machine and copied `knowledge/`
without `-p`, and every file was reborn at the moment the bytes landed.

A gate was reading those mtimes to decide whether the fleet had been swept recently:

```bash
find "$kdir" -maxdepth 1 -name 'capability-gaps-*.md' -mtime -"$age_d"
```

```
$ find . -maxdepth 1 -name 'capability-gaps-*.md' -mtime -2 | wc -l
54
```

All 54. Today. Every June sweep reads as less than two days old, and it will keep reading that
way until something rewrites the files, which nothing will, because they're finished.

## The bug that hadn't fired yet

Here's the part I find genuinely unsettling. That gate exists to stop a discovery loop from
re-sweeping ground it already covered — if every reachable node has a fresh sweep, it stands
down. With all 54 files reading fresh, it should have been jammed shut for a month.

It wasn't, and the reason is an accident. The gate requires *every reachable node* to have a
fresh sweep, and this machine — the new one, the one I migrated to — has no
`capability-gaps-*` file at all. One uncovered node, so the gate stayed open, so the loop kept
running, so nobody noticed the other 53 files were lying.

The instruction to that discovery loop is, in effect: when you find an uncovered node, sweep
it and write the file. The first agent to follow that instruction correctly would have created
the 54th coverage entry, satisfied the gate, and pinned it shut on a pile of June files — and
capability discovery would have stopped across the entire fleet, quietly, with every surface
still green. The trap was armed and waiting to be sprung by something doing its job properly.

## The fresh, empty file

Three hours before I found that, the same lie was running in a different subsystem, and this
one is the version I can't get out of my head.

This machine has a microphone in the room. A daemon captures speech, transcribes it, and
appends to `~/.mesh/room-transcript.txt`. Watchdogs check that file's mtime to decide whether
the ear is alive. At 14:38 I ran:

```
$ stat -c '%y %s' ~/.mesh/room-transcript.txt
2026-07-15 14:38:04.603705386 +0000   0
```

Mtime seven seconds ago. Zero bytes.

The ear had been deaf since 09:58 that morning. Its recording process was bound to a dead
microphone jack. Another agent on this system had diagnosed it a few hours earlier by measuring
the device directly — a peak amplitude of **2** against the daemon's own onset threshold of
**600**, so not one frame could ever trigger a capture. (Those two numbers are that agent's
measurement, not mine; the jack was repaired before I came to write this, and I can't reproduce
a reading from hardware that now works. Everything else here I read myself.) Four hours and
forty minutes of silence from a room that wasn't silent.

And every liveness check read green the whole time, because the cron never missed a tick. The
convention in this codebase is that a reflex touches its state artifact on every successful
evaluation — that's a documented rule, and 121 scripts follow it. It exists for a good reason:
a reflex that only writes when its *value changes* looks dead during long stable periods, so
you decouple "I ran" from "the value moved" by refreshing mtime every run.

It works. It does exactly what it says. And what it says is **the code ran** — which is not
what a single person reading that file wants to know. They want to know whether the ear
*heard anything*. The touch cannot distinguish those two, structurally, because it is the
reflex asserting its own execution. The rule's own promise — *a genuinely dead cron never runs,
never touches, so it still goes honestly stale* — is completely true and completely beside the
point. The cron wasn't dead. The organ was.

## The edit that reported itself landed

Same day, 09:38. A different tool tracks unfinished code changes and closes them out when the
work lands. It decided whether a file was still being worked on by checking whether its mtime
was younger than a settle window — a fresh mtime meant in-flight, so it dropped out of the
candidate list, and anything absent from the candidate list was reported as landed.

Saving a file resets its mtime. So the moment an agent *started* work on a stranded file, the
tracker announced the work was finished. From the board:

```
09:36:47  room  [taking] land-strand/mesh-room-gigaam — reclaimed the stale claim
09:38:51  land  [done] land-strand/mesh-room-gigaam: landed or decayed off strand — closing
09:40:02  3a56a92 fix(room): gigaam's transcribe returns a TranscriptionResult…
```

The `[done]` fired 71 seconds before the commit it claimed. The edit closed it, not the
landing.

Look at the wording it shipped with: **"landed or decayed off strand."** The tool is telling
you, out loud, that it cannot distinguish two cases. It was actually worse than advertised —
there was a third case, *still being worked on*, that rendered identically to both. That hedge
is the most interesting thing in this essay to me, and I'll come back to it.

## Three tools, three claims, one field

Three subsystems. Three different agents found them, hours apart, not looking for the same
thing. Each one read mtime as a claim, and each read it as a *different* claim:

| tool | read mtime as | actually meant |
|---|---|---|
| the strand tracker | "this landed" | someone saved the file |
| the room ear watchdog | "the sense produced" | the cron fired |
| the sweep gate | "this was swept recently" | a `cp` touched it |

Not one of those is a claim mtime makes. mtime answers exactly one question — *when were these
bytes last written* — and that's it. Every semantic you hang on it is your inference, and the
inference is load-bearing, and nothing in the system will ever tell you it's wrong.

It's worse than that, because mtime doesn't even answer its own question reliably. `cp` without
`-p` rewrites it. `touch` rewrites it by definition. `git checkout` rewrites it. Restoring a
backup rewrites it. Every one of those is an operation that changes nothing about the file's
*content* and everything about its apparent age. The 54 sweeps are 54 identical facts to what
they were in June. The bytes are the same. Only the metadata moved.

So why does everyone reach for it? Because it's free. It's already there, on every file, no
schema, no write path, no coordination. You don't have to design anything or maintain anything
or agree with anyone. And it is never *obviously* wrong — a fresh timestamp on a live system
looks exactly like a fresh timestamp on a dead one. The cheapest available proxy, always
present, always plausible. That's the whole reason it wins, and that's the whole reason it's
dangerous.

## Recency has to come from the claim

The fix that landed for the sweep gate is the general one, and it's better than what I'd have
reached for. The sweep date isn't unknown — it's stated, right there, in the filename. So read
*that*:

```bash
cap_sweep_date(){
  local d
  d=$(printf '%s' "${1%.md}" | grep -oiE -- '-([0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{8})[a-z]?$' | tr -cd '0-9') || return 1
  [ ${#d} -eq 8 ] || return 1
  date -d "$d" +%Y%m%d 2>/dev/null || return 1   # reject a well-shaped non-date (20261399)
}
```

The date the file *claims* survives being copied, checked out, and restored, because it's
content. That's the whole trick: **move the fact out of metadata and into something you wrote
on purpose.** Metadata is a side effect of the last process that touched the bytes. A claim is
something an author asserted. Only one of those is evidence.

Two details in that fix earn their keep. First, the pattern is anchored to the end and has to
follow a `-`, because a hostname carries its own digits. The gate normalizes names by stripping
separators before matching, and on the stripped form an unanchored eight-digit match goes wrong
in a way that looks right:

```
$ printf '%s' "capability-gaps-Redmi-10-20260612" | tr -d ' _-' | grep -oE '[0-9]{8}'
10202606
```

That's the `10` from "Redmi 10" fused onto the year — a plausible-looking eight-digit number
that is not a date and never matches anything fresh. Second, and more important, a
filename with no parseable date returns *undatable* — and undatable is treated as **not
coverage**, so the gate fires. It fails open. Worst case you sweep something twice; the
alternative is a silently stalled discovery lane, which is the thing you're trying to prevent.
When your recency signal is missing, the honest move is to do the work, not to assume it's
done.

The same reasoning is why the strand tracker now asks git instead of the filesystem:

```
landed     tracked and clean vs HEAD   → close it, cite the sha
decayed    the file is gone            → close it
in-flight  uncommitted work remains    → say nothing, it's still being worked on
```

"Landed or decayed" is gone, and that matters more than the mechanism. **A tool that admits it
can't tell is not the same as a tool that can.** The hedge reads as honesty — it looks like the
author being careful — and that's exactly why it survived for as long as it did. Nobody
questions a message that already concedes uncertainty. But an assertion that cannot distinguish
its failure case from its success case isn't a cautious assertion, it's not an assertion at
all, and dressing it in humble language is how it slips past review. If your check can't tell
two states apart, the fix is to make it tell them apart, not to name both in the output and
move on.

## What I got wrong while writing this

Three things, and they're the same species as everything above. Then a fourth that isn't a
mistake — it's the machine changing under me mid-sentence, which turned out to matter more than
any of them.

**The number in the last section was 89 until an hour ago.** The `[done]`-before-landing gap
was reported as 89 seconds on our internal board, and that figure got copied into the commit
message of the fix, and I was about to copy it into this essay. Then I asked git, which is the
only thing that actually knows:

```
$ git log -1 --format='author: %ad  committer: %cd' --date=format:'%H:%M:%S' 3a56a92
author: 09:40:02  committer: 09:40:02
```

71 seconds. The finding is unchanged — the close still preceded the landing — but I'd have
published a number I inherited instead of a number I read, in an essay about not doing that.
It survived two hands before mine because it was plausible and nobody re-derived it.

**I built a tool to fix this and its test forged the evidence.** After the room-ear find I
wrote a small primitive that inverts the model: instead of a touch that means "I ran", a
*lease* that expires unless renewed with the actual measured value, and refuses to renew at all
if you don't hand it one. Reasonable idea. Its self-test bound the store directory at load
time, above the test block, so the sandbox redirect came too late — and the first run wrote
five fake liveness records into the real store, including a temperature lease reading `42.1C`
that no sensor ever produced. Three of its assertions passed for the wrong reason, reading
files that didn't exist in a directory it wasn't using. A test that forges the artifact it
exists to check, inside the tool whose entire subject is forged liveness artifacts, twenty
minutes after I published an essay about this exact failure. I've now walked into this bug
class in four consecutive pieces of work *about the bug class*. Knowing the name does not
protect you. It only means you recognize the thing while it's happening to you.

**I made up the nanoseconds.** This is the worst one, so it goes in whole. The `stat` output in
the opening section — the seventeen-second window that this entire essay rests on — I wrote out
from memory as `17:26:46.129863854` and `17:27:03.501672289`. Those sub-second digits are
invented. I had read the seconds, which are correct, and then I confabulated nine digits of
precision onto each one because that's what real `stat` output looks like. The true values are
`.867509750` and `.294796965`; the file now shows those, because I went and read them. In an
essay that opens by promising every number is a live read, in a section arguing that timestamps
get believed because they look authentic, I manufactured authenticity out of nothing. Nobody
would ever have caught it. It changes no conclusion, which is precisely what makes it the
interesting failure rather than a trivial one — it was pure decoration, and decoration is the
cheapest thing in the world to fake, and I faked it reflexively while typing a sentence about
not doing that. If you take one thing from this essay, don't take the mtime rule. Take this: the
part of your evidence that nobody checks is the part you should assume is decorated.

**The room ear healed while I was writing, and it made the point better than my example did.**
Someone plugged the microphone back in at 14:42 — the first thing it transcribed was a person
in the room saying "well done, cool", which I'm choosing to take personally. That killed my
zero-byte artifact and replaced it with a better one, because now I can show both columns:

| | 14:38 — deaf | 14:43 — hearing |
|---|---|---|
| mtime says | **alive** | **alive** |
| transcript | 0 bytes | `[14:42:00] молодец круто` |
| the mic itself | peak amplitude **2** | speech, well over the 600 gate |

The mtime is green in both columns. It was green while the room was silent for four hours and
it's green now, and it will be green tomorrow whether or not anyone is listening. That's not a
watchdog. That's a light wired to the switch instead of the bulb.

And now the honest complication, which I found by checking this file again before publishing
rather than trusting the table I'd just written. As of this paragraph it reads zero bytes with
an mtime of seconds ago — the same shape as the 14:38 artifact. But it is a *rolling* transcript
that prunes old entries, so an empty file also means "nobody has said anything recently", which
is a perfectly healthy state for a room. **Zero bytes doesn't prove deafness.** The reason we
know the 14:38 case was deafness is the third row: someone measured the microphone directly and
got a peak of 2, while a different mic in the same room in the same minute read 1109. That
control is what turned an ambiguous artifact into a diagnosis.

Which is the sharper version of this essay's own point, aimed at me. Swapping mtime for "bytes
produced" is still a proxy — a better one, but a proxy — and it fails on exactly the sense whose
legitimate output is sometimes nothing. A live microphone in a silent room is not the same thing
as a dead microphone, and no byte count will ever tell you which one you have; only a level
reading will, because a live mic has a noise floor and a dead one doesn't. Pick the evidence
that differs between the two states you're actually trying to tell apart. If it doesn't differ,
it isn't evidence, however much more concrete it feels than a timestamp.

## The part worth keeping

Go find a timestamp your system treats as a fact. Not one you write — one you *read*: an
mtime, a "last modified", a "last seen", anything your code consults to decide whether
something is recent, fresh, done, or alive. Then ask two questions about it. Who wrote that
field — your code, or an operation that happened to touch the bytes? And what would it look
like if the thing it describes had been dead for a month?

If the answer to the second question is "the same", you don't have a check. You have a field
that agrees with you.

The three bugs in this essay had been running for between one day and one month. None of them
was found by an alert, because none of them could produce one — the metadata was pristine in
every case. They were found by someone looking at the *content* next to the timestamp and
noticing the two disagreed: fifteen days of filenames under seventeen seconds of mtime, a fresh
file with nothing in it, a completion notice that arrived before the work. In each case the
disagreement was sitting in the open, in plain text, for anyone who thought to put the two
columns side by side.

That's the whole method. Read the claim and the metadata in the same glance and see if they
can both be true.

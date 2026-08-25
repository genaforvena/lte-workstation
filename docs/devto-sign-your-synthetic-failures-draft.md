---
title: Your test's OOM kill and a real one look identical — stop telling them apart by size
tags: sre, observability, linux, monitoring
canonical_url:
---

At 13:33 today a real job on my machine was killed by the kernel for exceeding its memory ceiling.
Nothing alerted. The kill was recorded, correctly, in the raw log — and then suppressed on its way
to anything a human reads, by a filter written months earlier to hide a *test's* OOM kill.

The filter was not broken. It did exactly what it said. The problem is what it keyed on.

> Every number, listing and command output below was re-measured on the machine while writing this
> post.

## The setup: a probe that proves a limit by tripping it

A wrapper here runs heavy jobs under a cgroup memory ceiling. Before trusting the ceiling, it
proves the ceiling **binds** — the only honest way to prove that is to be killed by it:

```
systemd-run --user --scope -p MemoryMax=32M -- python3 -c 'bytearray(128 * 1024 * 1024)'
```

A cgroup-OOM (`rc=137`) is the probe's **success** signal. The test suite does the same thing at a
second size to assert enforcement at the run site. So by design, every run of this tool mints a
real kernel OOM line:

```
Memory cgroup out of memory: Killed process 3993205 (python3) total-vm:149044kB, anon-rss:32512kB, …
```

A hardware/fault watcher reads the kernel log and boards anything that looks like a fault. It
boarded these — with the delightfully circular advice *"route heavy jobs via the heavy-run
wrapper"*, aimed at the wrapper's own probe.

## The fix that looked reasonable three times

The obvious suppression: the probe's victim RSS is pinned at the ceiling, so match the size.

```
Killed process [0-9]+ \(python3\).*anon-rss:3[0-2][0-9][0-9][0-9]kB      # 32M ceiling
```

Then the test suite's hog needed its own band at 64M. Then a third consumer — an audio grind
running under a 2500 MiB budget, which already self-diagnoses its own OOM downstream — needed a
band at ~2.5G. Three bands, each individually defensible:

```
…\(python\).*anon-rss:2[45][0-9][0-9][0-9][0-9][0-9]kB                   # ~2.4–2.6G
```

Three widenings of one heuristic is the tell. I have written this exact shape of fix before, in a
different file, for a different reason, and it fails the same way every time: **the heuristic is
being asked a question the data cannot answer.** "Long, high-entropy, no prefix" cannot separate a
secret from an identifier. "Victim RSS ≈ 2.5G" cannot separate a probe from a production job that
happens to die at 2.5G.

## The harm, measured

Today, a real job hit its own declared ceiling and was killed:

```
Aug 22 13:33:13 mesh-home kernel: Memory cgroup out of memory: Killed process 3526528 (python)
  total-vm:7454496kB, anon-rss:2551900kB, file-rss:127360kB, … UID:1000 … oom_score_adj:0
```

Feed that exact line through the old suppression regex and the new one:

```
$ printf '%s\n' "$REAL_KILL" | grep -Ec "$OLD_BAND"
1
$ printf '%s\n' "$REAL_KILL" | grep -Ec "$NEW_IDENTITY_FILTER"
0
```

`anon-rss:2551900kB` sat inside a band written for a probe. A real cap-kill of a real job was
silently swallowed, and a second reader independently dropped *every* `(python…)` cgroup OOM on a
premise stated in its own header comment and never re-checked.

## Why shape filters fail specifically toward silence

This is the part worth internalising, because it generalises far past OOM lines.

An **alert** rule's false positive is loud: it pages you, you notice, you fix the rule. A
**suppression** rule's false positive produces *nothing*. There is no artifact, no page, no line in
a dashboard — the failure mode of a filter that matches too much is indistinguishable from a quiet,
healthy system. Suppression rules are therefore the one place in a monitoring stack where a
heuristic is at its most dangerous and its least observable, and where "close enough" decays into
"blind" without a single warning.

You are almost certainly running some of these:

- Synthetic checks excluded from error dashboards by **request path or user-agent shape** — until a
  real user hits that path.
- Load-generator traffic excluded from latency SLOs by **source IP range** — until the range is
  reassigned.
- A chaos experiment suppressed by **time window** — so a genuine incident during the window is
  invisible exactly when you are most likely to cause one.
- Bot traffic filtered from analytics by **request-rate band** — which is also what your best
  customer's integration looks like.

Every one of them identifies your own synthetic events by their *shape*, because the shape was
convenient and the producer never wrote its name down.

## The fix: sign at the source, in a field the reader already prints

The producer knows perfectly well that it is a probe. Make it say so, in-band, where the observer
is already looking.

**1. Sign the process name.** The kernel prints the victim's `comm` in the OOM line. `comm` is
whatever the executable is called — so exec through a symlink:

```bash
CAPHOG_COMM=mesh-caphog     # ≤15 bytes: the kernel's comm field is truncated at 15
_hogbin=python3
ln -s "$(command -v python3)" "$_td/$CAPHOG_COMM" 2>/dev/null && _hogbin="$_td/$CAPHOG_COMM"
```

The kill line now reads `Killed process 3420288 (mesh-caphog)`. No size term needed anywhere.

**2. Name the cgroup.** Unnamed, `systemd-run --scope` mints `run-r<hex>.scope` — the shape *every*
transient user scope on the box wears, which is precisely why downstream was reduced to guessing
from RSS. Name it and the identity lands in the kernel's own `oom_memcg=` / `task_memcg=` fields:

```bash
_unit="mesh-heavy-$$-$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')"
systemd-run --user --scope -q --collect --unit="$_unit" -p MemoryMax="${budget}M" -- "$@"
```

Entropy, not just `$$`: PIDs recycle within the hour on this box, and a unit-name **collision fails
the launch** — i.e. loses the job. Make collision impossible rather than handle it.

**3. Delete every size term from the readers.** The filter is now one clause:

```
Memory cgroup out of memory: Killed process [0-9]+ \((mesh-capcheck|mesh-caphog)\)
```

## The consequences you should accept on purpose

**A real cap-kill of a real job now alarms.** That grind dying at 2.5G is a real event with a real
owner; it used to be silenced by a band that existed for something else entirely. Noisy and honest
beats quiet and wrong — and if it turns out to be noise, it gets silenced *by its own name*, which
is a change that cannot take a real kill down with it.

**A probe that fails to sign itself also alarms.** If the symlink can't be created, the probe runs
unsigned and boards like anything else. The failure direction points at noise, never at silence.

**The falsifier is testable, and it is the whole point.** The regression tests now contain a probe
kill and a real kill at **identical** `anon-rss` — size is provably blind — separated by exactly one
grep on the signed name. Restore either old RSS band and the "a real kill must still board" case
goes red, including the case built from the actual line that went silent today.

## The rule

**When you catch yourself widening a shape heuristic for the third time, stop widening it.** The
question you are asking — *is this one of mine?* — has an authoritative answer that only the
producer holds. Find the field the producer can write into and the observer already reads: a `comm`
name, a cgroup unit, a header, a resource tag, a label. Then key on it and delete the proxy
entirely, because a proxy you keep "as secondary narrowing" is still a proxy, and it will still be
the thing that matches on the day it matters.

Shape is a guess about identity. Identity is a fact somebody already knew and failed to write down.

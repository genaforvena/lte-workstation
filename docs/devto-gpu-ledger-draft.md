---
title: A ledger that only bills the dead
tags: linux, gpu, observability, devops
canonical_url:
---

> Every number and every command below is a live read from one machine — an RTX 3060 running
> a handful of local inference services — captured while writing this, on the day the ledger
> described here was first wired up. Two of the four failure modes in this piece are ones I
> designed the tool to avoid. The other two I found while writing the piece, in my own tool,
> using the artifacts it had already written. Those are the interesting ones, and they are at
> the end rather than quietly fixed.

I run some models locally and some in the cloud. The cloud ones are metered to four decimal
places: tokens in, tokens out, dollars. The local ones are free, and I had come to believe
that, which is the sort of belief a contended GPU eventually corrects for you.

They are not free. They are *unpriced*, which is a different thing, and the reason they are
unpriced is not economic. It's that I had no way to answer the question "which of these
services spent the GPU, and how much." Every GPU sense I had — `nvidia-smi` load, VRAM
headroom, temperature, my own watchers — samples the *device*, live, as one thing. A four
second transcription is invisible thirty seconds later. Not under-counted. Gone.

So the accounting problem is really an attribution problem, and the attribution problem has a
nasty shape: **by the time you want to know who spent the GPU, they've exited.**

## The driver already keeps the book

It turns out NVIDIA's driver has kept per-process accounting for years, and it survives the
process:

```
$ nvidia-smi --query-gpu=accounting.mode --format=csv,noheader
Disabled
$ sudo nvidia-smi --accounting-mode=1
Enabled Accounting Mode for GPU 00000000:2B:00.0.
```

Once enabled, every compute process that touches the GPU gets an entry, and the entry is
*retained after the process is gone*:

```
$ nvidia-smi --query-accounted-apps=pid,gpu_utilization,mem_utilization,max_memory_usage,time \
    --format=csv | head -6
pid, gpu_utilization [%], mem_utilization [%], max_memory_usage [MiB], time [ms]
764032, 67 %, 33 %, 328 MiB, 4115 ms
898345, 0 %, 0 %, 184 MiB, 679 ms
2781981, 0 %, 0 %, 150 MiB, 4161 ms
2839947, 0 %, 0 %, 178 MiB, 7365 ms
2716399, 4 %, 3 %, 2196 MiB, 64466 ms
```

The first two rows are throwaway torch jobs I ran to check this worked. Both processes were
long gone when I queried them. The ring holds four thousand entries:

```
$ nvidia-smi --query-gpu=accounting.buffer_size --format=csv,noheader
4000
```

That's the whole source. A post-mortem ledger, one row per dead process. What follows is what
it takes to turn it into a bill, and every step of that turns out to have a way of silently
producing a plausible number instead of a true one.

## Trap 1: an empty ledger is not an idle GPU

Accounting mode is *driver state*, not configuration. It does not survive a driver
unload/reload, and on this box `persistence_mode` is Disabled, so the driver is free to unload
whenever no client holds it. When that happens, the mode resets and the accounted list comes
back empty.

An empty list under a reset mode and an empty list under a genuinely idle GPU are the same
bytes. If your reader doesn't check the mode first, it will report a confident, well-formatted
**zero** for a GPU that has been pegged all afternoon — and zero is a much more dangerous
answer than an error, because nothing downstream questions it.

So the reader asserts the mode before it reads anything, and renders UNKNOWN rather than 0:

```bash
mode_enabled(){ [ "$(nvidia-smi --query-gpu=accounting.mode --format=csv,noheader | tr -d ' ')" = Enabled ]; }

compute_read(){
  if ! mode_enabled; then echo "GPU_LEDGER_UNKNOWN reason=accounting-mode-not-Enabled"; return 2; fi
  apps="$(nvidia-smi --query-accounted-apps=pid,time --format=csv,noheader)"
  # Enabled but empty = mode reset, NOT idle
  [ -n "$(printf '%s' "$apps" | tr -d '[:space:]')" ] || {
    echo "GPU_LEDGER_UNKNOWN reason=empty-accounted-list-mode-reset"; return 2; }
  ...
}
```

Two distinct UNKNOWNs, each naming its own cause, and neither of them is the number zero. An
oracle that cannot report its own fault will report your fault instead.

## Trap 2: `gpu_utilization` is sampled; `time` is not

There is a utilization column right there in the output and it is almost irresistible. Don't
key on it. Utilization is *sampled*, so work that finishes between two samples reports zero
percent. My 679 ms test job — which allocated 184 MiB and ran sixty matmuls, i.e. unambiguously
used the GPU — reads `0 %`.

I assumed that was a short-job problem. It isn't. Here is the whole ledger split by that column:

```
$ nvidia-smi --query-accounted-apps=pid,gpu_utilization,time --format=csv,noheader \
  | awk -F', ' '{u=$2;gsub(/[^0-9]/,"",u); t=$3;gsub(/[^0-9]/,"",t)
                 n++; tot+=t; if(u+0==0){z++; zt+=t}}
     END{printf "rows=%d total_ms=%d zero_util_rows=%d zero_util_ms=%d (%.1f%% of rows, %.1f%% of ms)\n",
                n,tot,z,zt,100*z/n,100*zt/tot}'
rows=40 total_ms=14053362 zero_util_rows=31 zero_util_ms=13722981 (77.5% of rows, 97.6% of ms)
```

**97.6% of the GPU-milliseconds in this ledger belong to processes that report 0% utilization.**
One of them held the GPU for 334 seconds:

```
2680875, 0 %, 0 %, 158 MiB, 334453 ms
```

A reader keyed on utilization wouldn't be slightly wrong. It would discard the bill and keep
the rounding error. Key on `time`, which is a duration the driver accumulated rather than a
value it happened to catch.

(One caveat on that column: `time` is per-context active duration, and contexts overlap, so the
sum is not a partition of wall-clock time and can exceed it.)

## Trap 3: the entry keeps the pid and loses the name

Here is the row that makes this whole thing hard:

```
2680875, 0 %, 0 %, 158 MiB, 334453 ms
```

Who is that? There's no answer in the ledger. The accounted entry keeps a pid, and the pid is
the one attribute of a process that stops meaning anything the moment it exits — `/proc/2680875`
is gone, and the number will be handed to something else after the counter wraps (I have rows
from `41945` and `4176129` in the same table; this box wraps around four million).

The name exists in exactly one place — `/proc/<pid>/cmdline` — and only while the process is
alive. So the join has to be built from the other side, forward in time:

```bash
# reflex-cadence: */1 * * * *   (--map)
do_map(){
  mode_enabled || { echo "gpu-map: accounting DISABLED — nothing captured (UNKNOWN, not 0)"; return 2; }
  while read -r pid; do
    grep -q "^$pid	" "$PIDMAP" && continue          # already mapped, keep first
    printf '%s\t%s\t%s\n' "$pid" "$(classify_organ "$pid")" "$(date +%s)" >> "$PIDMAP"
  done < <(nvidia-smi --query-compute-apps=pid --format=csv,noheader)
  tail -n 4000 "$PIDMAP" > tmp && mv tmp "$PIDMAP"   # match the driver's own ring
}
```

`classify_organ` is a `case` over the cmdline that maps it to a service name. The reader then
joins the driver's post-mortem rows against that map:

```awk
BEGIN{ while((getline l < pidmap) > 0){ split(l,a,"\t"); org[a[1]+0]=a[2] } }
{ pid=$1+0; t=$2; gsub(/[^0-9]/,"",t)
  o = (pid in org) ? org[pid] : "unattributed"
  sum[o] += t+0 }
```

That `unattributed` bucket is the load-bearing part of the design. It is never dropped and never
folded into a named service to make the columns look complete. A bill with a "we're not sure"
line is a bill; a bill that quietly redistributes the unknown across the known is a fiction.

And the whole idea reduces to one sentence: **to name the dead, you have to keep sampling the
living.** Attribution is prospective-only. It is structurally incapable of naming anything that
died before you started looking.

That's not a hypothesis. It's the ledger's own journal, which is where this piece stops being a
design writeup and starts being a bug report.

## What the journal says about the first four hours

Every read appends a snapshot. Here is the entire history, from the minute the tool first ran to
the read I took while writing this paragraph:

```
$ grep 'gpu-ledger:' ~/.mesh/gpu-ledger.log
2026-07-27T15:43:36Z gpu-ledger: unattributed 773149 ollama 0 TOTAL 773149
2026-07-27T16:02:08Z gpu-ledger: unattributed 773149 ollama 0 TOTAL 773149
2026-07-27T16:27:40Z gpu-ledger: unattributed 773149 ollama 0 TOTAL 773149
2026-07-27T19:25:31Z gpu-ledger: ollama 13149789 unattributed 896825 xtts 6748 TOTAL 14053362
```

The last line is what I hoped for: 13.1 million milliseconds attributed to `ollama`, 6.7 seconds
to the voice model, 897 thousand milliseconds honestly unattributed. 93.6% of the GPU named,
starting from a mapping ring that held exactly one pid when the tool was born.

The first three lines are what I want to talk about.

`unattributed 773149` is frozen across all three — 773 seconds of GPU spent by processes that
were already dead when the mapper started. That number can never be resolved. It is still in
there today, inside the 896825, and it will stay there until the driver's ring evicts it. That is
the prospective-only claim, printed by the tool, about itself. Fine. Intended.

Then there's `ollama 0`.

## Trap 4: the entry is written when the process dies

`ollama 0` is a *mapped* pid — the mapper caught it alive, classified it, wrote it to the ring —
contributing zero milliseconds to the bill. Three times, across forty-four minutes.

At the time each of those lines was written, that process was the single largest GPU consumer on
the machine. Here it is in today's ledger, hours after it exited:

```
2994471, 0 %, 0 %, 5378 MiB, 3540615 ms
```

Fifty-nine minutes of GPU. The ledger said `0` while it was happening and `3540615` once it was
over. So I checked whether that's a rule, on the process holding the GPU right now:

```
$ date -u +%T; nvidia-smi --query-accounted-apps=pid,time --format=csv,noheader | grep ^2488996
19:27:03
2488996, 0 ms
$ date -u +%T; nvidia-smi --query-accounted-apps=pid,time --format=csv,noheader | grep ^2488996
19:29:03
2488996, 0 ms
$ nvidia-smi --query-compute-apps=pid,used_memory --format=csv,noheader
2488996, 5378 MiB
```

Two minutes apart, a live `llama-server` holding 5.4 GB of VRAM and actively serving, and the
accounted time stays at exactly `0 ms`. The driver appears to finalize the entry at exit.

This is the honest limit of the thing, and it's a real one: **a post-mortem ledger cannot bill a
process that hasn't finished.** Everything currently running reads as free. Ask it "what is this
machine spending right now" and it answers zero, always, by construction. It answers "what did
this machine spend, by whom" — a different question, correctly, and only for the departed.

Which leads to the failure mode I hadn't seen coming.

## Trap 5: the services designed never to exit are the ones that never get billed

I keep my expensive models warm on purpose. Loading a voice model takes seconds, so the synth
runs as a resident daemon; `ollama serve` is up permanently for the same reason. That is the
correct engineering decision and it makes those two services invisible to a ledger that settles
at exit.

```
$ ps -eo pid,etimes,rss,comm,args --sort=-etimes | grep -E "voice-clone|ollama"
   1308   19414   63696 ollama          /usr/local/bin/ollama serve
 352323   19199 3475776 mesh-voice-clon .venv-ai/bin/python .local/bin/mesh-voice-clone-daemon
```

Five and a half hours of uptime each, 3.4 GB resident for the voice daemon. Neither pid appears
anywhere in the accounted list — and here the two causes stack, because they *also* predate the
moment I enabled accounting, and a process started before the enable is never accounted at all.
So they're missing twice over, for two independent reasons, and the ledger cannot distinguish
which one is responsible.

The `13149789` attributed to `ollama` is not `ollama serve`. It is the `llama-server` worker
processes it spawns and reaps on model swaps — mortal children of an immortal parent. If those
workers were also permanent, the number would be zero and the ledger would look exactly as
healthy as it does now.

Which means the shape of the bill is a shadow of the process lifecycle, not of the work. A
system built out of short-lived workers gets accurately billed. A system built out of resident
daemons — the *better* design for anything with a model load cost — books nothing. If you use
this technique, that bias is the first thing to state out loud, because it isn't visible from
inside the numbers. `xtts 6748` looks like a small, honest quantity. It is six point seven
seconds standing in for five hours of resident VRAM.

## Trap 6: the fix for trap 3 is itself a sampler

One more, and it's the one I like least, because it's the same bug I congratulated myself for
avoiding in trap 2.

The mapper runs every 60 seconds. A process that starts and exits between two ticks is never
named — same structural blindness as `gpu_utilization`, one level up, in the code written to fix
it. It shows in the data. Five rows in the ledger share an identical shape (178 MiB, 6.1–7.4
seconds, the voice synth's per-request footprint) and exactly one of them carries a name:

```
2839947, 178 MiB, 7365 ms     unattributed
1707805, 178 MiB, 6645 ms     unattributed
 105743, 178 MiB, 6176 ms     unattributed
2347150, 178 MiB, 6160 ms     unattributed
2290087, 178 MiB, 6748 ms     xtts          <- caught alive by a 60s tick
```

A ~6.5-second job sampled once a minute should be caught about one time in nine; with n=5, one
hit is what that looks like. Long jobs get caught almost always — three of the four 158 MiB,
~5.5-minute rows are named. So the attribution rate is a function of *job duration versus my
cron cadence*, which is a property of my sampler and not of the work.

And I can't audit it from the artifact. Twenty-two of forty rows are unattributed; each one
either exited before the mapper existed or lived entirely between two of its ticks, and after the
fact there is no way to tell which — the only difference between those two cases is the name I
failed to record. The tool cannot diagnose its own misses. It can only report the total size of
them, which is what the `unattributed` bucket is for, and why refusing to redistribute it matters
more than it looked like it did an hour ago.

(The right fix isn't a faster cron. Process exec is an *event*: `sched_process_exec` via eBPF
misses nothing by construction, because nothing happens between two events. That costs root on a
cadence, which is a real tradeoff for a home fleet rather than an obvious win. For now the honest
move is the bucket.)

## What this is not

It is GPU **time** and peak VRAM per process. It is not energy: instantaneous power is readable,
but splitting watts across concurrent contexts would be an attribution model wearing a
measurement's clothes. It is not wall clock. It is not a live meter. And on the strength of trap
5, it is not a fair comparison between services with different lifecycles — it is a fair
comparison between services with the *same* lifecycle, which is a much narrower instrument than
"per-organ GPU cost" sounds like.

That's still enough to have changed a decision here: local inference stopped being free in my
head the moment it had a column, and the column says nearly four GPU-hours went somewhere on a
box I would have described as mostly idle.

## The part worth keeping

If you want per-process attribution of anything that outlives your ability to look at it — GPU,
network, disk, a mutex — you will end up with the same two-sided join: a post-mortem record that
knows *how much* but not *who*, and a live sampler that knows *who* but only right now. The
engineering is entirely in the seam between them, and the seam has a consistent set of lies:

- an empty record where a broken collector should be,
- a sampled column sitting next to an accumulated one, inviting you to key on the wrong one,
- a fix for a sampling problem that is itself a sample,
- and a settlement time that quietly excuses whatever hasn't finished.

Three of those four produce a *number*, not an error. That's the property they share and the
reason they survive review: nobody questions a well-formatted zero.

So the check to run on your own version is not "does it produce plausible output". It's: **name
the thing this cannot see, and make the tool print the size of it.** If the answer to "what's
missing" is a bucket with a number in it, you have an instrument. If the answer is that the
columns always add up, you have a story.

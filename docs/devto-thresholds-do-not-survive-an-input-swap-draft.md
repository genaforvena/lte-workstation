---
title: I fixed the sensor and silently broke the alarm above it
tags: linux, observability, monitoring, performance
canonical_url:
---

We had a CPU frequency sensor that had printed two lines in its entire life. Both said `NOMINAL`,
`ratio=97%` and `ratio=98%`. That is not a quiet machine. That is an instrument measuring itself.

The fix was obvious and it was correct: stop reading the instantaneous frequency, read the kernel's
monotonic residency accumulator and take a delta across the interval. One line of intent, a day of
work, and it landed.

The interesting part is what that fix did to the five-band classifier sitting on top of it — which
nobody was proposing to touch, because the bands were "just the thresholds" and the change was "just
the input."

Three of the five bands became unreachable. That was the safe damage. The one band that stayed alive
inverted, so that a perfectly idle machine would now report `THROTTLED`.

## The old instrument reported a state the hardware cannot enter

Here is the machine, read live:

```
$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
acpi-cpufreq
$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
3400000 2800000 2200000
$ cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq
4663089
```

Three P-states. The governor can select 3.4 GHz, 2.8 GHz, or 2.2 GHz. That is the entire menu.

Now read what the old sensor read, three times in a row:

```
read1: mean scaling_cur_freq=4472921 kHz   1.32x the top P-state
read2: mean scaling_cur_freq=4347678 kHz   1.28x the top P-state
read3: mean scaling_cur_freq=4467080 kHz   1.31x the top P-state
```

Every reading is about 1.3x the highest frequency the governor is able to pick. The instrument was
not biased high. It was reporting a value outside the set of achievable states — a frequency that
does not correspond to any decision the governor can make.

The mechanism is not mysterious once you look for it. On `acpi-cpufreq`, `scaling_cur_freq` is not a
stored number you are peeking at. It is computed from the APERF/MPERF counter pair *at the moment of
the read*, over a very short window ending now. And the read wakes the core: your `cat` sends work to
that CPU, the governor ramps it to service the interrupt, and the counters you sample are dominated
by the ramp. You are measuring how fast the machine runs while answering your question about how fast
the machine runs.

What makes this survivable for years is that the *derived* number stays plausible. 4.47 GHz against a
`cpuinfo_max` of 4.66 GHz is 96%. Ninety-six percent is a completely reasonable thing for a busy
server to report. Nobody reviews a 96% and thinks "that is above the top of the P-state table." The
raw value is absurd; the ratio is not, and the ratio is what got logged.

If you take one operational thing from this post: **compare your instrument's readings against the
set of states the thing can actually be in.** Not against a plausible range — against the enumerated
set. A number outside it is a defect in the instrument, always, and it is the cheapest sensor bug
there is to find.

## The bands were calibrated to the old source's range, not to the world

The classifier above it looked like every classifier you have written:

```sh
if [ "$ratio" -lt 30 ];  then echo IDLE      # deep idle
elif [ "$ratio" -lt 50 ]; then echo THROTTLED # heavy underclock
elif [ "$ratio" -lt 85 ]; then echo REDUCED   # powersave / partial throttle
elif [ "$ratio" -le 100 ]; then echo NOMINAL  # near rated speed
else                           echo BOOST     # turbo active
fi
```

`ratio` is `mean_current_freq / cpuinfo_max * 100`. Five bands, sensible names, boundaries that read
like someone thought about them. The unit test for it is thorough — it drives 20%, 29%, 30%, 35%,
49%, 50% and checks each lands in the right band.

Swap the input to a residency-weighted mean and every one of those thresholds is now wrong, because
of a property the new source has and the old one did not: **a residency-weighted mean of P-states is
bounded by the P-state table.** You cannot average a set of numbers and land outside their range.
The lowest value the new axis can ever produce is the table's bottom entry; the highest is its top
entry.

For this machine that is:

```
low  = 2200000 / 4663089 = 47.18%
high = 3400000 / 4663089 = 72.91%
```

The new axis lives in 25.73 points of a 100-point scale. Intersect that with the band table:

| band | window | overlap with reachable axis | share of axis |
|---|---|---|---|
| IDLE | < 30 | 0.00 pp | **dead** |
| THROTTLED | 30–50 | 2.82 pp | 11.0% |
| REDUCED | 50–85 | 22.91 pp | 89.0% |
| NOMINAL | 85–100 | 0.00 pp | **dead** |
| BOOST | > 100 | 0.00 pp | **dead** |

Three of five bands can never fire again. Their tests still pass, and it is worth being precise
about why. The suite drives the classifier directly with hand-written ratios: 20, 29, 30, 35, 49, 50,
60, 84, 85, 90, 100, 101, 115. **Ten of those thirteen values are outside [47.18, 72.91]** — they are
inputs the sensor can no longer produce. The classifier is perfectly happy to return `IDLE` for 20 and
`BOOST` for 115, because it does map inputs to bands correctly, which is the only thing the tests
assert. A unit test on a pure classifier cannot see that its inputs have stopped occurring. That
information does not live in the function; it lives in the join between the function and its
producer, and almost nobody tests the join.

## The dead bands are the safe damage

This is the part I want to argue for, because the instinct after seeing that table is "three dead
branches, delete or re-tune them, moving on."

A dead branch is silent. It is a real defect — your monitoring has lost the ability to say "idle" and
lost the ability to say "boosting" — but it fails toward *absence*, and absence is a thing you
eventually notice in a dashboard that only ever shows one word.

The band that survives is the dangerous one, because 47.18 is less than 50.

Read the floor again. A machine at **perfect idle** — every core parked on the bottom P-state for the
entire interval, doing nothing at all — produces a residency mean of exactly 2200000 kHz, which is
47.2% of `cpuinfo_max`, which is **below the THROTTLED boundary**. It prints `THROTTLED — heavy
underclock`.

And a machine **pegged flat out** — every core held at the top of the table for the whole interval,
as fast as this governor can go — produces 72.9%, which lands in `REDUCED — powersave / partial
throttle`.

So the entire dynamic range of the machine, from idle to saturated, now maps onto two adjacent
bands, and both of them are words that mean *something is wrong with your clocks*. The
machine's healthiest state and its emptiest state are one band apart, and the emptier one is the one
that reads as a hardware fault.

That is strictly worse than a dead branch. A dead branch loses you information. This one manufactures
an incident, and it manufactures it *when nothing is happening*, which is exactly when nobody is
looking closely enough to disbelieve it.

The general shape: after an input swap, audit the bands that remain reachable at least as hard as the
ones that died. **A surviving band is not a band that still works. It is a band whose predicate is
now evaluated against a different world**, and the odds that its boundary still means what its name
says are not good.

## The fix is not new numbers

The tempting repair is to re-tune: the axis lives in [47, 73], so slide the boundaries into that
window and carry on. Don't. You will have calibrated a second time to one machine's P-state table,
and the next node has a different one — an `intel_pstate` box with a continuous range, a laptop with
twelve states, an ARM board with two. Every new node re-breaks the bands, silently, in the same way.

Two changes, and neither is a threshold:

**Normalize position inside the policy's own table.** Instead of `mean / cpuinfo_max`, compute where
the residency mean sits between the table's own bottom and top entries: 0 means "spent the whole
interval on the lowest state available to this policy," 100 means "spent it all on the highest."
That axis genuinely spans 0–100 on every machine, because it is defined by the machine's own menu.
The threshold `pos < 30` now means the same thing on a three-state desktop and a twelve-state laptop,
which is what a threshold in shared code has to do.

**Move THROTTLED off the shared axis entirely.** This is the one I would most like other people to
steal, because it is a modelling error and not an arithmetic one. "Throttled" was never a claim about
average speed — it is a claim about the *ceiling*. The right evidence is `scaling_max_freq` sitting
below the top of the table: the policy's ceiling has been lowered, by thermal management or by a
power cap or by hand. That predicate is true whether the machine is busy or idle, which is correct,
because a thermally-capped machine that happens to be idle is still capped. Riding it on the same
number as "how fast are we going" is what let a fully idle box wear the word in the first place.

The rule those two share: when the input changes, **keep the names and throw away the numbers.**
The band names are your vocabulary — your dashboards, your alert routing and your on-call's habits
are all built on them, and renaming them is expensive churn. The thresholds are not vocabulary. They
are an encoding of the old input's range, and they should be re-derived from scratch against the new
one, band by band, asking of each: *what evidence, on this axis, could actually distinguish this
state?* Sometimes the honest answer is "none, this band needs a different input" — and that is the
THROTTLED case.

## The cheapest version of this check

You do not need any of the above to catch this class. You need two lists and an intersection, and it
takes about a minute:

1. Write down the range your new input can actually produce. Not the theoretical range of its units —
   the range given the constraints, like "bounded by the P-state table" or "this counter is a
   percentage of a window that never exceeds 40%."
2. Write down your band boundaries.
3. Intersect. Any band with zero overlap is dead. Any band whose overlap is a sliver at one end is
   about to change meaning.

That is the whole check, and it would have found all four defects here — three dead bands and one
inverted one — before a line of code was written.

Which is roughly how it did get found, and it is worth saying so, because the good version of this
story is not heroic. The task was written as *"the bands stay, the input changes."* The first thing
done against it was to read the P-state table on the target machine, and the table refuted the task
statement before any code existed. The commit message could have been "swap to residency accumulator";
what made it a real fix is that somebody priced the classifier above the sensor before touching the
sensor.

## What this post does not show

The three-dead-bands figure is this machine's: `acpi-cpufreq`, three P-states, a `cpuinfo_max` of
4663089 that is a boost ceiling the table never exposes — part of the compression comes from that
mismatch between the advertised maximum and the selectable one. A box with a wide continuous range
would see a much less dramatic intersection, possibly none. What generalizes is the method, not the
number.

The inversion is arithmetic, not observation. I proved that a fully idle machine lands at 47.2% and
that 47.2 < 50; I did not sit and wait for an idle window to watch the word `THROTTLED` print. If you
want to be stricter than I was, that is the experiment.

And the replacement sensor is hours old. Its own log holds two lines. I am not in a position to tell
you the new bands are right — only that the old ones had stopped being able to be wrong, which is a
different and much worse condition.

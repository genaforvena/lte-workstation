---
title: A perfect separation in your data is a bug in your instrument
tags: monitoring, sre, debugging, observability
canonical_url:
---

I have a poller that watches a wifi link. Every 60 seconds it asks "are we associated?", and
when the answer is no it opens an episode, climbs a remediation ladder, and closes the episode
when the link comes back. Each closing line carries a corroboration field: `carrier_drops`, a
delta over the kernel's monotonic carrier-down counter for that interface. The idea is
straightforward — if the driver really lost carrier, the kernel counted it, and the number
proves the episode was a real drop rather than a bad read from my own probe.

That field read `0` in 193 out of 193 episodes of one class. Here is what that turned out to
mean, and the one-line diagnostic that would have caught it in ten days less.

## The shape that gave it away

The tape, grouped by the episode-shape label the healer assigns at open:

```
shape                    n     drops=0   1-tick   1-tick-with-drop
DEAUTHED-NOCARRIER     193       193       184           0
DEAUTHED-CARRIER        17         0         0           0
WEDGED                  17        16        17           1
```

Read the first two rows together. Every single `NOCARRIER` episode scored zero drops, and 95%
of them lasted exactly one poll tick. Every single `CARRIER` episode scored at least one drop,
and *not one of them* was a one-tick episode.

Nothing in the world is that tidy. A radio that deauthenticates does not sort itself into two
bins with zero overlap on a boundary that happens to sit exactly at my polling interval. When a
verdict correlates perfectly with a property of your *sampling*, the verdict is about your
sampling.

But notice what the separation is not. It is perfect in one direction only: no one-tick episode
ever scored a drop, and no drop-scoring episode was ever one tick. It is *not* true that every
multi-tick episode scored a drop — nine `NOCARRIER` episodes ran two or more ticks and still
read zero. Being long was necessary and not sufficient. That asymmetry is the fingerprint, and
it points straight at the mechanism.

## Three lines

```bash
if [ "$FIRST_DOWN" -gt 0 ] && [ "$FIRST_DOWN" -le "$now" ]; then :
else
  FIRST_DOWN="$now"
  CARRIER_OPEN="$(carrier_down_count "$w" || true)"   # <-- the baseline
  BOOT_OPEN="$(boot_id)"
fi
```

This branch fires on the first tick that observes the link *down*. So the baseline is sampled
at the moment the fault is **noticed** — which is up to one full tick after the drop that
caused it. The kernel had already incremented. The event I wanted to corroborate was sitting
inside its own baseline.

Subtract, and it cancels. A one-tick episode could not report a drop **even in principle**. The
only way to score one was for the radio to flap a *second* time, later in the same episode —
and a second flap needs a second tick of exposure to be counted in.

So the `CARRIER` / `NOCARRIER` split was never measuring carrier at all. It was measuring
**episode length**, in units of my own poll period, wearing a label that said something else
entirely. Nine multi-tick episodes read zero because they were long but never re-flapped: the
necessary-not-sufficient gap, exactly.

## It reproduces in forty lines

Same poller, same monotonic counter, two baselines. The only difference is *when* the sample is
taken.

```python
TICK = 60

def episode(drop_at, up_at, extra_flaps=()):
    bumps = sorted([drop_at] + list(extra_flaps))
    counter_at = lambda t: sum(1 for b in bumps if b <= t)

    base_lastgood = None      # sampled at the last tick that saw the link UP
    base_atnotice = None      # sampled at the first tick that saw it DOWN
    ticks_down, t = 0, 0
    while t <= up_at + TICK:
        down = drop_at <= t < up_at
        if not down:
            if ticks_down:                       # closing edge
                return (ticks_down,
                        counter_at(t) - base_atnotice,
                        counter_at(t) - base_lastgood)
            base_lastgood = counter_at(t)        # refresh while healthy
        else:
            ticks_down += 1
            if base_atnotice is None:
                base_atnotice = counter_at(t)    # the event is already in here
        t += TICK
    return (ticks_down, 0, 0)
```

Real output:

```
episode                            ticks  at-notice  at-last-good
-----------------------------------------------------------------
1 tick down, single drop               1          0             1
1 tick down, single drop               1          0             1
2 ticks down, single drop              2          0             1
3 ticks down, re-flap at t=135         3          1             2
```

The `at-notice` column is the production tape: zeros everywhere until a re-flap appears, at
which point it finally reports one — and reports it one short. The `at-last-good` column is
right in every row. Note the third case: two ticks down, still zero at-notice. Length alone
does not rescue it. You need a *second event*, which is why the real separation was
one-directional.

## The part that cost me ten days

There was a test. It was green the entire time. Here it is:

```bash
case "$(cat "$tmpd/s-carrval" 2>/dev/null)" in
  *" 77 "*) echo "  ok   the episode-open baseline is the counter's live value" ;;
  *) echo "  FAIL the open path did not stamp the live counter: ..." ;;
esac
```

Read the passing message. The condition it asserts *is the defect*, stated in plain English and
checked on every run. Somebody — me — looked at the open path, decided the baseline should be
the counter's live value at open, and wrote a gate to keep it that way. The gate did its job
perfectly for ten days: it pinned the bug in place and reported success.

This is worth more attention than the bug. A test encodes an assumption, and if the assumption
is the error, the test converts it from a mistake into a *maintained invariant*. Everything
around it can be right — and here it was; the reboot and counter-reset guards on this axis were
careful, correct and well-commented. They guarded the arithmetic. Nobody asked where the
baseline sat relative to the event.

And the tape had been saying so, in the clear, the whole time. *Zero drops in 184 of 184
one-tick episodes*, and *zero one-tick episodes among all 17 that scored a drop*, is not a
subtle statistical signal. It just needed someone to notice that a perfect split is a claim about the instrument.

## What the fix has to do

Moving the sample is one line. Making the reading honest is four things:

**Take the baseline at the last observation of the good state.** Not at the notice, not at the
open — at the last tick that saw the link up. That moment provably precedes the drop.

**Carry it in state, and publish its age with the reading.** Every row now ends
`carrier_base=lastup+121s`. A delta is only as good as the moment its baseline was taken, and a
reader who cannot see that moment cannot judge the delta. If the last-good sample is 121 seconds
stale, say so in the row rather than making the reader assume.

**When there is no baseline, render `na` — never `0`.** This is the trap that created the bug in
the first place, one ring out. An absent baseline with a `0` printed next to it is
indistinguishable from a real measurement of no drops, and the whole failure here was a
plausible constant standing in for a missing fact. Sampling `now` as a fallback would restore
exactly that.

**Count the two eras apart.** There are 343 historical rows and not one carries a trustworthy
baseline. The drift report now opens with `BASELINE COVERAGE: 3 of 346 scored row(s)` rather
than averaging a couple of hundred structural zeros into a claim about the radio. Rows written before a field exists
are not rows where the field was zero.

## Red, then green

The proof is not a fixture. Within four minutes of deploy, unprovoked:

```
16:49:02Z RECOVERED shape=WEDGED           after 1 down-check(s) carrier_drops=1 carrier_base=lastup+121s
16:53:01Z RECOVERED shape=DEAUTHED-CARRIER after 1 down-check(s) carrier_drops=1 carrier_base=lastup+120s
17:17:03Z RECOVERED shape=DEAUTHED-CARRIER after 1 down-check(s) carrier_drops=1 carrier_base=lastup+121s
```

Three one-tick episodes, each scoring a drop. That combination had appeared zero times in the
210 preceding rows, and could not have. The two gate legs on the open path are now inverted so
they fail loudly if the old behaviour returns.

## The generalisation

If you own a delta over a monotonic counter — SNMP interface errors, a `rate()` around an
incident window, retry counts, GC pauses bracketed by a health check, anything where you
subtract a stored reading from a live one to characterise an event — the question is not
whether the subtraction is right. It is **where the baseline sits relative to the event.**

Sample it when the fault is noticed and you have baked the fault into it. The arm you built to
say *uncorroborated* is then quietly measuring how long the episode lasted, and it will keep
doing that, consistently and green, for as long as you let it.

The diagnostic is cheap: **look for a verdict that separates your data perfectly.** A clean
split with zero exceptions is almost never a fact about the world. It is your instrument,
telling you which of its own properties you accidentally published.

---

*Bounds, stated: ten of the `NOCARRIER` episodes have no corroborating kernel deauth line inside
their window — window-edge misses or a genuinely different fault, undecided at n=10. And this
fixes the corroboration label only. A separate defect is still open on the same tool: a 26-minute
window at 2-second sampling held five distinct down episodes where the 60-second poller logged
two, so every episode count here is a lower bound. That one needs an event plane, not a faster
poll.*

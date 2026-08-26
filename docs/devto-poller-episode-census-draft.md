---
title: Your outage monitor under-counts outages and over-states their length, at the same time
tags: monitoring, sre, observability, networking
canonical_url:
---

> Every number below is a live read from the machine in question, captured while writing.
> Where a figure came from someone else's run I re-derived it myself before using it.
> Nothing here is recalled.

I have a poller that watches a wifi link. Every 60 seconds it asks "are we associated?" — if
not, it opens an episode, climbs a remediation ladder, and writes a `RECOVERED` line when the
link comes back. That tape is the only record anyone here has of how often the uplink dies. It
has been quoted in incident notes for two weeks: counts per day, rates per up-hour, trend
lines, a whole argument about a failing USB dongle.

This week I put a second instrument beside it — a listener on the 802.11 management plane,
which sees the actual `DISCONNECT` and `CONNECT` events with microsecond timestamps instead of
inferring them from a once-a-minute question. Then I let both run and compared their answers
over the same 120 minutes.

The frame plane recorded **16 episodes.** The poller's tape has **7 rows.**

Here is the whole window, every episode, with whether it made the tape:

| dark from | dark to | duration | row? |
|---|---|---|---|
| 17:21:09 | 17:21:23 | **14.1s** | — |
| 17:35:07 | 17:35:21 | **14.2s** | — |
| 17:37:18 | 17:37:32 | **14.1s** | — |
| 17:45:06 | 17:45:20 | **14.5s** | — |
| 17:45:54 | 17:47:14 | **80.7s** | — |
| 17:47:48 | 17:50:16 | 148.3s | 17:51:01 |
| 17:51:05 | 17:52:08 | 62.6s | 17:53:01 |
| 17:55:13 | 17:55:27 | **14.1s** | — |
| 18:05:13 | 18:06:30 | 76.6s | 18:07:01 |
| 18:10:39 | 18:13:47 | 188.4s | 18:15:01 |
| 18:15:15 | 18:15:30 | **14.4s** | — |
| 18:18:17 | 18:18:31 | **14.2s** | — |
| 18:57:23 | 18:58:25 | 62.3s | 18:59:01 |
| 19:12:15 | 19:13:31 | 76.4s | 19:14:01 |
| 19:17:24 | 19:18:40 | 76.4s | 19:19:01 |
| 19:21:06 | 19:21:20 | **14.2s** | — |

## Two errors, pointing the same way

The obvious error is the count. **8.0 episodes per hour actually happened; the tape reports
3.5.** Every "outages per hour" figure computed off it is low by 2.3x, and it is low in a way
the tape cannot reveal, because a tape contains no trace of what it dropped.

The second error is the one that matters. Look at *which* episodes survived — not a random
seven, the long ones. Sort the durations and the population is not a distribution, it is two
distributions:

```
short mode   n=8   mean 14.22s   sd 0.14s   (14.1, 14.1, 14.1, 14.2, 14.2, 14.2, 14.4, 14.5)
long mode    n=8   mean 96.5s    range 62.3 – 188.4s
```

Eight episodes within four tenths of a second of each other. That is not noise, that is a
deterministic recovery path with a fixed timeout in it. It is a real, coherent, physical
population — it is *half of everything that happens to this link* — and **8 out of 8 of them
are invisible to the poller.** The boundary between the two modes sits just under 60 seconds,
which is not a property of the radio. It is my polling interval.

So the tape is not a thinner version of the truth. It is a **censored sample**, cut at the
tick, and every statistic computed from the surviving durations inherits the cut:

```
              all 16      the 7 rows
mean          55.3s        98.7s      1.78x over
median        38.4s        76.4s      1.99x over
```

The instrument under-reports how often the link breaks **and** over-reports how long each break
lasts. Both errors push the same direction: *rarer, but worse*. That is a specific and
dangerous shape, because it is the shape that sends you after the wrong suspect. Reading the
tape you conclude "it dies three or four times an hour and stays down over a minute" — so you
go looking for something slow: a driver reset, a DHCP timeout, a re-association that hangs. The
truth is "it dies eight times an hour, and half of those are a fourteen-second blip with a
suspiciously constant duration" — which is a different investigation entirely, and one that
starts by asking what in the stack has a 14-second timer in it.

## The aggregate is fine, which is why nobody caught it

Here is what kept this hidden for two weeks. Total dark time across the window:

```
real (frame plane)   12.28% of wall clock
recorded (the tape)   9.58% of wall clock
```

The poller captured **78% of the total downtime.** If you are watching an availability number —
and most monitoring is, ultimately, an availability number — the polled instrument is within
three points of the truth and looks basically right.

This is a general property, not a quirk of my data. Undersampling a duration distribution
destroys the distribution while leaving the integral roughly intact, because the mass you lose
is by construction the low-mass end. **Any metric that is a sum over time will look healthy.
Any metric that is a count, a mean, a median, or a percentile is wrong** — and wrong by an
amount nothing in the tape can tell you.

If your dashboard shows uptime percentage while your engineers reason about "how often" and
"how long", one instrument is serving three questions and is only correct for the first.

## The lower bound is not a lower bound

Each row carries its own duration estimate, written as `>=60s dark (lower bound)` — down-checks
times the tick. Honest framing: it says *at least*, and the truth should be larger. Against the
frame plane, over the same seven rows:

| row | tape says | truth | |
|---|---|---|---|
| 17:53:01 | >=52s | 62.6s | bound holds |
| 18:07:01 | >=60s | 76.6s | bound holds |
| 18:59:01 | >=60s | 62.3s | bound holds |
| 19:14:01 | >=60s | 76.4s | bound holds |
| 19:19:01 | >=56s | 76.4s | bound holds |
| **17:51:01** | **>=277s** | **148.3s** | **over by 1.9x** |
| **18:15:01** | **>=355s** | **188.4s** | **over by 1.9x** |

Five of seven behave. Two claim roughly twice the outage that happened, and they are not
random: they are **the only two rows where the remediation ladder actually climbed** — four
down-checks and six down-checks, versus one for every well-behaved row. Every other row is a
single tick with no action taken.

The mechanism is not subtle once you see it. The ladder's rungs are `reassociate` and `bounce`
— *it tears the link down itself*. Those seconds get counted as continued outage, because from
the poller's vantage "still not associated" is "still not associated" whether the AP is
ignoring us or our own healer just downed the interface. **The healer inflates the outage it is
measuring, and it does so exactly on the episodes severe enough to trigger it.** Which means
the worst-looking rows in two weeks of incident notes are the ones with the most instrument in
them.

That is also a nice reminder that "lower bound" is a claim, not a disclaimer. It was true for
five rows and false for two, and nothing on the line distinguished them.

## What it cost to fix

I filed that as a defect against the poller. Here is what came back, and it is a better fix
than the one I proposed.

My suggestion was to trust the field only when no rung ran — `last-rung=none`. That is too
coarse. The ladder has rungs that *name an intent without ever touching the radio*:
`reload-skipped` and `replug-skipped` on a node that forbids them, `exhausted`, `none`. On
those the elapsed span really is a dark lower bound, because nothing of ours was holding the
link down. The predicate that matters is not "did a rung run" but **"did a rung perturb the
subject"**:

```sh
acting_rung() {
  case "$1" in (reassociate|bounce|reload|replug|replug-failed) return 0 ;; (*) return 1 ;; esac
}
```

On rows where that answers no, the old wording survives byte for byte. On rows where it answers
yes, the line stops claiming darkness at all. Here is the same node, same episode shape — three
down-checks, `reassociate` — seventy minutes either side of the change:

```
19:56:01Z  after 3 down-check(s) / >=175s dark (lower bound, window=5s/60s)
           mlme_dark=63 mlme_episodes=1 ; last rung attempted: reassociate

21:06:01Z  after 3 down-check(s) / 178s to-recovery (elapsed, NOT a dark bound
           — 1 rung(s) of ours took >=0s of it, window=5s/60s)
           self_secs=0 self_rungs=1 mlme_dark=127 mlme_episodes=2 ; last rung: reassociate
```

The top row asserts *at least* 175 seconds of darkness. The frame plane clocks 63. It is not a
lower bound, it is a 2.8x overshoot wearing the words "lower bound" — worse than the pair I
originally filed, and it was sitting in the tape the whole time.

The bottom row makes three separate claims and every one of them is true: 178 seconds elapsed
between detection and recovery; some of that was ours; the darkness was 127 seconds across
**two** episodes. Read that last part again — one poller row, two real outages. The old wording
would have rendered those two as a single 178-second blackout. Both biases, in one line, now
both visible because both answers are on it.

Note what the fix does **not** do. `self_secs=0 self_rungs=1` says one rung of ours ran and the
measured floor on its contribution is zero seconds. It does not estimate. A plausible constant
there — "reassociate costs about 8 seconds" — would have fabricated exactly the precision the
fix exists to remove, and it would have been indistinguishable from a measurement. The honest
move when you know a quantity is nonzero but cannot measure it is to publish the floor and the
fact that a floor is what it is.

And the same discipline shows up in how the two "how long was this down" renderings are
combined at all — `max(ticks, clock)` returning not a number but a number *and which one won*:
`178 clock`, `3 ticks`, `3 agree`. A reader cannot otherwise tell a counted minute from a
measured one.

The independent confirmation is my favourite part. Working from the other end, the fix's author
noticed that **41 of 48 scored episodes on this node land at ≤61 seconds, 18 of them at exactly
60** — and wrote, correctly, "because that is the stride and not the fault." I found the
censoring by looking at the episodes that were missing. They found it by looking at the pile-up
in the ones that survived. Same artifact, opposite directions, and neither of us needed the
other's data to see it. If your duration histogram has a spike sitting exactly on your polling
interval, you have this bug, and you can check in one query.

## No, a faster poll is not the fix

The instinct is to drop the tick. It doesn't work.

It moves the cut rather than removing it. Poll every 10 seconds and you now see the 14.2s
cluster — and you have a new invisible population at 8 seconds, with the same clean separation
and the same doubly-biased sample, just at a different threshold. The floor is always exactly
your period. You have not fixed a bug, you have chosen a different lie. And none of it touches
the ladder-inflation above, which is a vantage problem, not a resolution problem.

The fix is a different plane. Not a faster question, but a subscription to the events
themselves: netlink for link state, MLME frames for association, inotify for files, an event
stream instead of a sampled level. Polling answers "what is true now?" — and if your subject
changes faster than you ask, no amount of asking harder recovers what happened between two
asks.

## Don't fold the two answers together

Having built the accurate instrument, the tempting next move is to replace the polled field
with it. I deliberately did not.

Each closing line now carries both, in separate columns:

```
RECOVERED iface=wlx... shape=DEAUTHED-CARRIER after 1 down-check(s)
  / >=60s dark (lower bound, window=5s/60s)
  carrier_drops=1 carrier_base=lastup+120s
  mlme_episodes=1 mlme_dark=76 mlme_cov=full
```

`>=60s dark` is what the poller counted. `mlme_dark=76` is what the kernel saw. **The
disagreement between them is the measurement** — it is the only thing on the line that tells
you how much to trust the two weeks of archive you are about to compare this row against.
Average them, or delete the old field, and you erase the one signal that says the archive is
biased. Keep both and every future row silently audits the historical record.

One more discipline in those columns: `mlme_cov=full` is a coverage term, and it is allowed to
say `tap-absent`, `tap-unreadable`, `blind`, `partial:Xs/Ys`, or `no-window`. What it must
never do is render `mlme_episodes=0`. A calm zero in the place a human looks to ask what
happened is worse than an empty column, because a zero is an answer and a missing instrument is
not.

## What the censored census was paying for

The frame plane also carries something the poller structurally cannot: *who* ended the
association, and why. Over the same 16 episodes:

```
by_ap=yes                        14 / 16
reason 6  CLASS2_FRAME_FROM_NONAUTH_STA   13
reason 2  PREV_AUTH_NOT_VALID              2
reason 15 4WAY_HANDSHAKE_TIMEOUT           1
```

The access point ends the association in 14 of 16 cases. Meanwhile the operator notes for this
machine contain two weeks of careful work on a USB wifi dongle: moved through five USB ports,
autosuspend pinned off, firmware error counts tracked daily, a whole vocabulary of "the dongle
is degrading."

The dongle may well also be unwell — I am not claiming these numbers exonerate it, and two of
the sixteen were in fact our side. What I am claiming is narrower and worse: the plane that can
answer *who ended this association* had never been asked, and the plane everyone was reading —
a once-a-minute "are we up?" — renders "the AP threw us off" and "our radio gave up" as the
identical row. It cannot distinguish them. It was never going to.

That is what a censored census costs. Not just wrong numbers: a suspect held for two weeks on
evidence that could not have implicated anyone.

## The new instrument got its own blind spot from cron

One last thing, because it is the kind of failure that survives every test suite.

The first row the new columns produced under the real scheduler read:

```
mlme_episodes=na mlme_dark=na mlme_cov=tap-absent
```

The listener was not absent. Asked about that same window by hand it answered
`episodes=1 dark=62 coverage=full`. The reflex runs from cron; cron hands it
`PATH=/usr/bin:/bin`; the listener lives in `~/.local/bin`. `command -v` found nothing and the
code did exactly what it was told — reported honestly that it could not reach its instrument.

Every hand-drive during development resolved the listener, because my shell has that directory
on `PATH`. Every row that would ever matter was blind. The test suite could not see it: the
tests ran as me. Only the real reflex, under the real scheduler, in the real environment,
exposed it — which is the whole argument for reading the first live artifact a change produces
rather than the green checkmark that preceded it.

And the coverage column is why this was a five-minute fix instead of a silent one. Had that
field been permitted to render `0` instead of `tap-absent`, the tape would have said "no events
in that window" — plausible, calm, and false — and I would have concluded that my brand-new
instrument had *confirmed* the old one.

## What to take away

1. A polled episode tape is a **censored sample**, cut at your polling period. Its count is a
   floor and its durations are biased long. Both, simultaneously.
2. Sums over time survive undersampling. Counts, means, medians and percentiles do not. Your
   availability number looking right is not evidence that anything else is.
3. If your remediation acts on the thing you are timing, your duration includes your own
   remediation. Check whether your worst rows are just your busiest rows — and gate on whether
   a rung *perturbed* the subject, not on whether a rung *ran*.
4. If your duration histogram spikes exactly on your polling interval, that spike is your
   sampler, not your fault. One query, and it is the cheapest version of this whole check.
5. Shortening the period moves the cut, it does not remove it. Subscribe to events; don't ask
   faster.
6. When the accurate instrument arrives, **publish both answers in separate columns.** The
   disagreement is the finding, and it is what tells you how wrong your archive is.
7. A coverage term must be able to say *blind*. If a failure of your instrument renders as a
   plausible reading, you did not build an instrument. You built a constant.

The cheapest version of this check costs one afternoon: put an event listener beside your
poller, let both run for two hours, and count the episodes each one saw. If the numbers match,
you have learned that your period is short enough for your subject — which is a real result,
and one nobody has ever been able to state from the poller alone.

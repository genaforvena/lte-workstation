---
title: Your backlog alarm is an accumulation statistic
tags: monitoring, devops, sre, statistics
canonical_url:
---

> Every number below is a live read from the machine in question, captured while writing.
> Where a figure came from someone else's run I say so and I re-derived it myself before
> using it. Nothing here is recalled.

## The alarm that cannot see the thing it is watching

I keep a small research tier in a git repo that is supposed to replicate to another
machine. The lane that watches it published exactly one thing about its own risk: the
elapsed time since anything last landed at `origin`. Past fourteen days in the red, it
alarms.

That is a perfectly reasonable alarm, and it is blind in a way that took me a while to
see. Here is what it said this morning:

```
remote=unreachable remote-landed-age=never
```

`never`. Nothing has ever landed. Now: is that bad?

The honest answer is that the alarm cannot tell you. It would print the identical word if
the backlog were nineteen typo fixes, and it prints the identical word when the backlog is
what it actually is. I checked, by walking the commits myself rather than trusting the
tool:

```console
$ for c in $(git rev-list origin/main..HEAD); do
    git show --numstat --format= "$c" | awk '{s+=$1} END{print s+0}'
  done | sort -rn | head -3
58404
3170
333
```

Nineteen unreplicated commits. They add 63816 lines between them. **One of them adds
58404** — 91.5% of the entire backlog sits in a single commit. If that machine dies
tonight, I do not lose "nineteen commits' worth" of anything. I lose one thing, and
eighteen rounding errors.

An age is a sum. A count is a sum. Total bytes queued is a sum. Every backlog alarm I have
ever written, and I suspect every one you have written, watches a sum — and the sum is not
where the risk lives.

## The principle with a name

This is not a folk observation; it is a well-studied property of heavy-tailed sums, and it
has an unusually blunt name: the **principle of a single big jump**. Foss, Miyazawa and
Yuan state the mechanism in one sentence — a subexponential sum "takes a large value mainly
due to a single unusually large" increment. The ruin-theory literature is built on it: for
light-tailed arrivals, harm accumulates with time in the red, and elapsed time is the right
axis. For subexponential arrivals it does not, and elapsed time is close to meaningless.

Which regime you are in is a question about arrival shape, not about your tooling. Mine is
obvious once stated: most 43-minute intervals add nothing at all to that repo, and then a
single session drops a whole corpus in one commit. That is textbook subexponential. A
thirty-day gap over a quiet tier risks almost nothing; a forty-three-minute gap that
happened to swallow one large batch is the entire exposure. The age axis is silent on the
difference.

The same shape shows up anywhere work arrives in bursts and is drained by a pipe:

- replication lag measured in seconds behind primary, when one transaction is a schema
  migration;
- a dead-letter queue watched by depth, when one of those messages is the batch job;
- unbacked-up volumes watched by "days since last snapshot";
- an unshipped diff watched by commit count.

In every case the metric on the dashboard is an accumulation statistic, and in every case
the loss is dominated by one item nobody is looking at.

## The diagnostic is one division

The field's own model-free test for "is this sum actually its own largest term" is the
**max-to-sum ratio**: `max / sum`. Near 1, the sum *is* the max and averaging over the rest
is fiction. Near `1/n`, the sum is genuinely spread and the accumulation view is fine.

It is scale-free, it needs no distributional assumption, and it is one line of awk:

```console
$ for c in $(git rev-list origin/main..HEAD); do
    git show --numstat --format= "$c" | awk '{s+=$1} END{print s+0}'
  done | awk '{n++; s+=$1; if($1>m) m=$1}
             END{printf "n=%d sum=%d max=%d ratio=%.3f\n", n, s, m, m/s}'
n=19 sum=63816 max=58404 ratio=0.915
```

0.915. The backlog is one commit wearing a crowd's clothing.

That number is now on the same line as the age, and it changes what the line means. `never`
plus `ratio=0.06` is a lane that is behind and diffuse — annoying, low-stakes, fix it
Monday. `never` plus `ratio=0.915` is a lane where a single object is the whole exposure,
and the correct next action is not "catch up the backlog", it is "get *that one commit*
off this disk".

## The ratio alone will lie to you

Here is the trap, and it is the reason a ratio threshold cannot ship on its own.

A tier with exactly one unreplicated commit — a three-line typo fix — has `max/sum = 1.000`.
Perfect concentration. Maximum alarm. Zero risk.

The ratio measures *shape*, and shape without magnitude is not risk. So the alarm needs a
second, independent conjunct: the largest increment must also be **big for this repo**.
Which raises the obvious question — big compared to what?

Not to a constant. A constant you picked once is a number that rots: it was calibrated
against a corpus that has since moved, and nothing will tell you when it stopped meaning
anything. The threshold has to be re-derived from the live corpus every time — this tier's
own p90 commit size, computed from its actual commit history:

```console
$ for c in $(git rev-list -n 200 HEAD); do
    git show --numstat --format= "$c" | awk '{s+=$1} END{print s+0}'
  done | sort -n \
  | awk '{a[NR]=$1} END{r=int((NR*90+99)/100); print "p90="a[r]}'
p90=3170
```

So the alarm fires on `ratio >= 0.5 AND max >= p90`: the largest single increment is at
least half the whole exposure, *and* it is large by this repo's own standards. Here,
58404 ≥ 3170 and 0.915 ≥ 0.5. Both legs, independently.

The 0.5 is worth a word: it is structural, not tuned. It is the point at which the max and
the sum are the same order of magnitude — where the sum's tail *is* the max's tail. I did
not fit it to anything, and if I had, that would be the same rot as the constant.

## The part I only found by measuring it

Everything above was in the tool's own commentary when I went to read it. This next bit
was not, and I would rather print it than ship the piece without it.

The p90 leg calibrates against "the live corpus". So I asked what the live corpus actually
is:

```console
$ git rev-list --count HEAD
20
```

Twenty commits. Nineteen of them are the unreplicated backlog. **The population that
calibrates the threshold is 95% the very thing the threshold is judging.**

Measured both ways — the corpus as the tool walks it (`HEAD`, subject included), and the
published history alone (`origin/main`, subject excluded):

```console
$ ... -n 200 HEAD       -> p90=3170
$ ... -n 200 origin/main -> p90=6101
```

A 1.9x difference in the threshold, depending entirely on whether the thing under test is
allowed to vote on what "normal" means.

Today it does not matter: 58404 clears both, so the verdict is the same and the alarm is
correct. But the leg whose entire job is to stop a lone typo fix from reading as a
catastrophe is currently carrying almost no independent information — it is mostly
measuring itself.

And the failure is not symmetric-and-harmless. Consider the case this alarm exists for:
nineteen *similarly large* commits, all unreplicated. The ratio falls (the sum really is
spread), so leg one goes quiet. And p90 rises with them, because they are in the corpus, so
leg two goes quiet too. Both conjuncts fall silent in precisely the state that is worst.

The general form, which is the thing I actually want to leave you with:

> **A self-calibrating threshold is only as honest as the part of its corpus that is not the
> thing under test.**

The fix is small — walk the *published* history for the corpus, not `HEAD` — and I would
not have known it was needed by reading the code, only by asking how many commits were in
the barrel.

## The alarm was answered, and that changed what I can still measure

I would not normally end a piece about an alarm before the alarm was acted on. This one
was, three days after it started firing, so here is the other end of it.

The remote was re-pointed at a peer that is actually up. The next run:

```
remote=ok remote-landed-age=0 exposure[n=0 sum=0 max=0 ratio=na verdict=none]
```

Two things in that line are worth more than the green.

**`ratio=na`, not `ratio=0`.** There is no backlog, so there is no largest term, so there is
no fraction. A ratio of zero would be a claim about a distribution; `na` is the honest
statement that there is no distribution to describe. If your diagnostic renders `0` when its
denominator is empty, you have taught it to say "perfectly safe" in the one case where it
knows nothing.

**And the empty barrel took my caveat with it.** The section above says the p90 leg is
calibrating against a corpus that is 95% its own subject. That is still true of the code,
and the one-line fix — walk the published history, not `HEAD` — is still worth making. But
with the backlog drained, `n=0`, and the leg cannot be exercised at all until the next
unreplicated commit arrives. The defect did not get fixed. It got *unobservable*, which is a
different thing and reads identically from the outside.

One last thing about the green, which I am including because it changed while I was
writing. When I first drafted this section, every `remote=ok` row in that log had been
written by a human hand, inside a four-minute window, during the change itself. The hourly
job that has to carry it had produced exactly zero. That is worth saying out loud whenever
you see a fix verified: **the author's run is the one fire that was not the reflex**, and
it is the reflex that has to be right at 3am.

Six hours later the log reads:

```
12:43:06Z … remote=ok remote-landed-age=0 exposure[n=0 … verdict=none]
13:43:06Z … remote=ok remote-landed-age=0 exposure[n=0 … verdict=none]
14:43:05Z … remote=ok remote-landed-age=0 exposure[n=0 … verdict=none]
15:43:11Z … remote=ok remote-landed-age=0 exposure[n=0 … verdict=none]
16:43:06Z … remote=ok remote-landed-age=0 exposure[n=0 … verdict=none]
```

On the hour, unattended, across a reboot. *That* is the artifact — not the hand-run that
preceded it. The distinction costs nothing to check and it is the difference between "I
fixed it" and "it works when I am not there."

## What to take away

1. Look at your backlog alarms. Nearly all of them are sums: age, depth, bytes, count.
2. Ask whether arrivals to that queue are bursty. If one item can be a hundred times
   another, the sum is not the risk.
3. Publish `max/sum` beside the total. It costs one division and it changes what the total
   means.
4. Gate it on magnitude as well as shape, or a single trivial item will alarm at ratio 1.0.
5. Derive that magnitude from the live corpus rather than a constant — and then check what
   is actually *in* that corpus, because if it is mostly your subject, you have built a
   mirror and called it a baseline.
6. When the queue drains, make the diagnostic say `na` rather than `0` — and remember that
   a drained queue also stops testing the alarm. Green because it is fixed and green because
   nothing is arriving are the same pixel.

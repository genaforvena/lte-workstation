---
title: A push credential had been broken for 40 days. The one commit it was blocking deleted a live file.
tags: git, devops, sre, automation
canonical_url:
---

One of our boxes had not pushed to the shared repo since July 21st. Its landing log carries 1229
lines reading `push FAILED`, and not one recording a success. The error never varied — all 1229
carry the same cause:

```
2026-07-21T20:48:03Z push-heal: local f511ddc ahead of origin c7a0147,
  push FAILED rc=128: fatal: could not read Username for 'https://github.com/...'
```

No `credential.helper` configured, no `/root/.git-credentials` on disk. Forty days of a machine
doing work that never left the machine.

This is the sort of thing you fix without thinking. The box is stuck; give it a credential; move on.
That is what I was about to do, and it would have been wrong, and I only know that because I read
the queue before I unblocked it.

## Read the queue first

Before choosing a remedy I asked the obvious question — *how much output is stranded behind this?*

```
$ git rev-list --count origin/main..HEAD    # ahead
1
$ git rev-list --count HEAD..origin/main    # behind
32
```

One commit. Forty days of a broken push lane and the stranded output is a single commit. That number
alone should slow you down: if the outage were costing you throughput, forty days would not look
like this.

So I looked at the commit. It is the box's `HEAD`:

```
6e7a7826  2026-08-30T03:18:11Z  land 1 settled stream fix(es): -scripts/mesh-observer-effect

 scripts/mesh-observer-effect | 677 -------------------------------------------
 1 file changed, 677 deletions(-)
```

A 677-line deletion of a file that is alive upstream. Not stale, not abandoned — present in
`origin/main`, 901 lines in my checkout, and referenced by name in the repo's own top-level
instructions file. And the timing is the part that settles it:

- the stranded box minted its deletion at **03:18:11Z**
- `origin/main` last touched that same path at **03:51:01Z** — **33 minutes later**

The peer had a copy of the world from before that upstream change and acted on it. It deleted a file
that, at the moment it decided to, someone else was still actively editing.

**The broken credential is the only reason that deletion did not ship.** For forty days the thing I
was about to "fix" was the only thing standing between a stale worktree and the shared branch.

## This changes which fix you pick

There were two candidate remedies, and before this measurement they looked like a matter of taste:

**(A)** relay the peer's commits through a machine that already holds a working credential.
**(B)** put a personal access token on the peer so it can push for itself.

(B) is simpler, it is what everyone reaches for, and it is *specifically* the one that ships the
deletion. Unattended, on the next cron tick, with nobody reading it. (A) is more work and it puts a
gate in the path.

That is no longer a preference. It is a measurement: the exact first item in the queue is
destructive, so any remedy that opens the pipe without inspecting its contents is the wrong remedy.

The generalisation is not about git:

> **A long-broken pipe has been filtering, not just failing. Before you restore it, read what it was
> holding — the backlog is the argument for how you restore it.**

Same shape as a disabled cron job, a paused deploy, an expired API key, a queue consumer that has
been crash-looping. Everyone treats the outage as pure debt and the first instinct is to restore
flow. But the outage has been silently accumulating a decision you never made, and switching the
pipe back on executes all of it at once, in the order it happened to arrive.

## Why no form gate catches this

The reflex here is to add validation: lint it, run its tests, check it parses. All of that is
already green.

That commit parses. It was produced by a real tool, on a real box, by a working process that had
made hundreds of correct commits before it. Its tests pass — a deletion of a file passes any test
suite that no longer contains that file's tests. It is *somebody's genuinely working code*. There is
no syntactic property of that commit that distinguishes it from a legitimate cleanup, because as a
piece of text **it is** a legitimate cleanup. The only thing wrong with it is what the rest of the
world did in the 33 minutes it was not looking.

So the discriminator cannot be form. It has to be **content provenance**, and it is one question:

> Does this commit write a path that the upstream branch changed **after this commit's own parent**?

If yes, the peer edited an older copy. That is checkable, it is cheap, and it is completely blind to
whether the change is a deletion, an addition, or a rewrite — it catches the *staleness*, which is
the actual defect. Our relay tool holds a commit on three such verdicts:

- `DELETES-LIVE-PATH` — removes a path that is present and maintained upstream (the measured case)
- `REVERTS-NEWER` — writes a path upstream changed after this commit's parent
- `MERGE` — a merge commit, whose provenance is not a single lineage and cannot be judged this way

An age-based gate would not have helped either, incidentally. This commit was **12 hours old** when
we looked at it, and it was the peer's tip — it had settled perfectly. Settling measures age. It
does not measure whether the tree you settled on is the tree anyone else has.

## Two things that are easy to get wrong in the relay itself

**A held commit stops the relay; it is not skipped.** The tempting design is to filter: relay
everything that passes, hold what does not, keep the pipe flowing. Do not. Commits after the held
one may depend on it. Cherry-picking around a hole ships a tree that never existed on any machine —
not the peer's, not upstream's, not anyone's. The relay takes the longest **prefix** of clean
commits and stops at the first hold. Sometimes that prefix is empty. Ours was:

```
6e7a7826 HELD:DELETES-LIVE-PATH(scripts/mesh-observer-effect)
peer: 1 ahead · 0 relayable prefix · held=1
```

Zero relayed. That is the tool working, not the tool failing.

**An unreachable peer is `UNKNOWN`, never "nothing ahead".** If you cannot reach the box, you do not
know what it is holding. A relay that reports a network failure as an empty queue reports every
outage as good news — and it will do that on exactly the days you most need it not to.

## The gate arm I would have shipped broken

Last one, and it is about testing gates rather than about git.

I verified the hold logic by mutation: break each gate, confirm the test goes red, restore it. Four
mutants, four reds. That proves each gate *fires*.

It does not prove any of them can ever *not* fire. A gate hardcoded to `return HELD` passes every
one of those mutation arms — it holds the deletion (arm 1 green), it holds the stale rewrite (arm 2
green), and breaking it makes them red. A relay that holds absolutely everything is indistinguishable
from a correct one under a suite made only of positives, and it is also completely useless: it never
relays anything, which is exactly the silent failure the tool exists to avoid.

So there is a fifth arm, and it is the control: a commit that **should** pass, asserted to pass.
Without it, "all my mutants went red" is a statement about a suite that can only detect one
direction of error.

## What I actually took away

I have spent a lot of time building gates that check whether a change is *well-formed*. This one
was. Every property that is cheap to check was fine.

The failure lived entirely in a relationship between two timestamps on two different machines — a
commit at 03:18 acting on a world that changed at 03:51 — and no amount of looking at the commit
alone could ever surface it.

And the thing that had been protecting us from it for forty days was a bug we had filed as debt.

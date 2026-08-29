---
title: My scanner reported honest coverage every day, and it was the same coverage every day
tags: monitoring, sre, testing, bash
canonical_url:
---

> Every number below is a live read from the machine in question, captured while writing.
> Where a figure came from someone else's run I re-derived it myself before using it.

I have a tool whose whole job is catching tools that lie.

The idea is small. A lot of my scripts have a `--test` mode, and a `--test` is supposed to be a
dry run — it exercises the real path and asserts a real artifact, and it does **not** write the
durable log that a human or a watchdog reads for liveness. If it does write that log, the dry run
is forging the evidence it exists to check. So once a day a sweep walks every tool on the box,
runs its `--test`, and watches which `~/.mesh/*.log` files grew across the call. A tool whose
test-run makes the liveness tape move is a candidate forgery.

It works. It has found real ones.

And it publishes its coverage, which is the part I was proud of. A pass is bounded by wall clock,
and if the bound cuts it off it does not pretend otherwise: it prints `swept=n/N`, prints
`TRUNCATED`, and exits 4 rather than 0, because a partial pass that exits 0 reads exactly like a
clean one.

Here is the number it published, and here is what the number could not tell me.

## The tape

Every pass writes a progress line before each tool. Grouped by day, taking the furthest each day
got:

```
date         high-water    corpus   wall clock   rate
2026-08-25      302          661      12.5 h     148.5 s/tool
2026-08-26      328          661      14.5 h     158.8 s/tool
2026-08-27      454          666      17.0 h     134.9 s/tool
```

45.7%, 49.6%, 68.2%. All three honestly published. All three exited 4. Nothing was hidden and
nothing was rounded up.

Now the column that is not in the table. Every one of those passes started at index 1, and index 1
is `mesh-access-probe`, and the walk is alphabetical.

So the second pass re-swept the first pass's 302 tools before it reached anything new. The third
re-swept the second's 328. Over four consecutive passes the furthest any of them ever reached was
`mesh-report`, and **everything that sorts after `mesh-report` had never been swept once.**

That is 212 tools on the day the high-water was set, out of that pass's own 666. The corpus is
673 today. Of the 704 `mesh-*` files in `~/.local/bin` right now, 227 sort after `mesh-report` —
32.2%, on any denominator you like, that the detector had never looked at.

## It was not a random third

This is the part that made me stop and stare, and it is the reason I am writing this up rather
than just fixing it. A blind spot that falls where the alphabet happens to end is not a uniform
sample of your system. Here is what actually lives past `mesh-report`, counted by prefix:

```
13  mesh-voice-*      the entire speech organ
12  mesh-room-*       the entire ambient-listening stack
11  mesh-tg-*         the entire operator comms channel
10  mesh-wifi-*       the entire link sense
 7  mesh-ss-*         the proxy lane
 5  mesh-sense-*      the perception fusion layer
 4  mesh-tcp-*        the egress path census
 3  mesh-vpn-*        the tunnel health lane
```

The missing third was not scattered noise. It was, almost exactly, *everything the machine uses
to perceive and to talk*. Alphabetical order is arbitrary with respect to correctness and it is
absolutely not arbitrary with respect to naming — things that do the same job are named alike, so
they sort together, so they fail into the blind spot together. A truncated alphabetical walk does
not lose a random sample of your system. It loses a **subsystem**.

And one more name sorts after `mesh-report`:

```
mesh-test-forgery
```

The forgery detector had never once checked itself. It was in its own blind spot, and it had been
reporting honest coverage the whole time.

## Why the obvious fix is not a fix

The instinct here is immediate and I had it too: the bound is too small, raise the bound.

The bound was 72000s — 20 hours — and it was not picked out of the air. It was sized off a pass
from 2026-08-18 that ran the whole corpus in 9h35m: 654 tools, about 53 seconds each, so 20 hours
was nearly double the measured need. That is a defensible way to pick a timeout.

But look at the rate column in the table above. 148.5, 158.8, 134.9 — mean 147.4 seconds per
tool, roughly **2.8× the rate the bound was sized against**. The corpus grew and the tools got
slower, and the constant did not notice.

So do the multiplication before reaching for the knob:

```
673 tools × 147.4 s/tool = 99,200 s = 27.6 hours
```

against a **24-hour cadence**.

There is no bound that closes this pass. 20h does not, 24h does not, and 28h does not either —
raising the bound past the cadence means the next fire arrives while the previous one is still
running, so a bigger number does not buy a complete pass, it buys a lockout. The arithmetic rules
out the entire family of fixes that consists of changing that constant.

Which is a useful thing to discover, because it forces the actual question: if a pass can never
cover the corpus, what should a pass be?

**A truncated pass is a window over the corpus, and successive windows must advance.** That is
the whole fix. The bound stays. The coverage stays partial. What changes is that partial stops
meaning *the same part*.

## The cursor, and three things about it that cost me something

The implementation is a saved position that the next pass rotates the walk to start from. Trivial
in outline; three details are not.

**Hold the name, never the index.** The corpus went 661 → 661 → 666 → 669 → 673 across the five
days in this post. A cursor holding "I got to 454" resolves, on the next pass, to whatever tool is
now 454th — and every insertion earlier in the alphabet shifts that by one. You would skip real
tools and re-sweep others and the tape would look perfectly healthy while doing it. Store
`mesh-report`, not `454`. Then a cursor naming a tool that has since been deleted has to fall back
to the head **and say so in the output**, rather than silently resolving to index 0 and looking
like a normal fresh pass.

**Advance it after every item, not at the end of the pass.** This one is specific to how passes
actually end here, and it is worth checking on your own system before assuming otherwise. On this
box a pass ends by being *killed* far more often than by finishing: the catch-up scheduler cuts a
fire at 2700s, and the machine power-cycles several times a day. A cursor written on the clean
exit path is a cursor that is essentially never written. Every irreversible step gets claimed
before the next one starts, or a crash mid-pass makes everything already done invisible to the
successor, which then repeats it.

**Put `from=` and `wrapped=` next to `swept=n/N` in every renderer.** This is the fix to the
original sin. `swept=302/669` is a true statement that cannot answer the only question a reader
has, which is *are the other 367 next, or are they never?* A scalar coverage number is ambiguous
between "this window" and "permanently outside every window", and those two situations demand
completely different responses. The number needs to carry where the window started and whether
the walk has wrapped, or it is just as misleading when it is honest as when it is not.

## The gate that passed for the wrong reason

One more, because it nearly got past me and it is the most portable lesson in the post.

I wrote a test for the "advance after every item" rule. Set the wall-clock bound low, run a
truncated pass, assert the cursor moved to the tool that was swept. Then I wrote the mutant it was
meant to catch — move the cursor write from inside the loop to after it — and ran the test against
the mutant.

It passed. Green, against the exact defect it was written for.

The bound I had picked for the fixture was `0`. A bound of 0 truncates *before the first tool*, so
nothing is swept at all — and when nothing is swept, correct code leaves the cursor untouched and
the deferred-write mutant also leaves the cursor untouched. The two candidates produce the same
value, so the assertion cannot distinguish them. **A fixture whose two candidates carry one value
cannot discriminate, no matter how sharp the assertion reading it is.**

The bound is `1` now, which lets the first fixture tool through and truncates at the second, and
the mutant goes red. The general form: after writing a test, break the thing it tests and *watch
it fail*. A gate you have not seen fail is not a gate — and a gate that passes against its own
mutant is worse than no gate, because it is now actively certifying the bug.

## The rule

Honesty about coverage is necessary and it is not sufficient.

An instrument that reports `swept=302/669` and exits non-zero on truncation is doing everything
the usual advice asks of it. It is not rounding up, not pretending, not silently degrading. And it
can still be **permanently blind to a third of its subject**, in the same place, every single day,
while every number it prints is true.

The missing property is not honesty, it is **advance**. If your scan, sweep, crawl, backfill, or
reconciliation job can be cut off before it finishes, ask the second question: when it restarts,
does it restart *where it stopped*, or does it restart *at the beginning*? If it restarts at the
beginning, your coverage number is not measuring your coverage. It is measuring how far into the
alphabet you get before the timer fires, and the rest of your system is not being scanned at all.

The tell is cheap to check and it is in data you almost certainly already have: **take your job's
progress tape, group by run, and look at where each run started.** If that column is a constant,
you have this bug.

Mine was `mesh-access-probe`, four days running.

---

*Bounds, stated: the "never swept once" claim is over the four passes since the progress marker
landed on 2026-08-25, not over all time — earlier full passes did exist, back when the corpus was
654 tools and the rate was 53s each, and that is where this tool's known forgeries were actually
found. So the honest statement is that the tail went unswept for as long as I have tape for, not
since the beginning. The per-tool rate is a mean over three passes (n=3) and the tools in the
unswept tail may well be slower or faster than the swept head, which would move the 27.6h
estimate; the conclusion survives that, since the cadence is 24h and the gap is not close. And the
fix is live but young — one pass, currently sweeping ground the detector has never looked at. What
it finds out there is not in this post.*

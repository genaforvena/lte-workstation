---
title: A fault model is not a flag
tags: distributedsystems, consensus, testing, bash
canonical_url:
---

I have a small consensus tool. It takes votes on stdin, keeps per-topic state in a JSON file, and
supports two algorithms: a Byzantine-fault-tolerant mode with a 2/3 weighted quorum, and a
Multi-Paxos mode with a crash-fault simple majority over an acceptor set. You pick one with a
flag:

```
printf 'a|blue\nb|blue\n' | mesh-vote deploy-ready --algo multipaxos
```

That line contains a defect I did not see for six weeks, and it is not in either algorithm. Both
are implemented correctly. The defect is in the *scope of the selector*: **the algorithm is a
per-invocation flag, and the cluster is per-topic durable state.** One is chosen fresh every call.
The other outlives every call. Nothing connected them.

Here is what that costs, measured both directions on the version before the fix.

## Direction one: a minority of two announces consensus at 100% confidence

Establish a five-acceptor Multi-Paxos topic. Everyone agrees on `blue`:

```
$ printf 'a|blue\nb|blue\nc|blue\nd|blue\ne|blue\n' | mesh-vote xalgo1 --algo multipaxos
blue — chosen slot=0 ballot=1 leader=a accepts=5/5 (phase1)
```

Now two of those five nodes run a round and **omit the flag**. Not a malicious act — a call site
somewhere that was written before anyone switched this topic, or a shell function that lost an
argument, or a human typing the command from memory:

```
$ printf 'a|red\nb|red\n' | mesh-vote xalgo1
red — confidence 100% (quorum) n=2
$ echo $?
0
```

Two nodes out of five just announced a new consensus, at 100% confidence, exit code 0. Under the
topic's own algorithm that round is *held*: 2 is less than the majority of 3, and the tool would
have printed `blue — held (turnout 2/5 below majority 3, no leader elected) ballot=1` —
verified by driving it. It did not run the topic's own algorithm. It
ran the default, whose quorum is computed over the workers who showed up.

The state file afterwards is the part I want you to look at:

```json
{"paxos": {"ballot": 1, "leader": "a", "slot": 1,
           "log": [{"slot": 0, "ballot": 1, "value": "blue"}],
           "last_chosen": "blue", "acceptors": ["a","b","c","d","e"]},
 "reputation": {"a": 0.55, "b": 0.55},
 "last_consensus": "red", "last_confidence": 1.0}
```

One file. Two answers. `last_chosen: "blue"` from Paxos, `last_consensus: "red"` from BFT, sitting
side by side under different keys, both current, both written by successful rounds. Nothing in the
tool flagged it, because from each algorithm's point of view nothing went wrong. Each one read its
own keys, found them consistent, and wrote its own keys back. The contradiction only exists in the
union, and no code was reading the union.

## Direction two: the string the test suite asserts is impossible

The other way round is sharper. Establish a five-worker BFT topic, then let **one stranger** enter
it under the other flag:

```
$ printf 'a|blue\nb|blue\nc|blue\nd|blue\ne|blue\n' | mesh-vote xalgo2
$ printf 'z|red\n' | mesh-vote xalgo2 --algo multipaxos
red — chosen slot=0 ballot=1 leader=z accepts=1/1 (phase1)
```

`accepts=1/1`. A single node, never seen on this topic before, elected itself leader and chose a
value on a cluster with five known members.

This is where it stops being a curiosity. That output shape — a lone acceptor announcing `chosen`
— is exactly what a previous fix to this tool was written to prevent, and the test suite contains
an assertion that it can never happen. The assertion passes. It has always passed. The suite drives
the Paxos path with a Paxos topic, and the guard it verifies is real.

The selector was a door into the same room that the test suite was standing in a different doorway
of. **A guard that is correct within one code path says nothing about the state that path shares
with another one.** Split-brain had been closed at the denominator (the quorum fix), and closed at
the write (a lock and an atomic rename). This was a third door, and it opened on one omitted word.

## Why this is not "the user passed the wrong flag"

It is tempting to file this as operator error. It isn't, for a reason worth stating precisely.

The two modes are not two implementations of one guarantee. They are **different fault models**.
BFT tolerates nodes that lie, at the price of needing a 2/3 weighted supermajority. Multi-Paxos
tolerates nodes that crash, and settles for a simple majority of a known acceptor set. Each is
sound. Neither is sound *over state the other one has been mutating*, because each is reasoning
about a membership and a history that the other has been editing under a different set of rules.

So a topic that alternates between them does not hold the weaker of the two guarantees. It holds
**neither**. And the observable failure — a minority announcing consensus, a stranger choosing
alone — is indistinguishable from a genuine bug in the algorithm you happen to be reading. I spent
the first few minutes of this looking at the quorum arithmetic.

The general form: *if a parameter selects between incompatible interpretations of durable state,
that parameter is part of the state's schema, not part of the call.*

## The fix, and the one line of it that is easy to get wrong

The state now records the algorithm that wrote it, and a mismatched round is a refusal — exit 1,
state untouched, same treatment as a corrupt state file:

```
$ printf 'a|red\nb|red\n' | mesh-vote xalgo1
mesh-vote: topic state .../xalgo1.json is bound to --algo multipaxos (stamped) and this round
asked for bft — refusing to run.
  bft is a 2/3 Byzantine weight quorum; multipaxos is a crash-fault simple majority over an
  acceptor set. They are different fault models over the same durable state, so a topic run under
  both holds neither: a minority that is correctly HELD by one algorithm can announce a fresh
  consensus under the other.
  Pass --algo multipaxos, or --switch-algo to rebind this topic deliberately.
$ echo $?
1
```

Straightforward. Except for the migration, which is where a guard like this usually dies quietly.

**Every state file that already exists has no stamp.** The field is new. If an absent `algo`
resolves to "whatever this round asked for" — the natural-looking default, the one you write
without thinking — then the guard agrees with every caller on every pre-existing file. It is
vacuous exactly where it is needed, and it stays vacuous until every topic has run at least once,
which for a rarely-used topic is *never*. You would ship a guard, watch the tests go green, and
have protected nothing.

An omitted field must never resolve to the value that makes the check pass. So the binding is
inferred from the keys the state actually carries:

```python
def state_algo(st):
    if isinstance(st.get("algo"), str) and st["algo"]:
        return st["algo"], "stamped"
    has_px  = "paxos" in st
    has_bft = any(k in st for k in ("reputation", "last_consensus", "last_confidence"))
    if has_px and has_bft:
        return "mixed", "inferred"   # already contaminated — its own refusal
    if has_px:
        return "multipaxos", "inferred"
    if has_bft:
        return "bft", "inferred"
    return None, "fresh"             # genuinely nothing decided yet
```

The data's own shape is the back-fill, never the request. And note the `mixed` branch: a file that
carries *both* key families is a topic this defect has already run through. There is no protocol
answer to which of its two disagreeing values is real, so it refuses and prints them both — an
operator can pick, and the tool must not pretend it can.

The stamp is written inside the single `save()` function rather than at each decision site. A stamp
written on only some paths leaves a topic whose last round happened to take an unstamped path
looking like a legacy file forever.

## A rebind must raise the bar, never lower it

`--switch-algo` is the deliberate escape hatch. It has its own trap, and it is the same one as the
lone stranger above: **the Paxos sub-state is born empty, but the topic is not new.**

Switch a five-worker BFT topic to Multi-Paxos and the acceptor set starts as `{}`. The first voter
is then a majority of themselves, and the switch hands back the exact split-brain the guard just
closed. So the switch carries the outgoing algorithm's membership across — those workers are the
topic's own record of who is in this cluster:

```
$ printf 'z|red\n' | mesh-vote xalgo2 --algo multipaxos --switch-algo
UNKNOWN — held (turnout 1/6 below majority 4, no leader elected) ballot=0
```

Held, not chosen. The carry can only ever *raise* the quorum bar, which is the only direction a
quorum is allowed to move without an operator saying so.

The carry is also persisted (`acceptors_src=learned+carried`), not just noted in the round that
performed it. The whole point is that some of those acceptors have never been seen voting under
this algorithm; a reader asking "is this bar real?" needs that provenance for as long as the bar
stands. A label that reverts to plain `learned` on the next round records the transition and loses
the fact.

## What this is not

Three things, because a post like this is worth less than nothing if it overstates its evidence.

**This tool has never run on a real topic.** Its state directory is empty; no cron job and no
dashboard calls it. Every drive above is a hand-built cluster under a scratch `HOME`. So the blast
radius of the bug was zero — and so was the live exercise of the fix. What I am claiming is that
the *shape* is real and common, not that it took down a production cluster.

**Thirteen mutants go red against the new arms, and two more were thrown out rather than counted.**
One was equivalent: it changed only the genuinely-fresh branch, where "bound to nothing" and "bound
to whatever you asked" behave identically, so it could not fail. One was invalid: it called `save()`
from above its own definition and died of `NameError` before reaching the code under test. A mutant
that goes red for the wrong reason is not coverage — it is a green light wearing red.

**The first mutant run of all was discarded whole, because the control was red too.** The copies
were not executable, and the suite invokes `"$0"`. Every mutant "failed"; the numbers looked
excellent. A mutation run whose control does not pass measures the harness, not the code, and the
failure mode is that it flatters you.

## The rule

A configuration flag that selects between incompatible readings of persistent state is a property
of that state. Pin it there, refuse on mismatch, infer the binding for records written before the
field existed — from the data's shape, never from the caller's request — and make the deliberate
rebind carry forward everything that constrains it.

The tell that you have one of these: a knob whose two settings both work, whose wrong setting
produces plausible output, and whose correct value is not recoverable from anything you have
written down.

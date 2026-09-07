# Multi-Paxos study artifact — 2026-09-07

The idea-queue item is already implemented in the genome source at
[`scripts/mesh-vote`](../scripts/mesh-vote). The cluster algorithm is selectable per invocation
with `--algo multipaxos` or `MESH_VOTE_ALGO=multipaxos`, and the topic state binds the algorithm
durably so a later BFT/Multi-Paxos mismatch refuses instead of mixing fault models.

The Multi-Paxos path provides:

- a stable leader and ballot/slot log;
- phase 1 on leader change and accept-only steady-state rounds;
- majority quorum over a configured or learned acceptor set;
- explicit `--reconfigure` and `--switch-algo` escape hatches;
- locked, atomic state publication and refusal of corrupt state.

Verification run from the source tree:

```text
$ bash -n scripts/mesh-vote
$ scripts/mesh-vote --test
smoke-test: ok
```

The self-test drives fresh Multi-Paxos rounds, a steady-state slot, leader change, minority hold,
algorithm mismatch, legacy-state inference, membership carry on switch, corruption refusal,
atomic-save crash injection, and concurrent rounds. It uses a scratch `HOME`; no live topic or
dashboard is wired to this study prototype yet.

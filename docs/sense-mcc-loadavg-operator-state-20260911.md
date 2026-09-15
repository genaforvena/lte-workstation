# MCC sense closure: `mesh-loadavg` → `mesh-operator-state`

Date: 2026-09-11

Closed producer↔consumer link: `scripts/mesh-loadavg` → `scripts/mesh-operator-state`.

The producer is a live `/proc/loadavg` reader. The consumer now reads its fresh
`.mesh/.loadavg-state` artifact and exposes `loadavg_state`; only the joint pattern
`operator=AT-DESK` + `loadavg=OVERLOADED` emits `cross_sense=DESK-UNDER-LOAD`.
OVERLOADED alone, AT-DESK alone, missing state, malformed state, and stale state do not
emit the relation. The cache is freshness-gated at 900 seconds.

Evidence:

- `mesh-loadavg --json`: PASS, real `/proc/loadavg` read and fresh `.mesh/.loadavg-state`.
- `mesh-loadavg --test`: PASS, including the real-read gate.
- `scripts/mesh-operator-state --test`: PASS, including fresh-artifact consumption,
  stale→UNKNOWN, positive joint relation, and non-overloaded negative control.
- `bash -n scripts/mesh-operator-state`: PASS.
- `git diff --check`: PASS.

Doctor gate: NOT CLEAN. `mesh-doctor` reports pre-existing `egress rides tailscale0`
and `exit-node set` failures, plus existing warnings for the busy default mic, untimed
peer SSH, sole-path bypasses, and absence-as-negative-reading sites. No new orphan warning
was reported. Therefore no `[sense]` board post was made, per the mint contract.

Uncommitted by request. Changed source: `scripts/mesh-operator-state`.

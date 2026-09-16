# test-forgery/mesh-doctor — --status dry-run wrote production log; fixed in mesh-supervise (2026-09-16)

Task: test-forgery/mesh-doctor-test-writes-the-liveness-log-it-checks (owner=genome)
Source accusation: chat.log:69463 — `--test` growing autowire.log, chat-deliver.log,
devcd-catch.cron.log, node-care.log, supervise.log (phaedra, attribution).

## Investigation
- `mesh-doctor --test` == `smoke_test` only (scripts/mesh-doctor:4847). The suite is
  heavily fixture-sandboxed (mktemp throughout) and redirects its own evidence tape to
  mktemp (`_SC_EVIDENCE`). No live invocations of chat/autowire/devcd/node-care exist
  in the --test path — 4 of 5 accused logs are NOT attributable to current source.
- The one live external call: `mesh-supervise --status` (real HOME). In mesh-supervise,
  `--status` was parsed at line 710 — AFTER two branches that author production
  `supervise.log`: absent-registry FAIL (691) and lock-timeout (705), both firing
  repeatedly (every --test), contradicting the file's own dry-run contract.
- Cross-node evidence: phaedra deployed mesh-doctor DRIFTS from genome source
  (5a936075… vs 82077abb…), while mesh-supervise matches; phaedra supervise.log holds
  ~199k FAIL/LOCK-TIMEOUT lines incl. no-registry bursts (2026-08-27, registry created
  09-03). The local sweep could not attribute here: all 4 --test runs exceeded the
  30s bound (rc=124), no verdict rows — suite length, not cleanliness proof.

## Fix (scripts/mesh-supervise, uncommitted working tree — landing via autoland/steward)
- Parse `--status` BEFORE the registry check; guard both production writes with
  `[ "$STATUS" = 1 ] ||`. Real runs unchanged (STATUS=0 passes through).
- Red→green, both arms driven live:
  - no-registry `--status`: was (rc=1 + FAIL line in production LOG) → now rc=1, LOG untouched.
  - contended-lock `--status` (lock held, MESH_SUP_LOCK_WAIT=3): was (rc=75 + LOCK-TIMEOUT
    line) → now rc=75, LOG untouched.
  - no-registry real run: still rc=1 WITH the FAIL line (f215c9e loud-fault preserved).
  - `bash -n` clean; live `--status` on this node lists children, rc=0.
- Deliberately OUT of scope: once-ever DEGRADED markers (child_pids, lines ~125/132) —
  single-write visibility, not repeatable forgery; touching them risks f215c9e-class silence.

## Remaining (not this row)
- chat-deliver.log / devcd-catch.cron.log / node-care.log / autowire.log accusations:
  unreproduced against current source; likely phaedra's drifted deployed copy or
  concurrent-cron coincidence (diskio-row pattern). Re-open only with a `self:`-attributed row.
- phaedra's deployed mesh-doctor drift (5a936075 vs 82077abb) belongs to whoever owns
  phaedra deploys — flagged, not fixed from here.

## Retry edge
Re-run `mesh-test-forgery --tool mesh-doctor` after landing + deploy; a future `self:` row re-opens this.

## Delegation
- None — single tightly-coupled investigate-fix-verify pass; exemption: one file, one defect, no splittable pieces.
- Personally inspected: smoke_test source region, STATUS/registry/lock ordering, live red+green drives, phaedra hashes + log counts over ssh.

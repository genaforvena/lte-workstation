# Sense coevolution: desk presence → operator state

Closed the under-consumed `mesh-desk-presence` → `mesh-operator-state` link (option b). Before the
change, `rg -l 'mesh-desk-presence|desk_presence' scripts/mesh-situation scripts/mesh-sensorium
scripts/mesh-stress scripts/mesh-ambient-clock scripts/mesh-operator-state` found no consumer. The
existing producer emitted a real `LIKELY-AWAY` observation on mesh-home.

`mesh-operator-state` now runs the producer live with a 30-second bound, validates its four verdicts,
and exposes `desk_presence` in text and JSON. Exit 2 and other non-zero producer exits render
`UNREACHABLE`; a missing executable is `UNAVAILABLE`; malformed successful output is `UNKNOWN`.
The cross-sense field reports `OPERATOR-UNKNOWN+DESK-LIKELY-AWAY` (and the corresponding active or
present-idle relation) without changing the primary operator state or assigning identity to an
unattributed person at the workstation.

The end-to-end integration used the real `mesh-desk-presence` script and hardware-backed read while
isolating unrelated operator-state inputs. Its artifact is
[`sense-coevolution-operator-state-20260914.json`](/home/mesh-home/lte-workstation/task-receipts/sense-coevolution-operator-state-20260914.json):
`state=UNKNOWN`, `desk_presence=LIKELY-AWAY`, and
`cross_sense=OPERATOR-UNKNOWN+DESK-LIKELY-AWAY`. The producer's standalone real-read artifact is
[`sense-coevolution-desk-presence-20260914.log`](/home/mesh-home/lte-workstation/task-receipts/sense-coevolution-desk-presence-20260914.log).
An unisolated `mesh-operator-state --json` attempt produced no JSON because its existing
`mesh-body-motion` call has no timeout and hung on the phone read. The integration isolated that
unrelated input so the actual producer→fusion path could be exercised; rerun the ordinary command
after the phone-motion path responds or is separately bounded.

Verification: `bash -n scripts/mesh-operator-state`; `scripts/mesh-operator-state --test` passed,
including a producer exit-2 assertion that stays `UNREACHABLE`; `git diff --check` passed. Full
`mesh-doctor` completed with rc=0, 0 FAIL and 33 repository-wide WARN. Its stable orphan set does not
include `mesh-desk-presence` or `mesh-operator-state`, and no orphan WARN names this link. Full output:
[`mesh-doctor-sense-coevolution-20260914-rerun.log`](/home/mesh-home/lte-workstation/task-receipts/mesh-doctor-sense-coevolution-20260914-rerun.log).

The updated installed fusion matches the source; the previous installed copy is preserved at
`/home/mesh-home/.mesh/tools-backup/mesh-operator-state.pre-desk-presence-20260914`. The requested
`[sense]` line was posted at 2026-09-14T17:00:06Z. No commit was made.

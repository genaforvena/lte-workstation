# Live driver process identity correction — witness verification — 2026-09-11

## Verdict

REJECTED pending a receipt-only correction. Runtime behavior and committed code pass, but the owner
receipt is not exact: it records deployed `mesh-consume-all` SHA-256
`c2266ca6e0483073a0288e941ae1d25b884e8552d51fdcd9528aa31ffc76e19a`, while commit `235b6aa1`
and the deployed executable both hash to
`31d7a6be9e0429417d7cd39a90f901a9abea5a6e6cf7cb779379b36d571165f5`. The discrepancy came from
the final live symlink-spelling correction after the receipt's hash was captured.

## Independent evidence

- `bash -n scripts/mesh-consume-all tests/test-mesh-consume-all-identity.sh scripts/mesh-pane-consume` — PASS.
- `tests/test-mesh-consume-all-identity.sh` — PASS: decoy excluded and concurrent ensure passes converge.
- `scripts/mesh-consume-all --test` — PASS.
- `scripts/mesh-pane-consume --test` — PASS.
- `tests/test-mesh-pane-consume-task-aware-idle-gate.sh` — PASS.
- Commit `235b6aa1` is an ancestor of `origin/main`.
- Source/deployed `mesh-consume-all` hashes both equal `31d7a6be9e0429417d7cd39a90f901a9abea5a6e6cf7cb779379b36d571165f5`.
- Source/deployed `mesh-pane-consume` hashes both equal `44a44dd490c31a44dda3bed0ca681d61be638f26a222b063a33778647dd20c3a`.
- Exact `/proc` audit found 15 channels, 15 processes, zero duplicates, and every process stamped with
  the deployed pane-consumer SHA.
- A plain deployed supervisor pass left all 15 status rows and PIDs unchanged.

## Exact correction

Correct only the stale supervisor SHA in
`docs/task-receipts/live-driver-process-identity-correction-implementation-20260911.md`, land and push
that receipt correction, then independently reconcile the corrected blob. No runtime/code change is
required by this finding.

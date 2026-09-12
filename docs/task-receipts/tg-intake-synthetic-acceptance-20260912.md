# TG synthetic-intake acceptance — 2026-09-12

## Verdict

**PASS.** The current `scripts/mesh-task` path satisfies the isolated acceptance contract. No
implementation task is needed. The fixture used a temporary `MESH_DIR`, task-chain directory,
canonical chat log, and board-event writer; it did not inject an ask into live operator intake.

## Evidence

Ran:

```text
rtk python3 tests/test-mesh-task-tg-intake-acceptance.py
PASS: isolated TG ask kept one owner/key and refused artifact-free closure
```

The acceptance test creates one synthetic keyed ask and a one-step `genome` plan, then verifies:

- the owner-scoped dispatch queue contains exactly one row for that task and its dispatch check exits
  0;
- one initial task post names `owner: genome` and carries the same ask key;
- the key is unchanged in every canonical task-ledger revision across create, take, and close;
- `done` with a missing artifact exits 2, leaves the chain active, and emits no completion receipt;
- `done` with a real temporary artifact completes the chain and records its SHA-256.

Test source SHA-256: `6b7d60e6c0c6218bc8f65b5036e79fb8ec6e4e70998b2c73ed5f238ad202c89e`.

The test exercises the real `mesh-task` CLI and its isolated canonical log path. The board writer
only captures task events under the temporary directory, so no synthetic operator message or live
intake state was changed.

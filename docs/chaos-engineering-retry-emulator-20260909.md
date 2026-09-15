# Chaos-engineering retry emulator — implementation run

Date: 2026-09-09

The repository now has a hermetic retry fixture at `scripts/mesh-chaos-emu`. It
keeps a per-scenario attempt counter, injects deterministic fail-first or
scripted nonzero exit codes, optionally hangs an injected attempt, and executes
the wrapped command after the fault budget is consumed. State is caller-scoped
with `MESH_CHAOS_EMU_DIR`, so acceptance runs do not touch live mesh state.

The bounded owner-routed consumer is `scripts/mesh-chaos-consumer`; it drives
two rc=75 failures and records retry/recovery transitions in its outcome log.
The existing `mesh-chat-deliver` test uses the emulator behind a fake
`mesh-tell`, so the retry logic is exercised through an actual repository
consumer rather than only through the emulator's unit smoke test.

## Verification

All commands ran from the repository root and passed:

```text
tests/test-mesh-chaos-emu.sh
  PASS: scripted transient/terminal rc sequence and validation
tests/test-mesh-chaos-consumer.sh
  PASS: owner-routed isolated fail-first/recovery consumer
tests/test-mesh-chat-deliver.sh
  PASS: 3 attempts, one failure edge, terminal ack, spaced terminal ack,
        duplicate suppression, fresh id reopen
scripts/mesh-chaos-emu --test
  smoke-test: ok
scripts/mesh-chaos-consumer --test
  smoke-test PASS
```

This is local-only and bounded: no service, network, scheduler, or substrate
state was changed. The source and tests are intentionally left uncommitted for
the steward to land.

# Design-spec sweep — model swap disposition

Task: `design-spec-task-sweep-20260907/spec-model-swap`

Status: complete; owner `tg`.

## Evidence

The model-swap design is explicit in `docs/superpowers/specs/2026-07-15-model-swap-design.md`:
STT/vision auto-swap requires a `mesh-model-swap` implementation, consumer-resolution
verification, and an organ-owned `--test` gate before adoption. The TTS path is proposal-only.

The repository has `mesh-model-resolve`, `mesh-model-bench`, and related model tools, but no
`scripts/mesh-model-swap` implementation or completed live swap/gate artifact was found during
this disposition. Therefore the design cannot honestly be marked done.

## Current blocker and next action

Blocker: implementation and live gate evidence are absent. Retry by implementing the marked-line
STT swap surface first, then run resolve plus the consumer's real test and preserve rollback
evidence. No adoption or completion claim is made here.

## STT swap implementation and gate evidence (2026-09-07 17:48Z)

The marked-line STT surface is now implemented and deployed. The marker is immediately above the
single ladder line in `scripts/mesh-voice-rx`; `scripts/mesh-model-swap` rewrites only that
marked ladder, requires an existing model, creates a rollback backup, and restores on syntax
failure. The selected incumbent is `ggml-large-v3-turbo-q5_0.bin`.

Owner artifacts and hashes:

- `scripts/mesh-model-swap` and deployed `/home/mesh-home/.local/bin/mesh-model-swap`:
  SHA256 `902e018517de3ecea45646e73e64fb1622e367b610fb2d5474cf235d5314c5d6`.
- `scripts/mesh-voice-rx` and deployed consumer:
  SHA256 `69973216dc6c439dc907ad3efe6bb2035cc90b4a0729459750212b65bece3d73`.
- rollback backup `/home/mesh-home/.mesh/model-swap/mesh-voice-rx.bak`:
  SHA256 `69973216dc6c439dc907ad3efe6bb2035cc90b4a0729459750212b65bece3d73`.
- regression test `tests/test-mesh-model-swap.sh` SHA256
  `0037825123df741197d08b8cea0f0e1ab041db754035bf8a9104c0d8269a1e61`; it exercises a real temp
  copy and the refusal path.

Red-before-green and focused verification:

```text
initial red: tests/test-mesh-model-swap.sh rc=1 — implementation missing
red refusal: nonexistent model rc=2, restored=yes
mesh-model-swap --test: rc=0, smoke-test: ok
test output sha256=17eef3feb959f69b6301b3c57b6ff1362a9af4acbaa694f498ffebe23601695f
bash -n scripts/mesh-model-swap: rc=0
python3 -m py_compile mesh-model-resolve deployed mesh-voice-rx: rc=0
mesh-model-resolve in consumer environment: rc=0
  voice-rx -> ggml-large-v3-turbo-q5_0.bin
  output sha256=e997ae375c9b82762e32629e0e5402439af06421f3a739804d3869c07b4fdf23
mesh-transcribe-organ --test (real organ): rc=0, smoke-test: ok
  output sha256=b389f643a6e1d4a5f38daf46cab24ca35ec82614c57d24d5d5954f9a30590c84
```

The bad-model mutation was performed against a temporary copy, not the live consumer; the exact
copy hash returned to its pre-mutation hash, proving refusal plus restore. The live consumer now
resolves the selected STT model and its real organ gate is green.

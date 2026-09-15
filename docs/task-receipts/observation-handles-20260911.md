# Observation handles prototype — 2026-09-11

## Result

`scripts/mesh-observation-handle` wraps one local command and writes a JSON receipt plus separate
byte-preserving stdout/stderr streams and fixed-size page files. The receipt records the exact argv,
shell display, UTC start/end timestamps, return code, status, stream byte counts and SHA-256 hashes,
page offsets/hashes, advisory overflow, timeout truncation, and the retention keep/prune boundary.

The real artifact is the `mesh-chat --tail 200` capture under
`artifacts/observation-handles-20260911/`; its receipt is the JSON file in that directory. The
capture was intentionally kept local: this prototype is not deployed or wired into a reflex yet.

## Failure states

- `status=ok`, `rc=0`: command completed successfully.
- `status=command-failed`, nonzero `rc`, `failure=command-rc`: command output remains a valid
  receipt and both streams remain inspectable; callers must not treat it as success.
- `status=timeout`, `rc=124`, `failure=timeout`: the process group was killed; both streams are
  marked `truncation=true`, so absence from the tail is not evidence of absence.
- `overflow=true`: the optional `--max-bytes` advisory bound was exceeded. Full bytes are retained;
  overflow is not silently converted into truncation.
- A receipt write or retention failure is reported on stderr. No success claim is emitted for a
  command whose receipt cannot be written.

## Verification

`tests/test-mesh-observation-handle.sh` proves stdout/stderr identity and hashes, page concatenation
and boundaries, retention pruning, nonzero command rc, timeout/truncation, and overflow without data
loss. It passed locally on 2026-09-11.

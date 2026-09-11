# Verified log reducers — 2026-09-11

## Result

Added `scripts/mesh-log-reducer`, a local JSON reducer for observation receipts. It applies hard
receipt, page, and stream-size bounds; validates stream and page lengths, offsets, and SHA-256
digests; rejects malformed/truncated or unverifiable records; and deduplicates repeated handles.
Accepted records retain the source receipt name, receipt digest, stream digests/byte counts, and
page digests, so every reduced value is traceable to captured evidence.

The real reducer artifact is
`artifacts/verified-log-reducers-20260911/reduced.json`, produced from the real
`artifacts/observation-handles-20260911/` capture. It accepted 1 handle and rejected 0 records.
Artifact SHA-256: `e22b4bd8b2f15a0d8c10aad732a365ebe96ee64842047f8579626adf9d6847d1`.

## Verification

`tests/test-mesh-log-reducer.sh` passed. It proves bounded receipt parsing, byte-identical replay
with duplicate inputs, same-length source mutation failure (`stream-hash-mismatch`), malformed /
truncated JSON rejection, and an oversized receipt rejection. The test also checks source receipt,
receipt digest, stream digest, and page lineage in accepted output.

Source hashes:

- `scripts/mesh-log-reducer`: `7c7b31fc17b5307b69b5ee50d631e8bddad7e77eb36e886af8843f08ec1f7beb`
- `tests/test-mesh-log-reducer.sh`: `7ce26234fbfe40450c58674a24cc5026891c931a4d99dbd9314b90a33852ecc9`

Failure semantics are explicit: the reducer still writes a JSON result containing rejections, then
exits 2 whenever any input is unverifiable. It exits 0 only when all inputs are accepted or when
duplicate handles are replayed.

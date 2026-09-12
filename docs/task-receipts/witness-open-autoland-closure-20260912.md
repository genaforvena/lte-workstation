# Open autoland reconciliation — 2026-09-12

Audited the six open autoland tasks at `~/.mesh/chat.log` physical lines 55717,
55730, 55742, 55759, 55766, and 55779. Each exact task key was still open and
had no earlier exact-key `[taking]` or `[done]`. The evidence receipts named by
the tasks were checked by SHA-256 against the local files and against blobs at
`origin/main` before closure.

| Exact task key | Artifact SHA-256 | Remote artifact | Landing commit |
|---|---|---|---|
| `autoland/health-warning/85f1e5114c1386ecd05e/triage` | `2b5e20ce8e15d28ea1809bfe96e6d00b870bd287112a5bbb591f8878db7d3a7a` | `docs/task-receipts/health-warning-85f1e5114c1386ecd05e-triage-20260912.md` | `7bbcbc7833037ce26eaca29669497952bdf791a9` |
| `autoland/witness-health-stale-receipt-correction-20260912/settle-overdue-health-triage` | `f32746056f5a37eee4c2aa9d07d7ef1c98a7299dbe786960e44a7c7fbce1db5e` | `docs/task-receipts/witness-health-stale-receipt-correction-20260912.md` | `1ee61f31b6c53195885117ea947d95805b75ba86` |
| `autoland/health-warning/747d421e2b2009967e9a/triage` | `1b804dd8440ec21bbb307c4c60489556f28be711e64940c2528c5e27d63dddb5` | `docs/task-receipts/health-warning-747d421e2b2009967e9a-triage-20260912.md` | `a73e01940cc591f6d28995be2a6bc4f9219c8e4a` |
| `autoland/health-warning/751e95f572b638ec0b9d/triage` | `64535e438a1d4ab432f917b92ba1470c042d35767d6cd86cf06a7a82d60b0727` | `docs/task-receipts/health-warning-751e95f572b638ec0b9d-triage-20260912.md` | `a75d9ce880f1980c37f4a324782687d84137ca42` |
| `autoland/tg-scripts-layout-migration-20260912/manifest-sync-doctor` | `72c7165a20f14c83d43fe34b693175d298c3f370d91e62c889e1068b596b16b6` | `docs/task-receipts/manifest-sync-doctor-20260912.md` | `cf60851d87f61b5515bd9ac1b455aaf88420dc9b` |
| `autoland/health-warning/655a5902f920e1bde157/triage` | `ce9dbdf59aa5f30c8015e03b65ac38dba55ce78a0b2eac9f61b1bf43a503e945` | `docs/task-receipts/health-warning-655a5902f920e1bde157-triage-20260912.md` | `b76fac7ccd3435fec0ff1509844ea3e9ab071ca6` |

The four health triage files originally lived under the untracked root
`task-receipts/` directory, which is outside `mesh-land`'s candidate set. Their
byte-identical copies under `docs/task-receipts/` preserve the original hashes
and were landed one at a time through `mesh-land` with the suggested task
subjects. The stale-receipt correction was already at its canonical docs path.

The manifest-sync receipt was already present remotely at line 55797's separate
`mesh-land` event, commit `cf60851d`; its exact receipt hash matched. It was not
landed again. Its implementation was already present in commit `08a122bf`.

Remote verification: after the five new landings, `git fetch origin main`,
`git rev-parse HEAD origin/main`, and `git ls-remote origin refs/heads/main` all
reported `b76fac7ccd3435fec0ff1509844ea3e9ab071ca6`. Streaming each of the six
remote blobs through `sha256sum` produced the table's artifact hash. Each task
was then closed with an owner-authored `[taking]` followed by an owner-authored
`[done]` carrying its exact task key, artifact hash, remote path, and commit.

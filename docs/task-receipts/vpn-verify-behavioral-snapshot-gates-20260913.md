# Independent behavioral snapshot gate verification (2026-09-13)

Task: `tinyfleet-drift-confirmatory-prerequisites-20260913/verify-behavioral-snapshot-gates`

Verdict: **PASS** for the six compatibility-preflight suite outcomes, frozen source identity,
runtime/dependency provenance, and retained logs. This does not claim a behavioral comparison,
score, or label; the upstream receipt correctly keeps those downstream gates closed.

## Assignment and inputs

The task ledger showed step 4 of 5 `open` before taking it. Step 3's artifact was present at
`/home/mesh-home/tiny-fleet/docs/task-receipts/haunt-behavioral-snapshot-gates-v3-20260913.md`
(SHA-256 `316555531af8ea8245e408b6afa3206b02974554ba63d850274135bd6ad59321`). The task was
therefore live and its requested independent audit matched the current state.

Frozen registration:
`/home/mesh-home/tiny-fleet/docs/tiny-fleet-artifacts-20260907/architecture-drift/02-external-sample-v2/sample-manifest.json`.
Run bundle:
`/home/mesh-home/tiny-fleet/runs/behavioral-preflight-v3-python311/`.
Recorded machine results SHA-256:
`d4c5dba53259a6a045592bc9906e80a5d3dcac56e0c7e237eccd734c9e23b966`.

## Independent replay

Replayed the archived source snapshots sequentially in a clean temporary study tree using the
exact image reference
`python@sha256:86adf8dbadc3d6e82ee5dd2c74bec2e1c2467cdad47886280501df722372d2e1` and the retained
`run_matrix.py`. Docker inspection confirmed image ID and repo digest equal that SHA-256
(`linux/amd64`). The runner reported Python 3.11.13, Linux 6.8.0-139-generic x86_64/glibc 2.36,
and OpenSSL 3.0.17. The independent invocation, output, install logs, full pytest logs, and resolved
freezes are retained under
`docs/task-receipts/vpn-behavioral-snapshot-gates-replay-20260913/`.

All six fresh runs had venv, install, freeze, and pytest exit codes `0/0/0/0`. Results:

| Snapshot | Fresh outcome | Frozen archive SHA-256 | Effective freeze SHA-256 |
|---|---|---|---|
| Flask 2.2.2 (`flask-old`) | 481 passed, 2 skipped | `9cab061d3c8b1fcc156b1ebb247d0a6caa73864fb096e1ebcdb369d2b3fbaefc` | `5cfe777cc24246048ea235cdfd75d430ab1ac02fb496aa9d7d977cae766b61cf` |
| Flask 3.1.0 (`flask-new`) | 490 passed, 2 skipped | `1ab1e67fb5c9e05d226e3cd94734e46009e012b269e29794f29151ef341feb06` | `9394584b694364848c5b539bb6d80a5826931bc4aff8659dfbd203d85d6c80f4` |
| Requests 2.28.1 (`requests-old`) | 579 passed, 13 skipped, 1 xfailed | `5b95d48511eaaad22b4bfe0ba42d12dcce08c97fb587aa9cfd17dab0399868b9` | `85eb0035b71b522c239820248f30c5c4c414a49c5860525a4e0e73510d6c95c7` |
| Requests 2.32.3 (`requests-new`) | 590 passed, 15 skipped, 1 xfailed, 18 warnings | `02db3918a45a7707a9eba6e240a7d3cde2ad5be23fc293dbe218d263662453dd` | `b0035a5a149179d941caae0aa82f524add447483e577399b7ec273be901f4bc6` |
| Pydantic 1.10.4 (`pydantic-old`) | 2,441 passed, 93 skipped | `d47f96f734030506f57bf3868314f2e3ccfcf34be323422a4ac645eb99c04585` | `bb1113a4097868ef905790a36e22a91bbe684e214fe3a09c02101706bc3d8a29` |
| Pydantic 2.10.4 (`pydantic-new`) | 5,050 passed, 1,039 skipped, 17 xfailed | `d8c26a1987494e70b3ee903a19ed7a75d37ea907358ed124d1567b7fa63b2df4` | `4cc2802ddc94505166023c34f5aa07baad33cbfd58fa1bd9b5e045bd69693ecf` |

Each source archive's SHA-256 and byte count match both `results.json` and its corresponding frozen
registration row. Each fresh resolved environment freeze is byte-for-byte identical to the stored
effective freeze above. The three recorded compatibility overrides are present in the effective
requirements and freeze: Flask-old uses Werkzeug 2.2.2/Jinja2 3.1.2/MarkupSafe 2.1.5; Requests-new
uses greenlet 2.0.2; Pydantic-old uses mypy_extensions 0.4.3. These are disclosed dependency
substitutions; they did not modify test assertions or pytest warning configuration.

## Integrity and warning/assertion checks

- Recomputed all six retained original pytest-log hashes from `results.json`; all matched. Each
  full log is present in the run bundle. The fresh independent full logs are also retained in the
  local replay artifact and show the same six pass/skip/xfail totals.
- The replay harness invokes `python -m pytest -q tests`; inspection found no warning filter,
  `PYTHONWARNINGS` override, `--disable-warnings`, or `-W ignore` option. Requests-new's log keeps
  its 18-warning summary and individual warning report visible.
- Every archived source/test/config tree matches its frozen registration hash. Among the files in
  the frozen Requests-new archive, the independently extracted copy differs only at
  `tests/certs/mtls/client/client.pem`, the documented public fixture-certificate replacement
  (SHA-256 `1323192105e8111761fb80f9fda74d5c63a458595a582cea830130098eb10c2b`). No test source,
  assertion, or warning policy was changed or weakened.

Evidence result: **PASS**. The six test-suite runs establish executable compatibility
preconditions only; they do not authorize comparison scoring or behavioral labels. Downstream
label and generative prerequisites remain separate gates.

# Haunt dictionary unblock receipt — adint/e39fd326ffa3e091

- Resolver: `unblock/adint/e39fd326ffa3e091/resolve`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Checked: `2026-09-12T00:20Z`
- Result: **BLOCKED/operator-input**

## Evidence

The parent remains blocked on missing scientific inputs. The current parent
receipt says the six-case runtime smoke does not discharge its dictionary arm.
The same-day adint revalidation receipt in `tiny-fleet` confirms no approved
dictionary input was selected, and the preceding operator-action packet gives
the exact missing-input manifest. Their SHA-256 digests were checked during
this resolution:

- `/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-adint-747f3093803a4ce6-20260912.md`:
  `c82237b282cf91a9bfcd1d77ef52841e94fa3241b06b457d7834be3381a5dd15`
- `/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-adint-4f1b25c11bcea743-20260911.md`:
  `0158eac7190e0ae21a62cb0c5755fa8d8a5b4473c78ba2a4e1b2a4bf4b486747`

## Exact operator-action packet

Provide and freeze all five fields below in a tracked study-input manifest;
placeholders are not valid inputs:

```text
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact Unicode/token normalization policy>
version: <immutable release, commit, or content checksum>
corpus: <immutable corpus path/URI plus SHA-256>
```

The source and corpus must be approved for this parent study. Do not substitute
the unrelated D02 concept list or install an unpinned package. After the manifest
and corpus are present, verify the corpus digest, run the parent's dependency
preflight and dictionary-arm command, and record their versions, output hashes,
and typed verdict. The bounded runtime-smoke command is:

```bash
cd /home/mesh-home/tiny-fleet
timeout 240 .venv/bin/python scripts/bbywvy_test.py
```

That smoke alone cannot clear the dictionary blocker. Resume the parent only
after the frozen inputs exist and the dictionary arm has its own verified result.
Until then, the exact retry condition is receipt of the completed five-field
manifest and matching corpus bytes (`event:operator-dictionary-input`).

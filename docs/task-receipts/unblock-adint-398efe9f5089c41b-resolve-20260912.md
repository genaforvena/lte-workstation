# Haunt dictionary unblock receipt — adint/398efe9f5089c41b

- Resolver: `unblock/adint/398efe9f5089c41b/resolve`
- Parent: `unblock/haunt/62c0662129fa8ee9/resolve`
- Checked: `2026-09-12T00:25Z`
- Result: **BLOCKED/operator-input**

## Revalidation

The parent ledger still reports `blocked`, type `operator-input`; the explicit
`mesh-task check resume unblock/haunt/62c0662129fa8ee9/resolve haunt` returned
exit 2. The dictionary source, study language, normalization policy, immutable
version, and matching corpus remain absent. The six-case runtime smoke does not
discharge the dictionary arm.

The exact operator-action packet was already recorded in
[`unblock-adint-e39fd326ffa3e091-resolve-20260912.md`](unblock-adint-e39fd326ffa3e091-resolve-20260912.md)
and in
`/home/mesh-home/tiny-fleet/docs/task-receipts/unblock-adint-4f1b25c11bcea743-20260911.md`.
It requires a tracked manifest with all five values frozen:

```text
source: <operator-approved dictionary/lexicon URI or repository-relative path>
language: <ISO language or explicit language set>
normalization: <exact Unicode/token normalization policy>
version: <immutable release, commit, or content checksum>
corpus: <immutable corpus path/URI plus SHA-256>
```

After those inputs arrive, verify the corpus digest and run the parent's
dependency preflight and dictionary-arm command. The bounded runtime check is:

```bash
cd /home/mesh-home/tiny-fleet
timeout 240 .venv/bin/python scripts/bbywvy_test.py
```

That command is only the six-case runtime smoke; it cannot clear the dictionary
blocker on its own. Resume the parent only after the frozen inputs are present
and the dictionary arm has its own verified result. Retry this resolver on
`event:operator-dictionary-input`.

# C07-V independent verification recheck — router failure boundary

- Actor: `vpn`
- UTC: 2026-09-11
- Canonical source revision: `71e09b56fd0f6b86988cf53c577f64b9c7da8122`
- Canonical implementation receipt SHA-256: `580b13780feaf3bc24fcc5650716e3791611fecf11863eec0288e3b3ef469e47`
- Fresh isolated checkout: `/tmp/tiny-fleet-c07-fresh-TcfiVV/repo`

## Fresh checks

All commands ran from the isolated checkout using `/home/mesh-home/tiny-fleet/.venv/bin/python`.

| Check | Exit | Output SHA-256 |
|---|---:|---|
| `scripts/test_router.py` | 0 | `74c03fc16fde9a2dfeff03db0ec8f472a5a8dfed04e9e982a912b4b7f64faee3` |
| `scripts/fleet_benchmark.py --test` | 0 | `9b278027e97aa3c0299d3242beba62227bd884ada4d1fdcd83d1f18fe2040193` |
| `-m compileall -q scripts/router.py scripts/test_router.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git diff --check` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Observed: router `Ran 7 tests ... OK`; fleet benchmark reported safety decisions `4/4`,
operator adversarial `14/14`, router contract `4/4`, specialist inventory `2/2`, and fleet
benchmark `24/24`.

## Load-bearing mutation

In the isolated checkout, the query embedding norm guard was mutated from an equality check to
an impossible negative comparison. The router suite then exited `1` and failed
`test_zero_query_embedding_abstains_with_machine_readable_reason`, observing
`invalid_similarity` instead of `invalid_embedding_norm`.

- Mutation output SHA-256: `78e33ac3880e01c6a69b558942bf2d5150ad3bffe02a22da1b4ad8780c62b436`
- Restored router output SHA-256: `670a39115e7523a8984e4842e16547cb2094b03fad392b037b4b9dc8b2656e62`
- Restored suite exit: `0`
- Final isolated checkout status: clean; `HEAD=71e09b56fd0f6b86988cf53c577f64b9c7da8122`

## Result

**CANONICAL DONE CONFIRMED.** Fresh independent evidence confirms the existing canonical
`/home/mesh-home/tiny-fleet/docs/task-receipts/C07-verification.md` PASS receipt. The mesh task
ledger already records `verify-router-failure-boundary` as DONE and has advanced to
`enforce-decision-consumer`; no duplicate terminal transition was issued.


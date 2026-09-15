# Genetic superoptimizer implementation — 2026-09-08

Task: add a bounded genetic-algorithm feature to the existing auto-code optimizer.

## Change

The Uxn chibicc consumer already exposed `-O2` as a deterministic genetic search over
safe peephole-pass schedules. `scripts/uxn/chibicc/src/optimize.c` now gives that search
an explicit lexicographic fitness: minimize generated instruction count first, then
literal bytes. The incumbent is still the fully optimized normal pass, so the genetic
search cannot return a larger program. Population size, generations, mutation rate, and
the deterministic seed remain bounded and unchanged.

## Focused trial

Fixture: `scripts/uxn/chibicc-eval/lease-gate.c`, preprocessed with the repository host
compiler. Two identical `-O2` runs emitted byte-identical TAL and did not exceed the
`-O1` token count:

| mode | TAL tokens |
|---|---:|
| `-O1` | 361 |
| `-O2` genetic | 361 |

The equal result is a non-regression, not an improvement claim.

## Verification

- `tests/test-uxn-genetic-superoptimizer.sh`: pass; deterministic output and `O2 <= O1`.
- `make -C scripts/uxn/chibicc`: compiler rebuild passed.
- `make -C scripts/uxn/chibicc test`: stopped at the existing missing `uxnasm` PATH dependency after compiling and emitting O0 TAL; no optimizer assertion failure was reached.
- `git diff --check`: pass.

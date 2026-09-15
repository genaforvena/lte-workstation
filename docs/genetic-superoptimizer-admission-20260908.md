# Genetic superoptimizer admission — 2026-09-08

Task: `study-genetic-superoptimizer-20260908/admit-genetic-superoptimizer`

## Current-state audit

The task was live when rechecked at 2026-09-08T16:44Z: the mesh task ledger showed the
step `open`, owner `discover`, and lease ending at 2026-09-08T17:00:53Z. The instruction
is correctly scoped: the repository has a named optimizer consumer and a bounded quality
predicate, so a real sample is required rather than a no-consumer rejection.

The consumer is the vendored C-to-Uxntal compiler at
`scripts/uxn/chibicc`. Its `-O2` path calls the deterministic genetic pass in
`scripts/uxn/chibicc/src/optimize.c`; the existing acceptance consumer is
`scripts/uxn/test-chibicc`, whose five-row `lease >= 2 * cadence` ROM truth table is the
quality predicate.

## Bounded measurement

Input: `scripts/uxn/chibicc-eval/lease-gate.c`, preprocessed with the repository's
documented host-compiler step. Toolchain was rebuilt with `scripts/uxn/build.sh --chibicc`
(rc 0; `bin/chibicc` 88224 bytes). Each mode compiled the same input once, then assembled
with `bin/uxnasm`.

| mode | TAL tokens | ROM bytes | truth rows | one compile wall |
|---|---:|---:|---|---:|
| `-O0` | 380 | 556 | 5/5 | 0.00s |
| `-O1` | 336 | 468 | 5/5 | 0.00s |
| `-O2` genetic | 336 | 468 | 5/5 | 0.00s |

The five rows were `900/1800=OK`, `900/1799=RED`, `900/1801=OK`, `900/900=RED`, and
`60/3600=OK`. The O2 ROM SHA-256 was
`71f966d35751b65a164fb8bcff30228e9bbd42349243682f4d470e889f1c4648`.

Cost accounting over 50 identical compilations of the same preprocessed input:

| mode | wall | user | sys | per-run wall |
|---|---:|---:|---:|---:|
| `-O1` | 0.03s | 0.02s | 0.01s | 0.0006s |
| `-O2` genetic | 0.11s | 0.08s | 0.02s | 0.0022s |

Thus the current genetic consumer is real and bounded, and its sample preserves the
quality predicate, but this sample shows no improvement over `-O1`: it costs about 3.7x
wall time while producing the same TAL and ROM size. No new optimizer or wiring is admitted;
the smallest honest disposition is a measured closeout and a future evidence requirement
for any claim of benefit (a corpus-level quality lift or a cost-justified objective).

## Verification and disposition

- `scripts/uxn/build.sh --chibicc`: pass.
- Direct O0/O1/O2 compile + assemble: pass.
- Five-row ROM truth table for all three modes: 5/5 each.
- `scripts/uxn/test-chibicc`: the compiler truth-table and mutation legs passed, but the
  overall test returned 1 because its existing vendor manifest includes only the original
  vendor tree while the current tree has three additional files (`LICENSE`, `Makefile`,
  `README.md`); this is unrelated to the optimizer measurement and remains an unresolved
  repository drift finding.

Verdict: admitted as a bounded measurement of the existing consumer; no implementation
follow-up is justified by this sample.

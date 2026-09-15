# Genetic superoptimizer trial — 2026-09-09

The repository's existing auto-code optimizer is the vendored Uxn/chibicc compiler.
Its `-O2` path runs the bounded deterministic genetic search in
`scripts/uxn/chibicc/src/optimize.c`, using safe peephole-pass schedules as genes and
keeping the normal optimized result as an incumbent.

Trial command:

```sh
bash tests/test-uxn-genetic-superoptimizer.sh
```

Result: PASS. The `lease-gate.c` fixture produced byte-identical output across two `-O2`
runs. The output was 361 TAL tokens at both `-O1` and `-O2`, so this small corpus trial
showed a non-regression but no size improvement. The test rebuilt the compiler from the
repository source before compiling the fixture.

The change remains in the working tree for steward review; no deployment or commit was
performed.

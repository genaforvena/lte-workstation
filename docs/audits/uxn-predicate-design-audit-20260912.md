# Uxn predicate design audit — 2026-09-12

Audited `docs/superpowers/specs/2026-07-23-uxn-predicate-engine-design.md` against the current sources, tests, and live cron entries. The predicate lane is implemented and has grown beyond the original per-gate-ROM proposal: `lisp-eval.rom` now executes s-expression predicates held as data, alongside the shared ROM runner for compiled gate ROMs. The old spec remains useful history, but it is no longer an accurate description of the whole lane.

## Findings

- **Shared runner (§1): implemented.** `scripts/mesh-rom-gate` resolves named or explicit ROMs, runs the local emulator, maps verdicts and honest n/a, and supports hash-before-execute pins. Its `--test` exercises both verdict polarities, missing-engine/ROM/mute-ROM refusal, domain NA, pin mismatch/tamper refusal, and attestation.
- **Fallback rule (§2): implemented for the thermal consumer.** `scripts/mesh-therm-watch` uses `mesh-rom-gate hyst-gate` and has an inline fallback marked `src=inline-fallback`; its smoke test asserts the ROM path and fallback equivalence. `scripts/mesh-body-power` still classifies its low-battery edge in shell (`classify_low`) and has no Uxn/ROM call. The later `mesh-body-gate` is a separate on-phone gate path; it does not satisfy the original `mesh-body-power` integration item.
- **Consumer wiring (§3): partly implemented.** The live `~/.mesh/reflexes.cron` contains `mesh-lease-audit` and `mesh-therm-watch` entries. The spec's requested `mesh-body-power` → `band-gate.rom` wiring is absent. Treat that item as open unless a later decision explicitly retired or replaced it.
- **Compiler lane (§4): implemented.** `scripts/uxn/chibicc/` and `scripts/uxn/cc-rom.sh` build C predicates into ROMs. `test-lisp-eval` rebuilds the evaluator and compares behavior against both the fresh and committed artifacts.
- **Predicate-as-data lane:** `scripts/uxn/sexpr-gates` contains `band-gate` and `hyst-gate`; the evaluator hash is pinned in the data. `mesh-sexpr-gate` validates positional natural arguments and refuses a mismatched evaluator before execution. `test-sexpr-gates` checks consumer-boundary truth tables, injection/arity/absence handling, pin refusal, expression equivalence, and flipped data predicates.
- **Documentation (§5): partly reflected.** `scripts/uxn/README.md` documents the evaluator and `mesh-sexpr-gate`. The old design's literal doctrine sentence about every new pure predicate defaulting to a ROM gate is not a complete description now that predicates can be data rows over a shared evaluator. Update the spec or mark it superseded when the lane's owner decides which current doctrine should stand.

## Parser and gate evidence

`lisp-eval.c` enforces naturals in 0..65535, checked arithmetic, lazy `if`, malformed-input rejection, a 512-byte source cap, and nesting cap 24. The current `test-lisp-eval` covers arithmetic/comparisons, both `if` branches and lazy errors, overflow/underflow/divide-by-zero, literal overflow, unknown op, unbalanced parentheses, and trailing input. It does **not** directly exercise the source-length or nesting limits; those implementation branches currently lack fixture rows.

On this node, the following completed successfully:

- `scripts/uxn/test-lisp-eval` — fresh and committed ROM tables passed; the inverted-`>=` mutant failed the same gate table.
- `scripts/uxn/test-sexpr-gates` — committed data fixtures passed; both boundary mutations went red; tampered evaluator was refused; injection and `--expr` checks passed.
- `scripts/mesh-rom-gate --test` — runner test passed, including n/a and tamper cases.
- `scripts/mesh-therm-watch --test` — passed on this node and reported a fresh live producer reading.

`scripts/uxn/test-threshold-ledger` was also run and **failed** (exit 1). Its output identifies stale consumer expectations: `mesh-load-gate --thresholds` now prints a second `eff_enabled/eff_thr` line, so four assertions comparing the entire output to only `thr/quiet/floor` fail. The hysteresis expression mutation's calibration subprocess returned 143 where the suite expected DIVERGE/rc 1; that leg did not verify successfully. These are unresolved test-suite issues, not passing evidence.

The mutation checks that did pass prove the tested boundaries discriminate their predicates; they do not fill the missing parser cap fixtures or establish the absent `mesh-body-power` wiring. The full threshold-ledger suite's failure remains open for a follow-up repair/audit.

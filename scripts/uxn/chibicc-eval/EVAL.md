# chibicc-eval — C→Uxn ROM compiler for the uxn pilot lane (2026-07-23)

**Task:** `uxn-chibicc-eval` (board 15:48Z, owner genome) — can
[lynn/chibicc](https://github.com/lynn/chibicc) (Rui Ueyama's chibicc retargeted to Uxntal)
replace hand-written Uxntal for mesh ROM organs? Artifact demanded: a working ROM from C
source under the existing pilot harness, Note3 armhf included.

## Verdict: YES for gate-class organs, with one structural catch — the pilot's vendored toolchain is a DIFFERENT (pre-2022) Uxn ISA

chibicc emits **modern uxntal** (bare-word calls → `JSI` 0x60 immediate opcodes, the
post-2022 ISA). The pilot's vendored `src/uxnasm.c`+`src/uxn.c` are the **older ISA**
(mode-bit encoding, no JCI/JMI/JSI): the vendored uxnasm rejects chibicc output
(`Unknown token: main_`) and the vendored uxncli **hangs** on a chibicc ROM (opcode 0x60
misdecodes; observed timeout, no crash). Migration is one-way clean:

| ROM \ emulator | vendored (old ISA) | modern uxncli |
|---|---|---|
| hand-written `lease-gate.rom` (133 B, old asm) | OK/RED correct | **OK/RED correct** (both verdicts seen) |
| chibicc `lease-gate-c.rom` (468 B) | **hangs** (timeout) | OK/RED correct |

So adopting chibicc means **vendoring the modern toolchain** (uxnasm from `~rabbits/uxn`
`archive/uxnasm.c`; uxncli from the same repo's pre-archive `src/`, commit `43453d7` — the
current `uxn11` emulator needs X11, unusable headless). Existing pilot ROMs keep working on
the modern emulator — no rewrite needed, only the emulator/assembler swap. (Exit-code
mapping differs across emulators; the pilot shims already judge by verdict TEXT, so they
survive the swap unchanged.)

## The artifact (RED-first, both architectures)

`lease-gate.c` (29 lines of plain C) reimplements the pilot's lease-vs-cadence gate —
same contract as `lease-gate.tal`: argv `<cadence> <lease>`, prints `OK`/`RED`,
`lease >= 2*cadence` inclusive. Compiled `gcc -P -E` (chibicc has no preprocessor) →
`chibicc -O1` → modern uxnasm → **`lease-gate-c.rom`, 468 bytes**
(sha1 `c46da8a…`, committed here). Truth table, exact match with the hand ROM:

```
900 1800 -> OK     900 1799 -> RED    900 1801 -> OK
900  900 -> RED    60  3600 -> OK
```

Both verdicts observed (not a constant), and the same **byte-identical** ROM pushed to the
Note3 (armeabi-v7a, static modern-uxncli cross-build per `verify-note3.sh` mechanics)
returns matching verdicts on all four rows: `900/1800 OK · 900/900 RED · 900/1799 RED ·
1800/3600 OK`. chibicc's own 800+-case suite also passes fully at `-O0` and `-O1` under the
modern toolchain.

Gotcha for future organs: `argv[0]` is an **empty program-name slot** — real args start at
`argv[1]`, `argc` counts the empty slot (first cut of the gate read `argv[0]`/`argv[1]` and
answered OK to everything; caught by the truth table before it saw RED).

## Subset-C limits (what an organ may use)

- **Yes:** C89 core (functions, loops, globals/locals, arrays, pointers, structs, enums);
  `char`/`short`/`int(16-bit)`/`unsigned`; limited variadics; `asm()` intrinsic for inline
  uxntal; varvara event handlers (`on_console` etc.); peephole `-O1`.
- **No:** preprocessor (use host `cc -P -E`), 32/64-bit ints, float/double, function
  pointers, VLAs, bit-fields, struct-by-value params/returns.
- 16-bit `int` ⇒ same `2*cadence` wrap ceiling (>32767 s) as the tal ROM's `MUL2` — parity,
  not a regression. Signed compare/divide is emulated and slow; prefer `unsigned`.
- `main(argc, argv)` pulls in a large support routine (468 B vs 133 B hand-written, 3.5×);
  a custom `on_console` handler is the lean path when size matters.

## Does it replace hand-written Uxntal?

For **gate-class organs** (arithmetic predicates, the pilot's whole point): yes — 29 lines
of readable C beat 44 lines of stack-machine uxntal for authorship and review, at 3.5× ROM
size (still 0.7 % of the address space). Hand uxntal remains right for size-critical or
vector-heavy ROMs. **Not adopted into the build yet:** wiring it means (a) vendoring the
modern toolchain + re-verifying the two existing ROMs' RED-first suites under it, and
(b) vendoring chibicc (or documenting a pinned clone) — filed as a follow-up decision, not
smuggled into this eval.

## Repro

```sh
git clone https://github.com/lynn/chibicc && cd chibicc && make   # host cc only
gcc -I. -P -E lease-gate.c -o lg.c && ./chibicc -O1 lg.c > lg.tal
uxnasm-modern lg.tal lease-gate-c.rom && uxncli-modern lease-gate-c.rom 900 1800
```

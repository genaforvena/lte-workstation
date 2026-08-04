---
title: I compile C to a 468-byte ROM that runs identically on x86 and ARM
tags: c, compilers, virtualmachine, systems
canonical_url:
---

I run a mesh of agents on old phones. They check invariants — is a watchdog's
lease longer than twice its producer's cadence? Is the battery in its longevity
band? Is the board log monotonic?

I was checking these with `grep`. Then I audited: **33 of 52** liveness gates
could *never fail* — each one `grep`'d its own source for a string, so it always
found itself. A gate you haven't seen fail is not a gate.

So I started moving them to [Uxn](https://wiki.xxiivv.com/site/uxn.html) — the
tiny virtual machine from [Hundred Rabbits](https://100r.co). Stack-based, 64 KB
address space, the emulator is ~42 KB of C89 with no deps beyond libc. A ROM you
assemble today runs unchanged on any architecture, forever.

## The first gate

A lease-vs-cadence check, hand-written in Uxntal (the assembly): 44 lines,
**134 bytes**. Same bytes pushed to an old Android phone — a 32-bit ARM core
running the identical ROM.

Then the obvious question: can I stop writing assembly?
[chibicc](https://github.com/rui314/chibicc) is Rui Ueyama's small C compiler;
someone [retargeted it to emit Uxntal](https://github.com/lynn/chibicc). The
same gate in 29 lines of plain C compiles to a **468-byte ROM** — truth table
exact match, cross-arch verified:

```c
void main(int argc, char *argv[]) {
    unsigned int cad = parse_int(argv[1]);
    unsigned int lease = parse_int(argv[2]);
    if (lease >= 2 * cad) print_string("OK\n");
    else                  print_string("RED\n");
}
```

```
cad=900 lease=1800 -> OK     cad=900 lease=1799 -> RED
cad=900 lease=900  -> RED    cad=60  lease=3600 -> OK
```

chibicc is now vendored — one `cc-rom.sh` goes from `.c` to `.rom`. Every gate
has a truth-table test that corrupts the arithmetic and watches it break. The
toolchain swap surfaced the best bug of the whole effort: old ROMs halted `#01`,
which maps to exit 1 under the modern emulator — and under `set -o pipefail`
(leaked from a sourced library), the entire audit *died silently*. No error, no
verdict, just gone. The fix was one byte.

## A ROM is a fixed point

Then it got interesting. A ROM is behavior decided once at commit time, in a
system where everything else re-infers per tick. That makes it a *fixed point* —
and a fixed point is three things:

**The thing you calibrate against.** I run the ROM and a different
implementation (native 64-bit shell arithmetic) on the same inputs and log both.
Agreement is weak evidence; *disagreement* isolates cleanly to the
implementations and posts loudly. The ROM's 16-bit `int` wraps at 65536 — a
`--pair 900 67335` input splits the two (ROM reads 1799, shell reads 67335) and
the calibrator catches it live. First fleet run: 208 pairs, 0 diverged.

**The thing you watch *with*.** The first fixed-point watcher is a board
invariant checker written in C, compiled to a ROM: it judges the last N board
lines for structure, monotonic timestamps, unknown nodes, and duplicate claims.
Text you control goes in; the ROM is the whole trust boundary.

**The thing that travels.** If a ROM is a fixed point, it can move. A ROM-as-
packet over SSH: the program ships in-band with the data
(`uxp1 <rom_bytes> <sha1>\n + <rom raw> + <payload>`). The receiving node — which
holds *zero* ROMs, only the 43 KB emulator — hashes what it actually got before
executing a byte. Declared hash ≠ actual is a loud refusal. This matters because
a tampered ROM that ran silently with rc=0 and empty output is indistinguishable
from consensus — so you verify, then execute.

## Gates as data

The next step got me to the actual payoff. I wrote a micro Lisp evaluator ROM
(3.9 KB) where the *expression is data*:

```scheme
(if (>= lease (* 2 cad)) 1 0)
```

That predicate ships as text and the fixed point runs it — homoiconicity on the
ROM, no recompile to change a threshold. Once the evaluator existed, the gates
collapsed into rows of a ledger:

- **stage 1** — the lease and band gates expressed as s-expression data lines
  the evaluator runs.
- **stage 2** — scattered inline magic numbers (battery bands, thermal windows,
  PSI ranges) became calibrated `threshold-ledger` rows, s-expr DATA, edited in
  one place.
- **stage 3** — an admission harness: a *generated* candidate gate (proposed by
  the cheapest available model through `mesh-relay`) has to pass the same
  RED-first truth table a hand-written one does before it's adopted into the
  ledger.
- **stage 4** — the walker that drives generated candidates through that door
  unattended, one per run, drain-first. Nothing walked through stage 3's door on
  its own — the never-wired-reflex hole again — so the walker is the reflex.

NA-honesty carries through all of it: overflow, `/0`, unknown op, bad parens all
answer `NA` (rc 2), never a wrapped value. A check that can't reach its input
says n/a; it does not fake all-clear.

## The body gates itself

This is where it stops being a thought experiment.

The first consumer of the mobile-code layer outside the `uxn/` directory is a
body node — the Note3 phone — gating its **own** battery and thermal:

1. Each run reads the phone's own sysfs (capacity, temperature in deci-°C).
2. It substitutes those numbers into `threshold-ledger` rows as s-expressions —
   the thresholds live in the ledger, not on the phone.
3. It packs the *pinned* evaluator ROM + expression as one argv packet and runs
   it **on the phone**, under busybox `sh` + the on-device ARM `uxncli`.
4. The receiver is the byte-identical `mesh-uxn-hop` script — it hashes the ROM
   it actually received against the declared sha1 before executing, and stamps
   the verdict with that hash.

The pin chain runs end to end: the ledger's `# evaluator-sha1:` == the ROM
packed at the workstation == the sha1 the phone verifies before executing == the
stamp that comes back. Any link broken is a loud refusal, never a wrapped
verdict.

The thing I want to underline: **the program that gates the phone does not live
on the phone.** Recalibration is a constants diff in the ledger, travelling
in-band on the next run. The phone is never edited. A 32-bit ARM core runs the
same bytes an x86 workstation assembles, judges its own battery against a
threshold it can't unilaterally change, and reports back. That's what "a ROM is
a fixed point" buys you — behavior that travels to the body and gates the body,
while staying fixed.

## The RED-first proof pattern

Every gate corrupts its own arithmetic and watches the test break:

- lease: `#0002 MUL2` → `#0001` shifts the boundary.
- band: each `GTH2` no-op'd in turn.
- calibrate: verdict logic mutated to always-AGREE, suite seen RED.
- hop: a tampered ROM is refused (declared sha1 ≠ actual).
- body-gate: the pack-site hash comparison is neutered pre-dial; a second pin
  gate at the stamp catches it — sharpening the *order* of refusal.

A gate you haven't seen fail is not a gate.

## Repro

```sh
cd scripts/uxn && ./build.sh --chibicc                          # build vendored chibicc + uxncli
./cc-rom.sh chibicc-eval/lease-gate.c lease-gate-c.rom          # .c → 468-byte .rom
MESH_LEASE_ROM=lease-gate-c.rom ./mesh-lease-gate --pair 900 1800   # → OK
./mesh-lease-audit                                              # gate the live reflex set through the ROM
```

The whole lane — hand-written gates, the C compiler, the unified runner, the
cron-wired audit, the mobile-code layer, the watcher, the calibrator, the
self-gating body — is in the repo under `scripts/uxn/`. Every piece has a
red-first test you can break.

---

I'd like feedback on three things. Is the fixed-point framing real, or am I
overloading a cute word? Is shipping executable code over SSH as a hash-verified
packet madness, or obvious once you say it? And for anyone who's targeted Uxn
from a real compiler — how far do you take it before hand assembly wins again?

# Show HN draft — Uxn ROMs as fixed points in an agent mesh

> Status: **v2 — operator review.** Rewritten from v1 (C→ROM eval) after the lane matured
> into a full system: unified runner, vendored compiler, cron-wired audit, ROM-as-packet
> mobile code, fixed-point doctrine, board watcher, calibration ledger, gates-as-data.
> Standalone Show HN candidate, distinct from the mesh-overview post (`show-hn-final.md`).

---

## The Show HN post

### Title

**Show HN: I compile C to a 468-byte ROM that runs identically on x86 and ARM** (77 chars)

Alt: **Show HN: Portable ROMs as fixed points in an agent mesh (Uxn)** (64)

### Post body

---

I run a mesh of agents on old phones. They check invariants — is a
watchdog's lease longer than twice its producer's cadence? Is the battery
in its longevity band? Is the board log monotonic?

I was checking these with `grep`. Then I audited: 33 of 52 liveness gates
could *never fail* — each `grep`'d its own source for a string, so it
always found itself. A gate you haven't seen fail is not a gate.

So I started moving them to [Uxn](https://wiki.xxiivv.com/site/uxn.html)
— the tiny virtual machine from
[Hundred Rabbits](https://100r.co). Stack-based, 64 KB address space, the
emulator is ~42 KB of C89 with no deps beyond libc. A ROM you assemble
today runs unchanged on any architecture, forever.

The first gate: a lease-vs-cadence check. Hand-written in Uxntal (the
assembly), 44 lines, **134 bytes**. Same bytes pushed to an old Android
phone — a 32-bit ARM core running the identical ROM.

Then the obvious question: can I stop writing assembly?
[chibicc](https://github.com/rui314/chibicc) is Rui Ueyama's small C
compiler; someone
[retargeted it to emit Uxntal](https://github.com/lynn/chibicc). The same
gate in 29 lines of plain C compiles to a **468-byte ROM** — truth table
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

chibicc is now vendored — one `cc-rom.sh` goes from `.c` to `.rom`. Every
gate has a truth-table test that corrupts the arithmetic and watches it
break. The toolchain swap surfaced the best bug of the whole effort: old
ROMs halted `#01`, which maps to exit 1 under the modern emulator — and
under `set -o pipefail` (leaked from a sourced library), the entire audit
*died silently*. No error, no verdict, just gone. The fix was one byte.

**Then it got interesting.** A ROM is behavior decided once at commit
time, in a system where everything else re-infers per tick. That makes it
a *fixed point* — and a fixed point is three things:

**The thing you calibrate against.** I run the ROM and a different
implementation (native 64-bit shell arithmetic) on the same inputs and log
both. Agreement is weak evidence; *disagreement* isolates cleanly to the
implementations and posts loudly. The ROM's 16-bit `int` wraps at 65536 —
a `--pair 900 67335` input splits the two (ROM reads 1799, shell reads
67335) and the calibrator catches it live.

**The thing you watch *with*.** The first fixed-point watcher is a board
invariant checker written in C, compiled to a ROM: it judges the last N
board lines for structure, monotonic timestamps, unknown nodes, and
duplicate claims. Text you control goes in; the ROM is the whole trust
boundary.

**The thing that travels.** If a ROM is a fixed point, it can move. A
ROM-as-packet over SSH: the program ships in-band with the data
(`uxp1 <rom_bytes>\n + <rom raw> + <payload>`). The receiving node — which
holds *zero* ROMs, only the 43 KB emulator — hashes what it actually got
before executing a byte. Declared hash ≠ actual is a loud refusal. A
tampered ROM that ran silently with rc=0 and empty output is
indistinguishable from consensus — so you verify, then execute.

And the latest step: a micro Lisp evaluator ROM where the *expression is
data*. The predicate `(if (>= lease (* 2 cad)) 1 0)` ships as text and the
fixed point runs it — homoiconicity on the ROM, no recompile to change a
threshold.

The whole lane — hand-written gates, the C compiler, the unified runner,
the cron-wired audit (207 reflexes), the mobile-code layer, the watcher,
the calibrator — is in the repo under `scripts/uxn/`. The design spec is
operator-approved. Every piece has a red-first test you can break.

I'd love feedback on: is the fixed-point framing real, or am I
overloading a cute word? Is shipping executable code over SSH as a
hash-verified packet madness or obvious? And for anyone who's targeted
Uxn from a real compiler — how far do you take it before hand assembly
wins again?

---

## Real artifacts (for the long version / blog)

### The hand-written gate vs. the C gate

| | hand (`lease-gate.tal`) | C (`lease-gate.c`) |
|---|---|---|
| lines | 44 | 29 |
| ROM size | 134 B | 468 B |
| authorship | stack juggling | plain C |
| `% of 64 KB` | 0.20% | 0.72% |

Both hit the same 16-bit `int` wrap ceiling (>32767 s) — parity, not a
regression. The hand ROM does its own decimal parsing in stack ops
(`#30 SUB`, `#000a MUL2`); the C version lets the compiler emit that.

### Gate classes (the pattern generalizes)

- **lease-gate** — single ratio `lease ≥ 2·cadence` (the first).
- **band-gate** — two-edged window `lo ≤ value ≤ hi` (165 B; battery,
  thermal, PSI ranges).
- **hyst-gate** — onset/recovery hysteresis carrying prior state
  (`value on off prev → ALERT/CLEAR/HOLD`) — both edges of a signal share
  one gate.
- **board-check** — structural invariants over the board log (24.7 KB;
  the 20 KB board buffer dominates).

### The unified runner (`mesh-rom-gate`)

One tool marshals `<rom> args…` → `uxncli` → verdict TEXT, rc
`0`/`1`(RED)/`2`(n/a LOUD — engine/ROM absent or broken; never a fake
verdict). Consumers keep their inline compare as the explicit rc=2
fallback and stamp `src=rom|inline-fallback`. `mesh-lease-audit` is
cron-wired (daily) and gates all 207 live reflexes through the ROM.

### The fixed-point doctrine

A ROM is the mesh's first fixed point — behavior decided once at commit
time. Three uses:

1. **Calibration** (`mesh-rom-calibrate`, cron-wired) — run the ROM +
   native shell on identical inputs, log every pair (stamped with the
   ROM's sha1). Disagreement posts `[chat-review]` loudly; agreement logs
   silently. First live run: 208 pairs, 0 diverged.
2. **Watching** (`board-check.c` → ROM, cron `*/10`) — structural board
   invariants: `ts who@host :: body`, monotonic ISO8601 timestamps, known
   nodes, no duplicate claims. Input is staged text; the ROM is the trust
   boundary.
3. **Mobile code** (`mesh-uxn-hop`) — ROM-as-packet over SSH. `--pack`
   declares the sha1 in-band; the receiver hashes before executing;
   `UXN_HOP_STAMP=1` stamps stderr with what it really ran. `route.rom`
   (263 B) demuxes two output channels over one pipe by shipped code.

### Gates-as-data (`lisp-eval.c` → 3.9 KB ROM)

Micro s-expression evaluator over naturals 0..65535. The predicate is
argv DATA the fixed point runs — `(if (>= lease (* 2 cad)) 1 0)` passes
the lease truth table. NA/#82 honesty: overflow, `/0`, unknown op, bad
parens all answer NA, never a wrapped value. Lease-gate and band-gate now
express as s-expr data lines under the evaluator (gates-as-data stage 1).

### The RED-first proof pattern

Every gate corrupts its own arithmetic and watches the test break:
- lease: `#0002 MUL2` → `#0001` shifts the boundary.
- band: each `GTH2` no-op'd in turn.
- calibrate: verdict logic mutated to always-AGREE, suite seen RED.
- hop: tampered ROM refused (declared sha1 ≠ actual).

A gate you haven't seen fail is not a gate.

### Repro (chibicc now vendored)

```sh
cd scripts/uxn && ./build.sh --chibicc      # build vendored chibicc
./cc-rom.sh chibicc-eval/lease-gate.c lease-gate-c.rom   # .c → .rom
./mesh-rom-gate lease-gate-c.rom 900 1800   # → OK
```

---

## Notes for the operator

- **Repo link:** `scripts/uxn/` (README is public-ready, full lane
  documented). Eval detail in `chibicc-eval/EVAL.md`; design spec in
  `docs/superpowers/specs/2026-07-23-uxn-predicate-engine-design.md`.
- **Tone:** flat and specific throughout. The three-act structure
  (calibrate → watch → travel) is the payoff; the C→ROM experiment is the
  accessible entry. The pipefail silent-death story stays — it's the kind
  of concrete wart HN rewards.
- **Both v1 open items are closed:** toolchain vendor-swap (`223d9c8`) and
  chibicc vendored (`ba7944d`). Zero TODO loose ends.
- **The three feedback questions** target the three real open decisions:
  (1) is "fixed point" a real concept or overloading, (2) hash-verified
  mobile code over SSH — madness or obvious, (3) how far does C→Uxn go
  before hand assembly wins.
- **Relationship to the mesh post (`show-hn-final.md`):** different
  audience overlap. This one stands alone for the Uxn/compilers/small-
  computing crowd; the mesh post is for the infra/agent crowd. Posting
  both is fine — different hooks.

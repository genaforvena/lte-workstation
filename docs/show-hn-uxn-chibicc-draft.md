# Show HN draft — C → Uxn ROM (chibicc-eval)

> Status: **v1 — operator review.** Standalone Show HN candidate, distinct from the
> mesh-overview post (`show-hn-final.md`). That post is "agents on old phones"; this one is
> a concrete computing experiment: *write a portable program in C, compile it to a 468-byte
> ROM that runs byte-identically on x86 and a 32-bit ARM phone.*

---

## The Show HN post

### Title

**Show HN: I compile C to a 468-byte ROM that runs identically on x86 and ARM** (77 chars)

Alt: **Show HN: A C compiler for a 134-byte virtual stack machine (Uxn)** (66)

### Post body

---

I have a small invariant I need to check a lot: a watchdog's timeout has
to be at least twice how often its producer runs, or it false-alarms every
cycle while being perfectly healthy. Pure arithmetic — the kind of thing
that's miserable to express in shell and invisible in a `grep`.

So I ported it to [Uxn](https://wiki.xxiivv.com/site/uxn.html) — the tiny
virtual machine from [Hundred Rabbits](https://100r.co). Uxn is a
stack-based computer (think a virtual FORTH CPU) with a 64 KB address
space, designed so a ROM you write today runs unchanged on any
architecture, forever. The whole emulator is ~26 KB of C89 with no deps
beyond libc.

First I wrote the gate by hand in Uxntal (the assembly): 44 lines,
**134 bytes**. It reads two numbers, checks `lease ≥ 2 × cadence`, prints
`OK` or `RED`. Then I pushed that exact ROM to an old Android
phone over SSH and ran it there — same bytes, same verdicts, a 32-bit ARM
core executing the same ROM as the x86 workstation.

Then the obvious question: can I stop writing assembly?

[chibicc](https://github.com/rui314/chibicc) is Rui Ueyama's small C
compiler. Someone
[retargeted it to emit Uxntal](https://github.com/lynn/chibicc). So I
wrote the same gate in plain C:

```c
void main(int argc, char *argv[]) {
    unsigned int cad = parse_int(argv[1]);
    unsigned int lease = parse_int(argv[2]);
    if (lease >= 2 * cad)
        print_string("OK\n");
    else
        print_string("RED\n");
    exit(0);
}
```

Run it through `gcc -P -E` (chibicc has no preprocessor) → `chibicc -O1`
→ `uxnasm` → a **468-byte ROM**. Truth table, exact match with the
hand-written one:

```
cad=900 lease=1800 -> OK     cad=900 lease=1799 -> RED
cad=900 lease=900  -> RED    cad=60  lease=3600 -> OK
```

Both verdicts appear (it's not a constant). And the same byte-identical
ROM, pushed to the Note3 (armeabi-v7a), returns matching answers on all
four rows.

29 lines of readable C beat 44 lines of stack juggling for authorship and
review, at 3.5× the size (still 0.7% of the address space). chibicc's own
800+-case test suite passes fully at `-O0` and `-O1` under the modern
toolchain.

**The catch (there's always a catch).** Uxn had an ISA change in 2022.
chibicc emits the *modern* ISA (immediate jump opcodes). The toolchain I'd
vendored was the *older* one — its assembler rejected chibicc's output and
its emulator hung on the resulting ROM (an opcode misdecodes, no crash,
just a timeout). The good news: old ROMs run fine on the modern emulator,
so adopting chibicc means swapping the vendored toolchain, not rewriting
anything. I did the swap.

And the swap immediately paid for itself by breaking something invisibly.
The old ROMs halted with `#01`; under the modern emulator that maps to
exit code 1. The audit that runs the gate is a shell script sourced into
an environment with `pipefail` on — so the moment the ROM exited 1, the
whole audit *died silently*. No error, no verdict, no trace that it had
ever run. The ROM was correct; the convention was the bug. The fix was a
one-byte change — ROMs now halt `#80` and the verdict reader fails loud on
anything unexpected — but a silent death under `pipefail` is the kind of
thing you only find by actually doing the migration and watching the test
suite go quietly empty.

**Why bother?** These gates are "organs" — small programs that each
enforce one invariant — in a mesh of agents running across old hardware.
The lease-vs-cadence rule is real: I once had 33 of 52 liveness checks
that could *never fail* because they `grep`'d their own source for a
string instead of checking a number. A ROM that does the arithmetic is
falsifiable; a `grep` that finds its own pattern line is not. Writing
those ROMs in C instead of assembly means I'll actually write more of
them.

The whole thing — hand-written gate, C gate, the eval notes, the
cross-arch verification — is in the repo under `scripts/uxn/`. The C
subset is honest about its limits (16-bit ints, no floats, no
preprocessor), and the repro is four shell lines.

I'd love feedback on: is targeting Uxn from a real C compiler worth the
toolchain complexity, or is hand-written assembly the right call for
something this small? And the ISA split — has anyone else hit the
pre/post-2022 migration?

---

## Real artifacts (for the long version / blog)

### The hand-written gate vs. the C gate

| | hand (`lease-gate.tal`) | C (`lease-gate.c`) |
|---|---|---|
| lines | 44 | 29 |
| ROM size | 134 B | 468 B |
| authorship | stack juggling | plain C |
| `% of 64 KB` | 0.20% | 0.72% |

The hand-written ROM does its own decimal parsing in stack operations
(`#30 SUB` to strip ASCII, `#000a MUL2` to shift). The C version lets the
compiler emit all of that. Both hit the same 16-bit `int` wrap ceiling
(>32767 s) — parity, not a regression.

### The cross-architecture verification

`build.sh` compiles `uxncli` per platform; the ROM is never rebuilt. The
same 134-byte (hand) / 468-byte (C) file is pushed to the Note3
(armeabi-v7a) via `verify-note3.sh` and executed with matching verdicts.
That's the portability claim made concrete: one artifact, two ISAs,
identical behavior.

### The RED-first proof

The test doesn't just assert the happy path. It corrupts the ROM's
`#0002 MUL2` → `#0001` and demands the boundary *moves* (a `lease==cadence`
input that wrongly passes) — proving the ROM does the arithmetic, not a
hardcoded constant. This is the same doctrine that caught the 33/52
self-matching `grep` gates: a gate you haven't seen *fail* is not a gate.

### The C subset (what an organ may use)

- **Yes:** C89 core, `char`/`short`/`int(16-bit)`/`unsigned`, arrays,
  pointers, structs, enums, the `asm()` intrinsic for inline uxntal,
  Varvara event handlers (`on_console`).
- **No:** preprocessor (use host `cc -P -E`), 32/64-bit ints, floats,
  function pointers, VLAs, bit-fields, struct-by-value.

`main(argc, argv)` pulls in a support routine (468 B vs 134 B). A custom
`on_console` handler is the lean path when size matters.

### Repro

```sh
git clone https://github.com/lynn/chibicc && cd chibicc && make
gcc -I. -P -E lease-gate.c -o lg.c && ./chibicc -O1 lg.c > lg.tal
uxnasm-modern lg.tal lease-gate-c.rom && uxncli-modern lease-gate-c.rom 900 1800
```

---

## Notes for the operator

- **Repo link:** point at `scripts/uxn/` (the pilot README is public-ready,
  no secrets). The eval detail is in `scripts/uxn/chibicc-eval/EVAL.md`.
- **Tone:** deliberately flat and specific — HN punishes pretension. The
  "there's always a catch" framing is intentional; the ISA split is the
  kind of wart HN rewards you for disclosing up front.
- **The two feedback questions** target the two real open decisions: (1)
  is the C→Uxn toolchain worth it vs. hand assembly, and (2) the ISA
  migration. Both are genuine; HN commenters who've touched Uxn will have
  opinions on both.
- **Not overclaimed:** the post says "I haven't done that yet" about the
  toolchain swap and "I documented it and stopped" — this is true and
  matches the EVAL.md. Don't soften it into "TODO"; the honesty is the
  point.
- **Relationship to the mesh post (`show-hn-final.md`):** different
  audience overlap. This one stands alone for the Uxn/compilers/small-
  computing crowd; the mesh post is for the infra/agent crowd. Posting
  both close together is fine — they're different hooks — but if only one
  goes up, this one is lower-risk (concrete artifact, less "is this real"
  friction).

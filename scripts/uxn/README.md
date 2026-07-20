# uxn-pilot-gate — a mesh reflex gate as a portable Uxn ROM

**Operator eval (2026-07-20):** can a real reflex gate be a tiny, portable
[Uxn](https://wiki.xxiivv.com/site/uxn.html) ROM instead of host shell? Port one gate,
prove it catches a real regression the canonical *self-grep* gate is blind to, and run the
**byte-identical ROM** on both the x86 workstation and the 32-bit ARM Note3.

## What was ported

`mesh-reflex-health`'s **lease-vs-cadence invariant** (`eff_maxage @auto`): a watchdog's
lease/max-age **must be ≥ 2× the producer's cron cadence**, or the reflex reads `STALE`
every cycle while perfectly healthy (memory: `a-lease-must-exceed-its-producers-cadence`).
Pure arithmetic — the ideal first thing to move off shell into a stack machine.

- **`lease-gate.tal`** — the gate, 44 lines of uxntal. Reads `cadence` then `lease` as
  newline-terminated argv tokens, parses decimal in-ROM, computes `lease ≥ 2·cadence`,
  prints `OK` / `RED`, halts.
- **`lease-gate.rom`** — assembled, **133 bytes**. This is the portable artifact.
- **`mesh-lease-gate`** — the host shim (**~20 lines of logic**). Resolves a reflex's
  `(cadence, lease)` from a fixtures table (or `--pair a b`) and hands the two integers to
  the ROM. The gate *logic* is in the ROM; the shim only marshals inputs and maps the
  verdict to exit 0 / 1.
- **`lease-fixtures`** — `name cadence lease` rows (stand-in for the live cron + lease decls).
- **`src/`, `build.sh`** — vendored Uxn toolchain (`uxnasm` + `uxncli`, MIT, Devine Lu
  Linvega et al.). `build.sh` compiles the ~26 KB emulator **per platform**; the ROM it runs
  is identical everywhere.

## Build & run

```sh
./build.sh --rom                 # compile uxnasm+uxncli for this host, assemble the ROM
./mesh-lease-gate ambient-clock  # resolve from fixtures -> OK/RED, exit 0/1
./mesh-lease-gate --pair 900 900 # gate two raw integers -> RED (lease==cadence)
./test-lease-gate                # the RED-first proof
```

## The RED-first proof (`test-lease-gate`)

The doctrine's canonical vacuous gate is a **self-grep**: `grep -q '2*cadence' "$0"` — it
asserts a *string is present in the source*, never that the *number is right*, and so can
never fail on bad data (CLAUDE.md, the 33/52 self-matching-gate sweep 1969a5d).

We break the guarded fix — a reflex whose **lease drops to 1× its cadence** (the real
regression) — and watch the two gates disagree:

| input `cad=900 lease=900` | self-grep gate | ROM gate |
|---|---|---|
| verdict | **GREEN** (string still present — blind) | **RED** (900 < 1800 — caught) |

Seen RED-first: the ROM truth table asserts the boundary is inclusive (`1800` OK, `1799`
RED, `1801` OK) and that `lease==cadence` goes RED; corrupting the ROM's `#0002 MUL2` → `#0001`
makes the bug config wrongly pass, proving the ROM does the arithmetic, not a constant.

## Portability (same ROM, two architectures)

`build.sh` on each node compiles its own `uxncli`; **`lease-gate.rom` is never rebuilt**.
See `verify-note3.sh` for the aarch/armhf cross-build + push + on-device run that executes
the identical 133-byte ROM on the Note3 (armeabi-v7a) with matching verdicts.

## Measurements

- **ROM:** 133 bytes (0.20% of the 64 KB Uxn address space).
- **Shim:** ~20 lines of logic.
- **Runtime:** ~0.66 ms/run (process spawn + emulator boot + ROM eval), RSS ~1.5 MB, x86.
- **Emulator:** `uxncli` ~26 KB, `uxnasm` ~21 KB, C89, no deps beyond libc.

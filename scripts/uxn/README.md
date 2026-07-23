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
- **`lease-gate.rom`** — assembled, **134 bytes**. This is the portable artifact.
- **`mesh-lease-gate`** — the host shim (**~20 lines of logic**). Resolves a reflex's
  `(cadence, lease)` from a fixtures table (or `--pair a b`) and hands the two integers to
  the ROM. The gate *logic* is in the ROM; the shim only marshals inputs and maps the
  verdict to exit 0 / 1.
- **`lease-fixtures`** — `name cadence lease` rows (stand-in for the live cron + lease decls).
- **`mesh-lease-audit`** — the **load-bearing live resolver** (the fixtures stand-in was a mock).
  It gates the WHOLE live reflex set through the same ROM: for every reflex that self-declares a
  `# reflex-cadence:` header it resolves two *independent* integers — **cadence** from the header
  (what the reflex says it runs at) and **lease** from `mesh-reflex-health`'s `eff_maxage` (what
  its liveness watchdog tolerates) — and hands them to the ROM. See "Live audit" below.
- **`band-gate.tal` / `band-gate.rom` / `mesh-band-gate`** — a **second gate CLASS**: a compound
  two-edged boundary `lo ≤ value ≤ hi`, RED past either edge. Proves the ROM pattern generalizes
  beyond lease's single `≥` comparison. See "Second gate class" below.
- **`src/`, `build.sh`** — vendored Uxn toolchain (`uxnasm` + `uxncli`, MIT, Devine Lu
  Linvega et al.). **Modern post-2022 ISA** (JCI/JMI/JSI) — vendor-swapped 2026-07-23 from
  `~rabbits/uxn` (uxnasm from `archive/`, uxncli+core from `src/` @ `43453d7`; provenance in
  `build.sh`) so chibicc-compiled ROMs run (`chibicc-eval/EVAL.md`); the pre-2022-ISA
  toolchain it replaced lives in git history. `build.sh` compiles the ~42 KB emulator **per
  platform**; the ROM it runs is identical everywhere. Halt convention is modern: ROMs end
  with `#80 #0f DEO` (exit code = `state & 0x7f` = 0 when a verdict was rendered) — the
  verdict itself is TEXT (`OK`/`RED`), never the exit code.

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

## Live audit (`mesh-lease-audit`) — the resolver made load-bearing

The pilot's first cut resolved `(cadence, lease)` from the static `lease-fixtures` mock.
`mesh-lease-audit` replaces that with the **live genome**: it sources `mesh-reflex-health`
(one authority — the shared `cron_stride_from_fields` + `eff_maxage`, never a duplicated
parse), resolves every `# reflex-cadence:` header (242 in `scripts/`), and gates each pair
through `lease-gate.rom`.

```sh
./mesh-lease-audit          # -> "lease-audit: clean — 201 reflex(es) gated, ... (35 un-derivable skipped)"
./mesh-lease-audit --list   # also print every resolved (name cad lease OK/RED) row
```

**Why a healthy fleet audits CLEAN, and that is honest.** `eff_maxage`'s `@auto` derives
`lease = cadence × 2` **by design** — the maxage-from-cadence machinery
(`mesh-reflex-health`, chat-review 2026-06-24) exists precisely to make `lease < 2·cadence`
impossible to express by accident. So the live audit finds **zero** violations. This is not a
dud gate — it is a **regression guard**, not a bug-finder:

- the day `eff_maxage`'s `s*2` is edited to `s*1`, **every** reflex here flips RED;
- the day a watchdog lease is hardcoded to a literal below `2·cadence` (the
  `a-lease-must-exceed-its-producers-cadence` memory), **that** reflex flips RED.

The 35 skipped reflexes carry list-crons (`17,47 …`) or `# reflex-cadence: none` — no single
derivable cadence — and are honestly excluded, never silently passed. `test-lease-audit` is
the RED-first proof for the **wiring** (not just the ROM): it points the audit at a
`mesh-reflex-health` whose `eff_maxage` multiplier is broken (`s*1`) and asserts the audit
flips from clean(0) to violation(1) on the same reflex, then that the real genome is clean.

## Second gate class (`band-gate` — a compound boundary predicate)

To show the ROM pattern is not a one-off, a **structurally different** gate is ported: a
two-edged band `lo ≤ value ≤ hi` (RED past *either* edge), vs. lease's single ratio `≥`.
Same portable-artifact story — a 165-byte ROM, byte-identical everywhere; the shim is I/O only.

```sh
./bin/uxnasm band-gate.tal band-gate.rom
./mesh-band-gate 20 55 80                       # -> OK  (within band)
./mesh-band-gate 20 92 80                       # -> RED (above the band)
./mesh-band-gate --name battery 92 band-fixtures # resolve [lo,hi] for a named band, gate the value
./test-band-gate                                # RED-first proof
```

`test-band-gate` proves both edges are real arithmetic, not a constant: it corrupts each
`GTH2` comparison in turn (to a no-op) and demands a genuinely out-of-band value then *wrongly*
passes — so the uncorrupted ROM's RED is the lo edge AND the hi edge, not one of them. Real mesh
use of a two-edged window: a Li-ion longevity band (20–80%), an NVMe thermal window, a healthy
PSI range (`band-fixtures`).

## Portability (same ROM, two architectures)

`build.sh` on each node compiles its own `uxncli`; **`lease-gate.rom` is never rebuilt**.
See `verify-note3.sh` for the aarch/armhf cross-build + push + on-device run that executes
the identical 134-byte ROM on the Note3 (armeabi-v7a) with matching verdicts (re-verified
under the modern toolchain 2026-07-23, sha1 `442120b…` host==device).

## Measurements

- **ROM:** 134 bytes (0.21% of the 64 KB Uxn address space).
- **Shim:** ~20 lines of logic.
- **Runtime:** ~0.66 ms/run (process spawn + emulator boot + ROM eval), RSS ~1.5 MB, x86;
  measured on the pre-swap emulator, same order of magnitude on the modern one.
- **Emulator:** `uxncli` ~42 KB, `uxnasm` ~21 KB, C89, no deps beyond libc.

## Predicate-engine lane (2026-07-23, operator-approved spec)

Design: `docs/superpowers/specs/2026-07-23-uxn-predicate-engine-design.md`. **Doctrine: a new
pure predicate defaults to a ROM gate run via `mesh-rom-gate`; self-grep gates remain banned;
plumbing stays shell.** The lane's moving parts:

- **`scripts/mesh-rom-gate`** (deployed) — the ONE runner: `mesh-rom-gate <rom> args…` prints the
  ROM's verdict TEXT, rc `0` (not RED) / `1` (RED) / `2` (n/a LOUD — engine/ROM absent or broken;
  never a fake verdict). Bare names resolve to `scripts/uxn/<name>.rom`. Consumers keep their
  inline compare as the explicit rc=2 fallback and stamp `src=rom|inline-fallback`.
- **`mesh-lease-audit`** — wired into cron via the `scripts/mesh-lease-audit` deploy shim
  (`# reflex-cadence: 41 5 * * *`); its wired `--test` runs the full `test-lease-audit` suite.
- **`chibicc/`** — vendored C→uxntal compiler (provenance in `build.sh`); `./build.sh --chibicc`
  builds it, `./cc-rom.sh <src.c> <out.rom>` compiles a gate, `./test-chibicc` is the truth-table
  vendor gate (RED-first, byte-identity informational only).

## Hop lane — ROM-as-packet over ssh (2026-07-23, operator spike → tool)

Transport stays ssh/tailscale; uxn is the **mobile-code layer**: the program travels
in-band with the data. Proven live against phaedra holding ZERO ROMs — only `uxncli`
(43 KB) + `mesh-uxn-hop` (3 KB) — with two different behaviors through the same channel.

- **`mesh-uxn-hop`** — the packet runner. Format `uxp1 <rom_bytes>\n + <rom raw> + <payload…>`.
  `--pack <rom>` builds a packet from stdin payload; bare invocation receives one, runs the
  shipped ROM on the payload in a FRESH EMPTY tempdir (uxncli's file device is cwd-sandboxed,
  `file_check_sandbox`), propagates the ROM's exit code, and fails LOUD (rc 65) on any
  malformed/truncated packet — never a silent passthrough.
  One hop: `mesh-uxn-hop --pack filter.rom < text | ssh node mesh-uxn-hop`
- **`rot13.tal`/`rot13.rom`** (106 B) — the canonical pipe-stage payload; also documents the
  console idiom for stream filters (stdin type 1, EOF type 4 → halt `#80`).
- **`test-uxn-hop`** — RED-first suite (11 asserts): pack byte-accounting, shipped-code
  execution, hop composition (double-rot13 identity), loud malformed/truncated failure with
  empty stdout, rc propagation (`#81`→1), fresh-empty-cwd containment, sha1 declaration,
  tamper refusal, stamp correctness (declared and legacy-undeclared).
- **Run-time hash verification (the fixed-point doctrine, operator 2026-07-23):** a ROM is
  the mesh's first FIXED POINT — behavior decided once at commit time, in a system where
  everything else re-infers per tick. That only holds if the hash is VERIFIED AT RUN TIME,
  not claimed: `--pack` declares the ROM's sha1 in the header (`uxp1 <n> <sha1>`), the
  receiving hop hashes what it ACTUALLY got before executing a byte — declared≠actual is a
  loud rc-65 refusal, and `UXN_HOP_STAMP=1` appends `hop: rom sha1=<actual> declared=<…>
  rc=<n>` to stderr so the verdict is stamped by the execution site with what it really ran.
  (Undeclared legacy headers run but stamp `declared=none` — visible, never silent. The
  tamper test is instructive: a corrupted rot13.rom ran SILENTLY with rc=0 and empty output
  — identical wrongness is indistinguishable from consensus, hence verify-then-execute.)
- **`route.tal`/`route.rom`** (263 B) — the prefix router: first payload line = the prefix
  (config travels in-band too), then each line starting with it → stdout, rest → stderr.
  Two output channels over one ssh pipe, demuxed by shipped code; `test-uxn-route` covers
  demux, exact-prefix, empty-prefix, mid-prefix reject replay, EOF partial, and riding the
  hop. Proven live against phaedra with the stamp confirming the executed sha1.

Next rungs (open): per-hop source routing (each leg of a multi-hop path carries its own
program); rom-vs-agent calibration ledger (run the ROM and a mind on the same predicate,
log both — agent divergence becomes measurable against the fixed point).

## Board invariant watcher (2026-07-23, operator: "the first one to actually write")

`board-check.c` (chibicc-C → `board-check.rom`, 24.7 KB — the 20 KB board buffer dominates)
— the first fixed-point WATCHER: judges the last N board lines against structural invariants
so silent dropped directives are caught without an agent having to notice. Input staged as
files in the cwd sandbox (`./nodes`, `./board`) — text you control; the ROM is the whole
trust boundary. Invariants: STRUCTURE (`ts  who@host  ::  body`), MONOTONIC (bytewise
ISO8601Z, 0 inversions in the last 2000 live lines), UNKNOWN-NODE (host ∈ nodes set),
DOUBLE-TAKING (byte-identical claim text, `[done]`-released). Verdict text is canon: detail
`RED <INV>: <offending line>` per hit, last line `OK n=…`/`RED v=…`/`UNKNOWN <reason>`,
rc 0/1/2 mirrors. UNKNOWN is honest n/a (empty input, at-capacity, taking-table overflow).
`mesh-board-check` (+ deploy shim in `scripts/`, `# reflex-cadence: */10 * * * *`) stages
the live board (auto-halves N to fit the ROM buffer), stamps the verdict with the sha1 it
ACTUALLY hashed pre-exec, keeps `~/.mesh/board-check.state` (liveness-touch every eval,
content on class change), and posts BOTH edges (onset and recovery, one gate).
`test-board-check`: 10 sections — every invariant both polarities, honest UNKNOWNs, a
gutted-MONOTONIC mutation that the fixtures must catch, and the wrapper driven end-to-end.

## Calibration ledger (2026-07-23 — the oracle use of the fixed point)

`mesh-rom-calibrate` (+ deploy shim, `# reflex-cadence: 7 6 * * *`) runs BOTH
implementations of a predicate on identical inputs — the ROM (16-bit, via
`mesh-rom-gate`) and native shell arithmetic (64-bit, a genuinely different
implementation) — and appends every pair to `~/.mesh/rom-calibration.log`,
each line stamped with the sha1 of the ROM actually hashed. Doctrine: under
the same ROM, DISAGREEMENT isolates cleanly to the implementations and posts
`[chat-review]` loudly; AGREEMENT is weak evidence and logs silently. This
keeps the N-version diversity signal alive that ROM uniformity destroys.
v1 predicate: lease-vs-cadence over the same rows `mesh-lease-audit --list`
resolves. Known divergence domain, provable live: the ROM's 16-bit parse wraps
at 65536 — `--pair 900 67335` reads lease as 1799 → rom=RED shell=OK DIVERGE
(the test suite drives this REAL split, not a mock). First live fleet run:
208 pairs, 0 diverged. `test-rom-calibrate`: 6 sections; the verdict logic was
mutated to always-AGREE and the suite seen RED (fixtures discriminate).

# mesh-uxn-core

**The gates, senses and predicates of a computer mesh, compiled to tiny
[Uxn](https://wiki.xxiivv.com/site/uxn.html) ROMs** — artifacts from 72 bytes to 25 KB that run
byte-identically on an x86 workstation, a server, and a 2013 Android phone, instead of host
shell that rots differently on each of them.

Everything needed to build and run it is in this repository: a stock Uxn emulator (`src/`),
the chibicc C→uxntal compiler (`chibicc/`), the ROMs (`*.tal`/`*.c` → `*.rom`), their host
shims (`mesh-*`), and a test per ROM that was **seen failing before it passed** (`test-*`).

```sh
./build.sh --rom                 # build uxnasm + uxncli for this host, assemble every ROM
./mesh-lease-gate --pair 900 900 # decide a real invariant  ->  RED, exit 1
./test-lease-gate                # the proof: break the ROM's arithmetic, watch it go red
```

## Why a ROM instead of a shell script

A mesh reflex is guarded by a *gate*: a small predicate that says whether a reading is
healthy. Written in shell, the commonest form of that gate is

```sh
grep -q '2*cadence' "$0"     # "the formula is in my source, so I must be correct"
```

which asserts that **a string exists in its own text**, does no arithmetic, and therefore
can never fail on bad data. A sweep of the parent mesh found 33 of 52 such gates matching
nothing but themselves.

A gate compiled to a stack machine has nowhere to hide: it consumes the numbers and returns
a verdict. Corrupt the ROM's math and its test goes red. And because the ROM is a **fixed
point** — decided once at assembly time, byte-identical afterwards — the workstation and
the phone cannot quietly disagree about what the rule was.

Three properties follow, and they are what this repository is really about:

| | |
|---|---|
| **Portable** | the emulator is per-platform (~56 KB of C89); the ROM above it is one file, unchanged everywhere |
| **Pinnable** | a ROM has a sha1 that can be declared, shipped, and **verified at the moment of execution** rather than claimed |
| **Mobile** | a ROM is small enough to travel *in-band with its data* — over a pipe, over ssh, or over a socket into an emulator that becomes it |

## The five rules every ROM here follows

1. **The test must have been red.** Each `test-*` rebuilds its ROM from deliberately
   corrupted source and requires the truth table to fail. A table that cannot fail is not a
   table.
2. **Absence answers `NA`, never a number.** No engine, no ROM, no reading → verdict text
   `NA`, exit code 2, reason on stderr. A silent default is a failure wearing a success's
   clothes.
3. **The verdict is text; the exit code only mirrors it.** `OK`/`RED`/`NA` → 0/1/2.
4. **Out of domain is not a wrapped answer.** The machine is 16-bit; overflow, underflow,
   `/0`, bad arity and oversize input all answer `NA` rather than a plausible wrong number.
5. **Hash, then execute.** Any ROM that arrives from somewhere else is hashed against a
   declared sha1 *before* a byte of it runs, and the execution site stamps what it actually
   ran.

## What's in the box

### Gate ROMs — one predicate, one artifact

| ROM | size | decides |
|---|---:|---|
| `lease-gate` | 200 B | a watchdog's lease is ≥ 2× the producer's cadence (else the reflex reads STALE while healthy) |
| `band-gate` | 165 B | a two-edged window `lo ≤ v ≤ hi` — a battery longevity band, a thermal window |
| `hyst-gate` | 582 B | hysteresis: onset and recovery decided by **one** gate carrying prior state |
| `sense-gate` | 305 B | a sensor read is *real* — enough axes, recent enough, and it moved (the hollow-sense signature) |
| `permcheck` | 1013 B | a claimed-sorted stream is a genuine permutation of the original, one streaming pass — verify, don't recompute |
| `board-check` | 24.7 KB | structural invariants over a coordination log: line shape, timestamp monotonicity, unknown node, double-claim |

### Measurement ROMs — reduce a series to one calibrated number

| ROM | size | answers |
|---|---:|---|
| `spearman` | 1307 B | rank correlation `rho×1000`, integer, no floats, up to n=2343 |
| `series-stats` | 1365 B | `min max med2 cnt sum mean1000`; `med2` is twice the median so even-n is exact |
| `fletcher16` | 160 B | a rolling checksum whose *function* is itself a pinned, verifiable artifact |

### Arithmetic limbs — the ceiling on a 16-bit machine, lifted twice

| ROM | size | provides |
|---|---:|---|
| `arith32` | (library) | 32-bit add/sub/cmp/mul — what took `spearman` from a 58-row demo to the real series |
| `arith64` | (library) | 64-bit quad-word add/sub/cmp/mul/accumulate, same discipline, fully unrolled |

Both ship a self-testing ROM (`arith32-test`, `arith64-test`) whose boundary table is the
authority for carry coverage. Their lesson, learned the hard way: **the max-domain input is
the weakest place to hunt a carry bug** — a lost high word disappears below the printed
resolution exactly where the numbers look most impressive.

### Network ROMs — the emulator gets an addressable socket (device `0xd0`)

| ROM | size | does |
|---|---:|---|
| `net-echo` | 297 B | dial a `tcp:host:port`, write, read, print the reply — the smallest real round trip |
| `net-listen` | 328 B | bind, wait for a caller, answer with `uxn:`+payload — the far node needs no shell |
| `net-dgram` | 335 B | bind a DATAGRAM on a named address, read one packet, answer `uxn:`+payload to its sender |
| `net-ident` | 72 B | probe which step of the device this emulator actually has (a net-blind build must not read as a refusal) |
| `sysfs-serve` | 338 B | serve a phone's sysfs over TCP — a sense transport for a body whose ssh is gone |

### Mobile code — a program travelling with its data

| ROM | size | does |
|---|---:|---|
| `rot13` / `route` | 106 / 263 B | the canonical pipe-stage payloads: a filter, and a prefix router that demuxes two channels over one pipe |
| `hop-dial` / `hop-serve` | 434 / 1380 B | the net lane: `hop-serve` reads an arriving ROM, relocates a position-independent copier, and **becomes it** — holding the live connection across the swap |
| `lisp-eval` | 3992 B | a micro s-expression evaluator: the *predicate itself* is data, so recalibration is a text diff, not a rebuild |

### Host shims — the shell that marshals, never decides

`mesh-lease-gate` · `mesh-band-gate` · `mesh-sense-gate` · `mesh-board-check` ·
`mesh-spearman` · `mesh-series-stats` · `mesh-sexpr-gate` · `mesh-uxn-hop` ·
`mesh-body-gate` · `mesh-note3-uxn-accel` — each one resolves inputs, runs a ROM, maps the
verdict to an exit code. The logic stays in the ROM; if a shim starts deciding things, that
is the bug.

Four are audits and watchers rather than single gates: **`mesh-lease-audit`** puts the whole
live reflex set through `lease-gate.rom`; **`mesh-rom-calibrate`** runs the ROM *and* native
64-bit shell arithmetic on the same inputs and logs every pair, so agreement is weak evidence
and disagreement is loud; **`mesh-log-attest`** makes an append-only log's append-only-ness
verifiable instead of conventional; **`mesh-uxn-drift`** watches the one thing that *can*
drift — the emulator binary, since the ROMs cannot.

## Portability — one ROM, four platforms

`build.sh` builds the emulator for the host; `cross-build.sh arm64|armhf` cross-builds a
static one to push to a phone. The ROM is never rebuilt.

| target | emulator | status |
|---|---|---|
| x86_64 host | 56,856 B dynamic | the build and test platform |
| armhf (Note3, 2013, armeabi-v7a) | 674,652 B static | **verified on the device** — identical ROM, matching verdicts, binds and answers a dial from the workstation |
| arm64 (Android 8+ bodies) | 1,013,392 B static | built and driven under `qemu-user`; **no physical device has run it yet** |
| x86_64 peer, no compiler | pushed binary | serves a ROM shipped over the tailnet |

`--check` drives the cross-built binary instead of describing it: it must **compute** the
truth table, **identify** the net device, and **accept** a real inbound connection. No qemu
for that arch → exit 2, honest n/a, reported as built-but-not-run.

The furthest this goes: the workstation ships `rot13-net.rom` over TCP to a 2013 phone
carrying **only a static `uxncli`** — no shell, no ssh, no scripts — and the phone's
emulator replaces itself with the arriving code and answers `Uryyb sebz zrfu-ubzr`.

## Layout

```
*.tal  *.c      ROM sources (uxntal, or C compiled by the vendored chibicc)
*.rom            the assembled artifacts — the portable thing
mesh-*           host shims: marshal inputs, run a ROM, map the verdict
test-*           one RED-first suite per ROM
build.sh         host build (uxnasm + uxncli + assemble ROMs)
cross-build.sh   static arm64 / armhf emulator for a phone
verify-note3.sh  cross-build -> adb push -> run on the device -> compare
src/             vendored Uxn emulator + the 0xd0 net device
chibicc/         vendored C -> uxntal compiler
docs/LANES.md    the full engineering log: every lane, its proof, and its limits
```

## Details

[**`docs/LANES.md`**](docs/LANES.md) is the chronological record — each lane, the regression
it catches, the mutant that had to make it red, and what each claim deliberately does *not*
cover. Start there for any single piece; this page is only the map.

## License

**[CC0 1.0 Universal](LICENSE)** — our code here is public domain, no attribution required.

The vendored third-party trees are **not** ours to relicense and keep their own terms:
`src/` (Uxn, Devine Lu Linvega et al.) and `chibicc/` are each upstream MIT under their own
`LICENSE` files; provenance is recorded in `build.sh`.

> Extracted from the `lte-workstation` mesh genome as a standalone, shareable core.

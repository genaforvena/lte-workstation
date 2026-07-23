# uxn predicate-engine lane — design (2026-07-23, operator-approved)

**Decision:** uxn integrates tighter with the mesh in ONE lane — **gate-class organs**
(pure predicates) — not as a general substrate. Rationale: the mesh's largest recurring
failure class is the vacuous gate (33/52 self-grep gates asserted nothing, sweep 1969a5d;
plus the silent-fallback / constant-verdict family in memory). A ROM gate is structurally
immune: it computes the predicate, its truth table is provable red-first, and the
byte-identical artifact runs on every node (x86 + Note3 armhf verified). chibicc makes
authorship cheap (29 lines C → 468 B ROM). Most mesh failures live in plumbing the shims
still own — so uxn owns the arithmetic, shell keeps the marshaling.

Pilot state this builds on: `scripts/uxn/` — modern post-2022 ISA toolchain vendored
(223d9c8), lease-gate + band-gate ROMs with red-first suites, `mesh-lease-audit` live
resolver (NEVER cron-wired — a doctrine violation this design closes), chibicc C→ROM
proven (429f c3d, `chibicc-eval/EVAL.md`).

## 1. Shared runner — `mesh-rom-gate` (new, `scripts/`, deployed via sync-tools)

One tool marshals `<rom-name> args…` → runs the ROM under the node-built `uxncli` →
prints the verdict TEXT, maps to rc **0 (OK) / 1 (RED) / 2 (n/a — engine or ROM absent,
stated LOUDLY on stderr)**. Extracts the `rom_verdict` logic already inside
`mesh-lease-audit` so there is exactly one copy (a-format-fix-must-sweep-every-reader).

- ROMs resolve from the genome checkout (`scripts/uxn/*.rom`); `uxncli` from
  `build.sh`'s per-node output (`scripts/uxn/bin/uxncli`).
- rc=2 is honest-n/a per the mesh-land convention: absence of the organ is a claim about
  the node, never a fake verdict (na-must-be-a-claim-about-the-node).
- A nonzero uxncli pipeline fails LOUD (the halt-convention trap, EVAL.md: sourced
  `set -uo pipefail` once killed the audit silently).

## 2. Fail-mode rule (load-bearing decision)

A consumer routed through a ROM keeps its existing inline compare as the **explicit rc=2
fallback**: on n/a it computes inline AND stamps the verdict source (`src=rom` /
`src=inline-fallback`) into its state line. Never a silent pass; never a blocked reflex on
a node without the engine. Both edges of this rule are part of each red-first proof
(fallback must be rare and LOUD — the detect_beat_ms canon, f51e36d).

## 3. Consumers wired this round (all run on mesh-home)

1. **`mesh-lease-audit` → cron.** Header exists (`# reflex-cadence:`), never wired — the
   never-wired-reflex rule (cc617e5). Wire via `mesh-autowire`; its `--test` must fit
   autowire's `timeout 30` (test-render-exceeds-autoland-timeout) — slim the wired test if
   needed, keep the heavy red-first suite as `test-lease-audit` (manual/doctor). Verify the
   crontab line EXISTS afterward, and that `--test` writes no live log (mesh-doctor runs
   tests hourly — the guardian-log forgery canon 09f7914).
2. **`mesh-therm-watch` → `band-gate.rom`** for the NVMe temp window (`nvme-c 20 70`,
   `band-fixtures`), via mesh-rom-gate + §2 fallback.
3. **`mesh-body-power` → `band-gate.rom`** for the charge longevity window
   (`battery 20 80`).
4. **New C gate class — `hyst-gate.c`** (chibicc): onset/recovery hysteresis carrying
   prior state — `value on_thresh off_thresh prev` → `ALERT/CLEAR/HOLD` — the
   both-edges-of-a-signal-need-the-same-gate regression family. Wired into
   mesh-therm-watch's alert/recovery path so onset and recovery provably share ONE gate.
   Red-first: corrupt each comparison in turn; assert ALERT requires crossing on_thresh
   and CLEAR requires dropping below off_thresh (not on_thresh); prev=ALERT holds between
   the thresholds.

## 4. chibicc vendored

`scripts/uxn/chibicc/` at the verified commit of lynn/chibicc (pinned source; provenance
header in build.sh like the uxnasm/uxncli vendor). `build.sh --chibicc` builds it (host cc
only). New `cc-rom.sh` helper: `gcc -P -E` → `chibicc -O1` → `uxnasm`.
**Gate:** rebuild `lease-gate-c.rom` from the vendored source and assert the 5-row truth
table matches (byte-identity is a bonus, not the gate — chibicc output may legitimately
drift a byte across hosts; the CONTRACT is the truth table).

## 5. Doctrine line

`scripts/uxn/README.md` + CLAUDE.md verification section: *a new pure predicate defaults
to a ROM gate via mesh-rom-gate; self-grep gates remain banned; plumbing stays shell.*

## Testing (every item red-first)

- Bad value → RED seen live (not a constant: corrupt-the-opcode proof pattern from the
  pilot suites).
- Engine removed (`uxncli` renamed away) → rc=2 LOUD + inline fallback engages + state
  line says `src=inline-fallback`.
- `--test`s never write live state/logs; exit 2 where the organ is honestly absent.
- After autowire: the crontab line exists (invoked-by-is-not-ever-runs).

## Out of scope

Persistent/varvara organs · fleet-wide ROM deploy beyond genome-checkout nodes ·
rewriting plumbing in C · uxn for anything that is not a pure predicate.

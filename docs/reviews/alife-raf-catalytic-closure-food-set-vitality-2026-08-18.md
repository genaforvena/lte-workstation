# LITERATURE review — RAF theory: catalytic closure against a DECLARED food set (2026-08-18)

**Area:** artificial life / origin-of-life & open-ended evolution, entered from the angle of an
**operational mechanism** — an algorithm that decides whether a network sustains itself, not a
philosophy of what self-sustaining means.
**Reviewer:** genome mind · live WebSearch 2026-08-18 + read of the primary arXiv abstracts.
**Verdict:** LAND — one un-embodied mechanism, one shipped (uncommitted) read-only axis in
`scripts/mesh-vitality`, gated red-then-green on three mutants.

---

## The mechanism, and where it is being published now

> **RAF theory — Reflexively Autocatalytic and Food-generated sets.** Hordijk & Steel, *"A concise and
> formal definition of RAF sets and the RAF algorithm"*, **arXiv:2303.01809** — the polynomial-time
> closure algorithm and the maxRAF / subRAF / **irreducible RAF** hierarchy.
> Still live literature: Palmerini, Sartori, Serra et al., *"Bridging two theoretical frameworks of
> autocatalysis: RAF sets and stoichiometric autocatalysis"*, **arXiv:2605.25523 (May 2026)** — proves
> that under mild and general conditions **any RAF is stoichiometrically autocatalytic**, by putting
> both frameworks in a common stoichiometric-matrix representation.
> (Found via the ALIFE-2026 open-endedness thread → arXiv; abstracts read directly.)

A set `R` of reactions over molecules is a **RAF relative to a food set `F`** iff

1. **reflexively autocatalytic** — every reaction in `R` is catalysed by a molecule produced by `R`
   or already present in `F`; and
2. **F-generated** — every reactant of every reaction in `R` is producible from `F` by `R`.

The **RAF algorithm** is a fixed point: repeatedly delete any reaction whose catalyst is not
available, until nothing more deletes. What survives is the **maxRAF**; it is empty exactly when the
network has no self-sustaining core. A RAF with no proper RAF subset is **irreducible** — the shape
where the whole core hangs on single catalysts.

**The move that makes it operational is the food set.** Closure is *undefined* until you say what the
system may take for granted. That is the part we had never written down.

### The live controversy, honoured

The 2026 bridge paper's contribution is also its warning: RAF is **catalytic** closure ("every
reaction has a catalyst the set makes"), while stoichiometric autocatalysis is **net-productive**
closure ("the flux actually reproduces the set"). They coincide only under stated conditions. A CLOSED
RAF verdict is therefore **not** a claim that the loop out-produces its own decay — and the axis below
says so in its own output rather than in a footnote.

## Why it is genuinely un-embodied

`mesh-vitality` already carries three neighbours, and RAF is none of them:

| existing sign | what it asks | what it never asks |
|---|---|---|
| `loop_closure_frac` | does any tool read this sense's state **and** actuate? | is the actuator itself produced? |
| `allopoiesis_gap` | how many hours has the production→landing loop stood **open**? | one loop's latency, not the network |
| `rhizome_index` | how **centralized** is the call graph? | shape, not self-maintenance |

None of them declares a food set. Without one, *"the mesh maintains itself"* has never been a
checkable sentence: every autopoiesis sign here silently counts the operator's hands, cron, git and a
hand-installed systemd unit as free.

## What was built — `raf_closure()` in `scripts/mesh-vitality`

The RAF algorithm over the mesh's five **maintenance reactions**:

| reaction | product | live catalyst(s) here |
|---|---|---|
| `deploy` | genome source → `~/.local/bin/mesh-*` | `mesh-land --autoland` |
| `schedule` | `# reflex-cadence:` header → a live cron line | `mesh-autowire`, `mesh-reflexes` (indirect) |
| `push` | settled fix → origin | `mesh-land`, `mesh-genome-sync` |
| `pull` | origin → local genome | `mesh-genome-sync`, `mesh-land` |
| `session` | the tmux channel set | `mesh-restore` (via the `mesh-liveness-loop` unit) |

**Food set, declared:** `bash git tmux ssh`. The operator's hands are deliberately **not** food — that
is the whole point.

A catalyst counts only if it is **deployed** AND **carried** (a cron line · an active systemd unit ·
one hop from a carried tool) AND **invoked with the arguments that enable its production step**. The
fixed point then cascades as the theory requires: a cron-carried mesh catalyst is available only while
`deploy` (which makes its binary) and `schedule` (which makes its cron line) themselves survive — so
losing the deployer empties the whole core, not one row.

### Measured on mesh-home, 2026-08-18

```
CLOSED core=5/5 food=ok single=[deploy,session]
       indirect=[schedule:mesh-reflexes(via:mesh-autowire),
                 session:mesh-restore(via:mesh-liveness-loop)]
```

Catalytically closed — **and thin**. Two facts the panel had no way to state before:

- **`deploy` has exactly one live catalyst**: `mesh-land`. `mesh-sync-tools` runs `*/20` on this node
  **report-only by design** ("the healing stays a decision someone makes", its own header) — it detects
  deploy-drift and catalyses nothing; only `--apply` would, and no schedule passes that flag. So the
  binary→disk step rides entirely on the landing path.
- **`session` has exactly one**: `mesh-restore`, and it is not scheduled at all — it is carried
  indirectly by `mesh-liveness-loop.service`, a unit file **no reaction here produces**. (Note this
  also contradicts `CLAUDE.local.md`'s "`@reboot mesh-restore`" driver line: the live crontab has
  **zero** `@reboot` entries. The loop unit is what actually holds the session up.)

That is Hordijk & Steel's **irreducible RAF**, and it is the honest shape of our autopoiesis claim.

### Stated boundary (kept in the output, not the footnotes)

- **Catalytic only.** `mesh-land`'s deploy fires only on runs that have something to land — catalysis
  without guaranteed production, exactly the gap that cost 55 unlanded commits for 11h
  (`the push that only happens when something else does`, 1969a5d). The 2026 bridge paper's
  RAF-vs-stoichiometric distinction is the reason this is reported as `CLOSED`, never as "productive".
- **`indirect=` is a weaker claim** than a schedule — a call site is not proof it ever runs
  (`invoked-by-is-not-ever-runs`) — and is never merged into the strong count.
- **`stale-table=`** fires if a named catalyst no longer contains its reaction's code signature, so
  the hand-declared table cannot rot silently into a false CLOSED.
- Report-only: it never touches the `[vitality-low]` edge or the exit code.

## The gate, seen red

`raf_closure --selftest` is the **same tool, same schedule, one flag apart**: a bare report-only
`mesh-sync-tools` cron must catalyse nothing (core cascades to `EMPTY`), and `--apply` must make
`deploy` live. Plus a live-read well-formedness leg and an env-driven no-deployer leg
(`EMPTY core=0/5`) — a fixture-only gate cannot cover the real crontab/systemd path.

Three mutants, each seen **red** before restoring:

| mutant | result |
|---|---|
| drop the `--apply` arg-gate | `gate=FAIL(report-only cron catalysed deploy: core=3)` |
| remove the SELF exclusion | `gate=FAIL(self-catalysis: deploy via mesh-vitality)` |
| break the deploy cascade | no-deployer fixture reads `OPEN core=4/5` instead of `EMPTY core=0/5` |

**Self-reference trap, found live while building it** (the same one `loop_closure_frac` hit in prose
form, here in *code*): this file's reaction **table** names `mesh-sync-tools --apply` in a Python
literal — not a comment — and `mesh-vitality` is itself cron-carried, so the scan made the measurement
its own catalyst, inventing a second deployer and hiding `deploy` from `single=[]`. Fixed by excluding
SELF and by refusing `(` as a command-position prefix (a tuple is not an invocation). The gate for it
was **vacuous at first** — the fixture didn't include `mesh-vitality`, so the check could never fail;
the fixture now carries this tool's own cron line on purpose.

## Files

- `scripts/mesh-vitality` — `raf_closure()` + literature block + report/log wiring + three `--test` legs.
- this doc.

Uncommitted in the tree; steward lands.

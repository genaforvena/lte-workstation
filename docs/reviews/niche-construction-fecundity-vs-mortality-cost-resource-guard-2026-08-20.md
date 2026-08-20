# The cost you apply to a producer has a KIND, and we only ever applied the bad one

**Live review, 2026-08-20 — niche construction & the extended phenotype, from the angle the task
asked for: an OPERATIONAL mechanism, not a philosophy.**
Landed in `scripts/mesh-resource-guard` (uncommitted; steward lands from the tree).

## Where we already are, so this could not re-land

`memory/niche-construction-review-coverage.md` is the ledger for this area. Landed axes: external
immunity / removal control · the negative inter-scale terminator niche (Coninx 2023) · realized
heritability inflation (Fogarty & Wade 2022, HELD) · collective social NC (Sueur et al. 2026) ·
driftability / the variance channel (Fábregas-Tejeda & Ramsey 2024) · NC3 mechanism attribution
(Trappes 2022, Krüger 2026) · the by-product null and the fitness sign (Poulin 2010) · the ghost —
durability × recipients (Jones/Lawton/Shachak 1994, landed 2026-08-19 in `mesh-reflex-health`).

Every one of those lands on `mesh-forage`, `mesh-vitality`, `mesh-ideate`, `mesh-promises` or
`mesh-reflex-health`, and every one is about **detecting** construction. This one is about what
happens when you **load** a producer, and it lands on a file this literature has never touched.

## The source

**Longcamp, A. & Draghi, J., "Evolutionary rescue of niche constructors from habitat exploitation:
Fecundity costs can promote rescue", *Evolution* 79(12):2667–2681 (2025),
doi:[10.1093/evolut/qpaf090](https://doi.org/10.1093/evolut/qpaf090)**
(Oxford Academic, https://academic.oup.com/evolut/article/79/12/2667/8134642). Found by working
forward from its own predecessor, Longcamp & Draghi, *Theor. Popul. Biol.* 153:37–49 (2023),
"Evolutionary rescue via niche construction: Infrequent construction can prevent post-invasion
extinction" — which is the same group's earlier result that the construction RATE, not the
construction, is the dangerous quantity.

The model: a resident population constructs its own reproductive habitat (converting habitat type 2
→ type 1) at a fitness cost; a non-constructing invader exploits the constructed habitat and pays
nothing — "its fundamental advantage is that it evades niche construction's fitness cost."

The result, and it is the operational part:

> "fecundity costs are not only less harmful than mortality costs but can even promote rescue
> compared with no costs by **reducing the rate at which constructors attempt reproduction and thus
> construction**."

So loading a producer is **not one axis with a magnitude**. The KIND of cost flips the sign of the
outcome:

- a **mortality cost** decides *who dies*. It changes nothing about the rate that drove the system
  into the wall.
- a **fecundity cost** acts *through the production rate itself* — the process lives and does less —
  and that rate is the quantity feeding the thing that kills you.

## Where it bites us — `scripts/mesh-resource-guard`

`mitigate()` was four lines and applied exactly two costs, never naming which was which:

```bash
renice -n 19 -p "$pid"                      # a FECUNDITY cost — lives, does less per second
echo 800 > "/proc/$pid/oom_score_adj"       # a MORTALITY cost — a standing kernel kill order
```

Their coverage of the two RUNAWAY axes is lopsided, and the lopsided direction was invisible
because both were logged as one word, `mitigated`:

| axis that fired | fecundity cost actually applied | mortality cost |
|---|---|---|
| **CPU** (>nproc×90%) | `renice +19` — real, it is a scheduling share | `oom_score_adj=800` |
| **RSS** (>3GB, >50% RAM) | **none** — renice does not slow allocation by one page | `oom_score_adj=800` |

**A memory runaway receives a pure mortality cost and zero fecundity cost.** It is marked for death
and then allowed to allocate at full rate all the way to the OOM. That is precisely the combination
this paper identifies as strictly worst, and it is the mesh's only response on the axis where the
2026-07-05 20:05–20:12Z OOM storm actually happened.

Two things wrong beyond the missing cost:

1. **The header's claim was false.** It read *"never hard-kills — operator decides"*. `oom_score_adj
   = 800` is a kill order handed to the kernel, executed without the operator ever seeing it. The
   guard issues no SIGKILL of its own; it does not follow that nothing dies. (Doctrine family: *a
   proxy that is not the claim*.)
2. **The missing fecundity channel exists on this node and is unused.** cgroup-v2 `memory.high`
   throttles allocation via reclaim pressure *without killing* — the textbook fecundity cost for
   memory — and under a systemd user manager the per-pane scope is delegated to uid 1000. Measured
   live: each mind pane is its own `tmux-spawn-*.scope`, `memory.high` is `-rw-r--r-- mesh-home`,
   currently `max`, and a write is **accepted**.

## The change (report-only — it sets nothing)

`cost_kind()` (pure) · `memhigh_state()` (probe) · `cost_clause()` in
`scripts/mesh-resource-guard`, wired into `mitigate()`'s durable log line and the `[resource-guard]`
board post. Verdicts **MORTALITY-ONLY** / **MIXED** / **FECUNDITY+MARK** / `na`.

Live render against a real mind pid (46812), one per firing pattern:

```
RSS only : fec=NONE(renice is scheduling-only; allocation rate untouched)
           mor=oom_score_adj=800(standing kernel kill order)   verdict=MORTALITY-ONLY
CPU only : fec=renice+19(scheduling share)                     verdict=FECUNDITY+MARK
both     : fec=renice+19(CPU axis only — no page of RSS slowed) verdict=MIXED
rss-fecundity-channel(cgroup memory.high, per-pane scope)=available(now=max)
```

That last line is the finding in one string: **the fecundity cost this paper says is the protective
one is available, unprivileged, on every mind pane, and we have never written to it.** Whether to
start is the operator's call, not a reflex's — so this publishes the choice instead of taking it.

Decisions that are decisions, not defaults:

- **The verdict, not the presence of a cost line, is what the gates assert.** A gate that only
  checked "a cost clause was printed" is blind to the entire finding.
- **`MIXED` still scopes the fecundity cost to CPU.** Printing a bare `renice+19` when both axes
  fire would read as though the memory axis were covered. It is not.
- **The probe ATTEMPTS the write; it never reads the mode bit** — CLAUDE.md's *"the mode bit that is
  not the write"*, whose worked example is a pseudo-file on this very node. It writes the file's
  **own current value** back, so the probe cannot change what it measures.
- **`absent` ≠ `na` ≠ `refused`.** No `memory.high` in the cgroup, not cgroup-v2 at all, and the
  kernel refusing the write are three different claims about the node.
- **Granularity is published, not assumed.** `memory.high` lives on the **cgroup**, so the channel is
  per-pane, not per-pid — a throttle would take everything sharing that pane with it. The clause
  says so.

## Gates

15 new assertions, 8 mutants seen RED with the control arm GREEN:

`rss-gets-renice` (RSS treated like CPU — the defect itself) · `mixed-unscoped` · `modebit-probe`
(the probe gates on `[ -w ]`) · `absent-as-na` · `v1-as-absent` · `unwired-log` (the clause never
reaches the durable log) · `no-mortality-name` · `probe-mutates-file` (the no-op probe writes `0`).

**One of those went GREEN first and that is the reusable part.** The `refused` fixture was a regular
file `chmod 0444` — where the mode bit is *honest*, so `[ -w ]` is false and the mode-bit mutant
passed it. A fixture for this doctrine has to BE a mode-lying file. `/proc/pressure/cpu` on this node
is mode `0666`, `[ -w ]` reads **TRUE**, and every unprivileged write is refused `EINVAL` — measured
in the same run. The suite now symlinks the fixture's `memory.high` at it, and the mutant goes red.
The leg is node-dependent and says so out loud when it cannot run, rather than passing silently.

A second thing the live run taught: `err="$(cmd > "$f" 2>&1)"` does **not** capture a failing
redirection. Redirections apply left to right, so `> "$f"` fails before `2>&1` is in force and the
diagnostic escapes to the caller's stderr — a bare `Permission denied` leaking out of `--test`. The
brace group `"$( { cmd > "$f"; } 2>&1 )"` puts stderr in place first.

Also fixed while here: `mitigate()`'s test could not be written without a real pid, and the obvious
`$$` would have reniced and oom-marked the test's own shell. It uses a throwaway child.

## Not done

The paper's actual dynamical claim — that **infrequent** construction is protective, and that
over-exploitation generates damped oscillations in the producer's population — is not measured here.
That needs the guard's RSS series held against the consumer's, which is a different instrument. And
`memory.high` is probed, never set: the fecundity cost remains available and unapplied, deliberately.

# LITERATURE (live review) — autopoiesis & the biology of cognition, entered from a known CRITIQUE

**Window:** genome, 2026-08-25 · **Landed in:** `scripts/mesh-closure --flux` (report-only, uncommitted in tree)
**Coverage map consulted first:** `[[autopoiesis-review-coverage]]` — closure-of-constraints, structural
coupling, normativity/adaptivity, allopoiesis, complexity-ratio, sympoiesis/holobiont, mortality
manifold, assembly theory, constraint-conservation-at-a-timescale, causal symmetrization and semantic
closure were all already embodied and none of them was re-landed.

## The critique

The critique is the one **Chemical Organization Theory was built to answer**: autopoiesis says a living
system *produces the components that produce it*, but the theory only ever formalized the **qualitative**
half of that claim. Closure — "no novel species are produced" — is a set-membership fact and is cheap to
check. Self-production is a **rate** fact and is not.

**Live source (2026):** Tomas Veloz & Christian Jendreiko, *"Chemical organizations as a conceptual tool:
from synthetic biology to interdisciplinary systems and back"*, **Frontiers in Bioengineering and
Biotechnology 14 (2026), doi:10.3389/fbioe.2026.1801128**, read 2026-08-25.

- verbatim on the formalization: *"COT formalizes the autopoiesis concept — that living systems are
  self-producing networks (Maturana and Varela, 1980) — into a formal framework"*
- verbatim on the gap: *"semi-self-maintenance (qualitative cycles exist) does not guarantee
  self-maintenance (quantitative sustainability)"*
- their counterexample: a cyclic pathway that consumes two units and produces one. Closed,
  semi-self-maintaining, visibly circular — and it drains to death, because *"no positive flux through
  both reactions can achieve"* balance.

**Definitions (source of the framework):** Peter Dittrich & Pietro Speroni di Fenizio, *"Chemical
Organisation Theory"*, **Bulletin of Mathematical Biology 69:1199–1231 (2007),
doi:10.1007/s11538-006-9130-8**. A **semi-organization** is closed + semi-self-maintaining (structural).
An **organization** is closed + self-maintaining, and self-maintenance requires a **strictly positive
flux vector v > 0 with Sv ≥ 0**: every reaction in the set must actually occur at a positive rate.

## What we did not embody

Every closure axis the mesh owns is a claim about **structure** or about a **schedule**, never about an
observed rate:

| axis | asks |
|---|---|
| base graph | does A's product reach B? |
| `--timescale` | is it conserved at B's clock? |
| `--enacted` | does the mention sit on a line that *could* run? |
| `--semantic` | who wrote the threshold? |
| `--symmetry` | do structure and activity move together in aggregate? |

Under the COT criterion the mesh's closure report has therefore always been a **semi-organization report
wearing an organization's name** — `mesh-closure`'s own first line says it asks whether the reflex set
forms "a self-maintaining CLOSURE", and nothing in it measured self-maintenance. `--enacted` names the
residual exactly and declines to close it: *"a live mention is still only a mention: it proves the token
appears on a line that COULD run, never that it ran … the residual would need runtime tracing, which no
reflex here carries."* **That residual is the flux vector**, and the runtime trace turns out to already
exist on this node.

## The oracle, and why the obvious cheaper ones are wrong

**Chosen: the cron EXECUTION journal** (`journalctl -t CRON`), not any artifact a tool writes.

Every one of the 285 wired cron lines here appends to its own `>>` log, so that mtime looks like a free
per-reflex flux reading. It is a tape of **errors**, not of runs. Measured 2026-08-25: only **247/285** of
those targets had been written in *seven days*, and among the dark ones is `mesh-egress-health`, whose own
board posts prove it ran three minutes earlier. A healthy quiet run writes nothing and moves no mtime, so
an artifact-mtime oracle reads the healthiest reflexes as the deadest ones — `[[a-tape-of-only-positives-is-a-numerator]]`
one ring out. The `# reflex-state:` per-run artifact is sound but declared by only **17** tools.

journald's CRON identifier records the **invocation itself**, output or not: **122272 CMD lines over 266
distinct `mesh-*` tools in 24h** on this node. That is the flux vector, observed.

## The up-time term (without it the axis is a lie on this node)

A daily reflex that did not fire because the machine was **powered off** has not "run at rate 0" — nothing
scheduled it. This node power-cycles hard, so the denominator is **up-time**, never wall time, and it is
derived from the journal itself rather than from a second source: sum the consecutive-entry deltas ≤ GAP
(default 300s) and drop the rest. Then `expected_fires(t) = up_minutes / period_minutes(t)` from
`mesh-closure`'s own `cadences`, and a reaction is only ever called DARK when its own schedule predicted
at least one fire inside the observed up-window.

**Independently validated against the boot record** (a source the axis never reads): journal-derived
up-time over the 24h window = **16.13h**; `last -xF reboot` gives 3.38 + 1.97 + 10.83 = **16.18h**. Agreement
within three minutes.

## Classification and verdict

Per enablement edge A→B, over the **enacted** subgraph (`--enacted`'s narrowed base, not the prose-inflated one):

- **FLUX** — both ends observed firing: the reaction occurs at a positive rate
- **ZERO-FLUX** — an end fired 0 times while its own cadence predicted ≥1 fire inside the observed up-time
- **UNCOVERED** — expected < 1 fire, no parseable cadence, or the tool only ever appears *chained* behind
  another in a cron command (it may have been gated out, so it can never be convicted). Honest n/a.

Verdict over the covered sub-network: **ORGANIZATION** (closed AND every covered reaction carries v > 0) ·
**SEMI-ORGANIZATION** (closed and cyclic, ≥1 covered reaction at rate 0 — the Veloz & Jendreiko
counterexample: circular on paper, draining in fact) · **UNDETERMINED**.

## Live reading (mesh-home, 2026-08-25, 24h window)

```
window=24h nominal · observed UP-time=16.13h from 40869 cron invocation(s)
base graph=ENACTED
edges: FLUX=242  ZERO-FLUX=0  UNCOVERED=51   coverage=242/293 assessable
LOOPS: FLUX=9  ZERO-FLUX=0  UNCOVERED=6
VERDICT: ORGANIZATION — closed AND every covered reaction carries positive flux (v > 0)
```

**ZERO-FLUX=0 is not a blind detector.** 21 of the 267 scheduled tools did not fire in 24h
(`mesh-job-scan`, `mesh-test-forgery`, `mesh-log-attest`, `mesh-reflex-decay`, …). **Every one of them is
daily (period 1440m) or weekly**, and 16.13h of up-time = 968 up-minutes gives expected = 0.67 < 1 — so the
up-time term correctly declines to convict them. That is the same fact `mesh-cron-catchup` was built for
(`[[a-daily-cron-slot-is-lost-not-deferred]]`), arriving here from the opposite direction: on this node the
whole daily class is *structurally unobservable* inside a one-day window, and the axis says so instead of
calling it dead.

## Gate (RED-first, driven both ways)

`mesh-closure --test` PASSes; five new legs, and the two load-bearing ones were driven red by mutation:

| mutant | leg that went red |
|---|---|
| kill the `expected < 1` power-cycle exemption | *"must NOT convict a reflex whose slot never came round"* + *"named mesh-fc as zero-rate on a window too short"* |
| kill the gap exclusion (count wall time as up-time) | *"2×30min clusters 20h apart should read ~1.0h up"* — read **20.50h** instead |

Other legs: all-firing fixture → ORGANIZATION; the same fixture minus one hourly reflex → SEMI-ORGANIZATION
naming it, its period, its expected count and the consumer it **starves**, with the loop leg flipping
`FLUX=1 ZERO-FLUX=1`; a readable-but-empty journal → UNDETERMINED, never a mass conviction; a fixture var
set-but-unreadable → error, never a quiet fall-back to the live journal. The live `journalctl`-absent branch
was exercised under `env -i PATH=<stub dir without journalctl>` → honest n/a, **rc 2**.

## Honesty bounds (in the tool header too)

- The journal records **invocation, not completion**. A reaction that fires and dies at line 1 counts as
  flux. That is the COT criterion (the reaction occurs), not a health claim — `mesh-reflex-health` owns the
  did-it-*succeed* question.
- Coverage is **published in the reading** (covered/total edges, observed up-hours vs the nominal window).
  A rotated journal shrinks up_minutes → shrinks expected_fires → turns DARK into UNCOVERED. The error
  direction is toward silence, never toward a false conviction.
- Only the **first** `mesh-*` token of a cron command is credited with firing (the convention `cadences`
  already uses); later tokens are marked CHAINED and are exempt from ZERO-FLUX rather than counted as fired.
- A tool launched by something other than this cron table (systemd timer, a mind's hand, `@reboot`) has no
  cadence here and reads UNCOVERED, never DARK.
- Report-only. It never prunes, never edits cron, never gates.

## Sources

- Veloz, T. & Jendreiko, C. (2026). *Chemical organizations as a conceptual tool: from synthetic biology to
  interdisciplinary systems and back.* Front. Bioeng. Biotechnol. 14. https://doi.org/10.3389/fbioe.2026.1801128
- Dittrich, P. & Speroni di Fenizio, P. (2007). *Chemical Organisation Theory.* Bull. Math. Biol. 69:1199–1231.
  https://doi.org/10.1007/s11538-006-9130-8
- Maturana, H. & Varela, F. (1980). *Autopoiesis and Cognition: The Realization of the Living.* Springer.
  https://doi.org/10.1007/978-94-009-8947-4

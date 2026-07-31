# VSM live review — a POWER-RELATIONS lens on the mesh: who holds the hidden power of agenda-setting?

**Date:** 2026-07-31 · **Area:** Viable System Model / management cybernetics (Stafford Beer) ·
**Angle:** a *recent* (2025) result · **Organ touched:** `scripts/mesh-vitality`
(`power_concentration()`, report-only)

## The live literature (real sources, read this session)

The standing critique of Beer's VSM — that it is a "unitary, functionalist" model, structurally
rigorous but blind to power, politics, and *whose voice* shapes what an organization does — got a
concrete cybernetic answer this year:

- **Sh. Zeini, "The Viable System Model Through a Power-Relations Lens: Towards a Power-Aware
  Conceptual Framework," *Systems Research and Behavioral Science* (2025), doi:10.1002/sres.70028**
  (<https://onlinelibrary.wiley.com/doi/10.1002/sres.70028>). It grafts **John Gaventa's power cube**
  (Gaventa, "Finding the Spaces for Change: A Power Analysis," *IDS Bulletin* 37(6), 2006) onto the
  VSM. Power operates in three **forms** — **visible** (observable decisions, formal rules),
  **hidden** (who sets the *agenda* — controls what even gets to be decided), **invisible** (norms
  that shape what is thinkable) — across **levels** and **spaces** (closed / invited / claimed).

Cross-checked against the authoritative pathology frame (José Pérez Ríos, *Models of organizational
cybernetics for diagnosis and design*, Kybernetes 39(9/10); and his 2025 re-application, "The VSM and
the Taxonomy of Organizational Pathologies in the Age of AI," *Systems* 13(9):749) and Espinosa's
emancipatory-VSM revisit (*SRBS* 42, 2025, doi:10.1002/sres.3090). The Pérez Ríos and Espinosa lines
are **already embodied** in the genome (`homeostat34` cites the *Systems* 13(9):749 AI paper for the
S3-S4 "headless-chicken" pathology; `residual_variety` cites Espinosa for S1↔S3 variety balance). The
**power-relations lens is not** — 0 prior grep hits for power/Gaventa/agenda anywhere in `scripts/`.

## The concept we do NOT embody

**Gaventa's HIDDEN power — the concentration of agenda-setting voice.** Every VSM/variety sign in
`mesh-vitality` reads *structure*: `autonomy_ratio` (who committed code), `residual_variety` (where
variety is absorbed vs escalated), `homeostat34` (present-vs-future balance), `channel_variety`
(inflow-vs-closure rate). **None** reads the *relational* question the power cube makes central: among
the many voices on the board, **whose agenda is the mesh actually running?**

This blind spot has already bitten in the wild and is named one function down: `omega_cycle`'s own
header records *"roll-call re-raising the identical GAP set every round"* — a single automated channel
monopolising the agenda by repetition. That is a textbook Gaventa hidden-power concentration, and no
marginal or structural sign in the file flags it.

## The application (landed, report-only)

`scripts/mesh-vitality` → **`power_concentration()`**. Over `POWER_WIN_H` (72h) of the board, count
`[task]` **originations** by author (`who@node`) — the `[task]` lines *are* the mesh's agenda, the set
of things it has decided are worth doing. Report the **top-originator share** = `max_author / total`,
the number of distinct **voices**, and **who** the top voice is:

- `top-share ≥ POWER_HI` (0.60) → **CONCENTRATED** — one voice owns the agenda (hidden-power monopoly).
  *Read WHO:* the operator legitimately holds S5 visible power, but a **reflex** monopolising the
  agenda is the pathology (the roll-call limit-cycle above).
- `top-share < POWER_LO` (0.35) → **DISTRIBUTED** — many voices shape what the mesh works on.
- else **MIXED**. Below `POWER_FLOOR` (6) → `INSUFFICIENT`.

Re-posts are **not** deduped: repetition *is* agenda control, exactly the roll-call pathology.
Report-only — a concentration statistic wants trend and a human read of *who* before it could gate;
it never touches the `[vitality-low]` edge or the exit code.

**Live reading (real board, this session):** `DISTRIBUTED(top=0.20, who=genome:12, voices=9, N=59)` —
59 agenda-setting posts over 72h spread across 9 voices, the top voice only 20%. A healthily
distributed agenda; no reflex monopoly right now.

### Distinct from every existing axis

- `autonomy_ratio` — git-commit **provenance** (who wrote code), not who set the agenda.
- `residual_variety` — `[verify]`/leaked-hold **escalation direction** (who couldn't absorb variety),
  not who **originated** the agenda item.
- `channel_variety` — `[task]`-inflow-vs-`[done]`-closure **rate**, blind to how inflow is *shared*
  across originators.
- `rhizome_idx` — call-graph centralization of **tools** (code topology), not board voices.

This is the mesh's **first power-relations reading**: a concentration of agenda-setting *voice*.

### Verification

RED-first `--test` (3 fixtures): a `rollcall`-dominated board → `CONCENTRATED(top=0.90,who=rollcall)`;
8 distinct voices → `DISTRIBUTED(top=0.12,voices=8)`; a board of 40 `[taking]`/`[done]` markers →
`INSUFFICIENT(N=0)` (only `[task]` originations count). Mutants proven: collapsing the classifier to a
constant `MIXED` → the CONCENTRATED/DISTRIBUTED fixtures go RED; counting all markers instead of
`[task]` → the execution-guard fixture goes RED. Both restored → GREEN. Full `mesh-vitality --test`
passes.

### Held (not shipped)

Gaventa's **claimed-vs-invited space** — a `[task]` a window self-raises (claimed) vs one dispatched
*to* it (invited) — would split self-determined from imposed agenda, but needs an owner/author
reconciliation that risks the two-matcher rot the one-matcher rule warns against. Deferred.

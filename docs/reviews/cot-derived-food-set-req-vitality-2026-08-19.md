# Chemical Organization Theory's `req(X)`: derive the food set, don't declare it — `mesh-vitality`

**Area:** autopoiesis & the biology of cognition (Maturana/Varela lineage → self-fabrication formalisms)
**Angle:** a concrete METRIC the area uses to measure itself
**Date:** 2026-08-19 · **Window:** genome · **Status:** implemented, uncommitted in tree

---

## 1. Where the live literature is

**Chemical Organization Theory (COT)** — and it is genuinely live, not a 2007 artefact:

- **Tomas Veloz & Alejandro Bassi, "Synergy and Complementarity: The Generative Basis of Chemical
  Organizations", arXiv:2608.03541v1 [q-bio.MN], submitted 4 August 2026** — read at
  <https://arxiv.org/html/2608.03541>. Two weeks old at the time of this review. Gives the formal
  definitions used below and an ERC-based generative account; reports sublinear compression
  (exponent ≈ 0.71) over 438 biological networks.
- **Veloz & Jendreiko, "Chemical organizations as a conceptual tool: from synthetic biology to
  interdisciplinary systems and back", *Frontiers in Bioengineering and Biotechnology*, 2026**,
  doi:10.3389/fbioe.2026.1801128.
- **Heylighen, Beigi & Veloz, "Chemical Organization Theory as a General Modeling Framework for
  Self-Sustaining Systems", *Systems* 12(4):111 (2024)** — MDPI (paywalled to this node, 403).
- Foundational: **Dittrich & Speroni di Fenizio, "Chemical Organisation Theory", *Bulletin of
  Mathematical Biology* (2007)**, doi:10.1007/s11538-006-9130-8.

**Prior-art check (this is the most-mined lane in the genome — 40+ reviews).** `Dittrich`,
`chemical organization theory`, `lattice of organi`, `Speroni` — **zero hits** across `scripts/` and
`docs/`. The single trace is one survey word, "COT", inside
`autopoiesis-measurement-control-complementarity-link-heal-2026-08-18.md:16`. A mention is not an
embodiment.

Also checked and **rejected as already-landed**: Beer's cognitive domain (`mesh-chaos:55-94`, with its
own HELD extension), RAF (`mesh-vitality raf_closure`, 2026-08-18), operational/organizational closure,
semantic closure, NTIC, constraint closure, eigenform, precariousness, viability space. The ALIFE 2026
tutorial page was re-fetched before noticing the 08-18 review had already recorded that it offers no
quantitative measure — that note was right, and re-reading it first would have saved the fetch.

## 2. The mechanism

COT's definitions, verbatim from arXiv:2608.03541:

- **Closure:** "The closure clos(X) of a set of species X is the smallest closed set containing X."
- **Requirement set / semi-self-maintenance (Definition 2):** X is semi-self-maintaining iff
  **`req(X) = supp(ℛ_X) − prod(ℛ_X)`** is empty — "every consumed species in ℛ_X can be produced by ℛ_X".
- **Organization:** "A set of species X ⊆ ℳ that is closed and (semi-)self-maintaining."

The operational content, stripped of chemistry: **COT never asks you to name what the system may take
for granted. It computes it.** That is the exact complement of RAF, whose whole operational move is the
*declared* food set F — as our own RAF block says: *"closure is undefined until you say what the system
is allowed to take for granted."*

## 3. Where it bites: `scripts/mesh-vitality`, `raf_closure()`

`raf_closure` runs the RAF fixed point over five maintenance reactions (deploy · schedule · push ·
pull · session) against `FOOD = ['bash', 'git', 'tmux', 'ssh']` — **four hand-typed literals**. Its
`food=` field checked only whether those four are on `PATH`:

```python
missing = [f for f in FOOD if not any(os.access(os.path.join(d, f), os.X_OK) ...)]
out += ' food=ok' if not missing_food else ' food=MISSING:[...]'
```

So `food=ok` has always meant *"the four names I typed are installed"*. **It has never asked whether the
declaration is complete** — and an unchecked enumerated list is precisely the shape this genome has
already paid for (`reflex-health`'s value-frozen registry, 203ce10; doctrine:
*"an enumerated alphabet is a copy that rots"*).

**Artifact — the derived set, measured on this node 2026-08-19:**

```
before:  CLOSED core=5/5 food=ok single=[deploy,session] indirect=[...]
after:   CLOSED core=5/5 food=ok food-UNDERDECLARED:[chmod,cp,cron,crontab,grep,mv,systemd]
                                 single=[deploy,session] indirect=[...]
```

Seven species consumed by a **live** catalyst that no reaction here produces and F never named, against
four declared. Two of them are load-bearing rather than cosmetic: **`cron` and `systemd`**. This file's
own availability predicate is *"a catalyst counts only if it is DEPLOYED and CARRIED (a cron line, an
active systemd unit...)"* — so `CLOSED core=5/5` has always been closure **conditional on an exogenous
scheduler the food set does not mention**. `systemd` is reachable only through the `via:` hop
(`session` is held by `mesh-liveness-loop`, a unit); the `via:` label hides the carrier kind, and
recovering it is what makes `systemd` visible at all.

The verdict is unchanged and report-only — this never gates or alters the exit code. It makes the
existing CLOSED claim *auditable*, which it was not.

## 4. Gates

Six assertions in `raf_closure --selftest`, **8/8 mutants RED against a green control**:

| Mutant | Gate that catches it |
|---|---|
| req hardcoded, not derived | **the null**: an empty surviving set must derive an empty `req` |
| carrier not counted as consumed | a cron-carried catalyst must register `cron` |
| `mesh-*` products leak in | `prod(ℛ_X)`: the deploy reaction makes them |
| tool-internal names leak in | `prod(ℛ_X)`: a name the tool defines is produced inside it |
| `underdeclared` accuses unconditionally | a food set covering every derived species must silence it |
| `underdeclared` always empty | an empty food set must leave the whole set underdeclared |
| quote-parity guard removed | prose in a quoted message must not mint a species |
| assignment read as invocation | `foo=bar` is not a call |

The null (row 1) is deliberate: the repo's standing rule after
`enactivism-4e-nave-unfalsifiable-closure-null` is that a closure statistic ships with a null that *can*
fail.

**Three of these gates were vacuous when first written** and are the honest lesson here. The `mesh-*`,
tool-internal and quoted-prose filters all survived deletion with the suite green, because they were
asserted only *through the live corpus* and the fixture's own code never presented that shape. Factoring
the token filter into `species_of(line, tool)` and driving it on synthetic lines is what made them fail.
A fourth was vacuous for a different reason: the internal-name probe used `sorted(...)[0]`, an
upper-case local the command regex never matches, so the gate could not fail whatever the filter did —
**a probe outside the thing's domain tests nothing**.

## 5. What was NOT taken

COT's **lattice of organizations** (join `X ∨ Y = clos(X ∪ Y)`, meet `clos(X ∩ Y)`) is the bigger prize
— it would answer a question the mesh cannot currently ask: *when organs die, which sub-mesh is still
an organization?* Enumerating closed sets is exponential; the 2026 paper's contribution is the ERC
(Elementary Reaction Closure) route that avoids it, plus **synergy** (`ℛ_{X∨Y} ⊋ ℛ_X ∪ ℛ_Y`) and
**complementarity** (`req(X ∨ Y) ⊊ req(X) ∪ req(Y)`) as the generative relations. Not taken here: it is
a build, not an edit, and `req(X)` is the part that audits an existing landed claim today.

# Guattari's coefficient of transversality — the mesh cured horizontality with verticality, and its one topology metric calls that "rhizomatic"

**Area:** Deleuze & Guattari — assemblage, rhizome, the machinic. **Angle:** cross-domain transfer to a
distributed sensor mesh. **Date:** 2026-08-15. **Window:** genome (mesh-home). **Status:** landed,
uncommitted in the tree.

---

## 1. The concept, and where I found it

**Transversality** (Félix Guattari, *La transversalité*, 1964 — in *Psychanalyse et transversalité*,
Maspero 1972; English in *Psychoanalysis and Transversality*, Semiotext(e) 2015).

Guattari's own parable, written out of the Clinique de La Borde:

> "Imagine a fenced field in which there are horses wearing adjustable blinkers, and let's say that the
> 'coefficient of transversality' will be precisely the adjustment of the blinkers."

Adjust them to full blindness and the horses collide traumatically; open them and the herd moves
harmoniously. The coefficient is *"the degree of openness of these avenues"* — equivalently *"the degree
of blindness … of closure"*.

The load-bearing claim, and the whole reason the concept exists:

> **Transversality opposes BOTH verticality AND horizontality.**

Verticality = hierarchy, routing-through-a-superior. Horizontality = groups each sealed in its own
compartment. Transversality is neither: it is the diagonal that *"cuts diagonally through previously
separated parallel lines, as in the common garden gate"*.

### Sources actually read (not a reading list)

| what | where | how verified |
|---|---|---|
| Jean-Sébastien Laberge, **"Transversality, or How Not to Reproduce the Organisations You Fight"**, *Deleuze and Guattari Studies* **18(1):98–119**, Feb 2024, **doi:10.3366/dlgs.2024.0544** | euppublishing.com (403 to the fetcher) | metadata + full abstract pulled first-hand from the **Crossref REST API** (`api.crossref.org/works/10.3366/dlgs.2024.0544`) |
| **18th Deleuze and Guattari Studies Conference — theme "Transversality: Ethics and Politics"**, Panteion University of Social and Political Sciences, Athens, **10–12 July 2026** | dgs2026.org | page fetched 2026-08-15 |
| Helen Palmer & Stanimir Panayotov, **"Transversality"**, *New Materialism Almanac* | newmaterialism.eu/almanac/t/transversality.html | page fetched — source of "degree of openness of these avenues" and the garden-gate line |
| Guattari's blinkered-horses parable + Genosko's gloss ("Blinkers prevent transversal relations … The adjustment of them releases the existing, but blinkered, quantity of transversality") | traced from the 1964 essay via secondary quotation | quoted text located, primary text **not** held on this node — flagged as second-hand |
| Lucas Pavani Goulart, **"Guattari e a problemática da análise"**, *Psicologia & Sociedade* **38** (2026), **doi:10.1590/1807-0310/2026v38292117** | Crossref | evidence the institutional-analysis lane is publishing *now* |

**Why this counts as LIVE literature and not a fixed list:** the field's own flagship conference has taken
transversality as its *entire theme* for July 2026. This is the seam D&G scholarship is working this year.

**Not already embodied.** Checked both coverage maps (`deleuze-guattari-coverage`,
`deleuze-guattari-review-coverage`) and `grep -ri transversal scripts/` — zero hits in any organ. The
ten prior D&G landings cover exteriority, deterritorialization, disjunctive synthesis, machinic phylum,
order-word, smooth/striated, refrain, asignifying rupture, double articulation, rhizome-vs-arborescent,
and Buchanan's purpose-oriented reading. None is this.

---

## 2. The misread it corrects, in our own genome

`mesh-vitality`'s **`rhizome_index`** (landed 2026-07-31) scores the genome's topology by Freeman
in-degree **centralization**: →1 arborescent (fragile, god-tool SPOF), →0 *"flat/rhizomatic"* (healthy).

Live right now:

```
rhizome_index → 0.250/recip0.21/root=mesh-chat:158(N=612,E=3447)
```

C = 0.25 — read as rhizomatic, i.e. healthy.

**That metric treats horizontality as the cure for verticality.** Which is exactly the error Guattari's
concept exists to name, and exactly Laberge's title — *how not to reproduce the organisations you fight*.
Two boards score identically "rhizomatic" under it:

- one where every window closes **only its own** promises (pure courtyard — horizontality, C≈0);
- one where every promise is **routed by dispatch** to a named `owner:` and closed by that owner and
  nobody else (pure hierarchy laid flat — also C≈0).

Neither has a single diagonal avenue. Both pass.

Nor does anything on the **board** side see it. `--report`/`--balance` count whether a promise is kept.
`--mttr` times the repair. `--collisions` catches two takers on one slug. `--roles` measures each
window's *own* phase cycling. `--empowerment` asks whether a window *moves* the board. **Not one of them
asks who discharged whose** — the only question whose answer is an avenue between two groups.

And `rhizome_index` structurally cannot ask it: it reads **source text**, a static reference graph. An
avenue is something a window either travels or does not.

---

## 3. Application — `scripts/mesh-promises --transversality`

One edge per **kept promise**: `(poster → closer)`, with the post's `owner:` clause as the **prescribed**
avenue. Three classes, which are Guattari's three terms:

| class | condition | Guattari |
|---|---|---|
| `self` | closer == poster | the courtyard — **horizontality**, no avenue used |
| `routed` | closer == the prescribed window | **verticality** — the avenue the hierarchy laid |
| `diag` | closer ≠ poster **and** ≠ prescribed | **transversality** — an avenue nobody prescribed |

**T = diag / n.**

**Null:** permute the closer labels across episodes — each window's *close volume* preserved exactly, the
pairing destroyed. That is the correct null because the pairing is the quantity on trial (same posture as
`--roles`, whose null permutes a window's own role sequence). Two-sided permutation *p*, 2000 reps,
seeded `crc32` of the edge list.

**Blinker reading** (Guattari's literal metric): per closer window, how many **distinct other posters** it
has closed for *unprescribed*. Plus the high-volume windows with zero.

### No verdict of good

Guattari is explicit that the coefficient is **adjusted**, not maximised — there is no universal optimum,
only a setting for this group at this moment. So the bands name the **shape** (`SEALED` / `AS-MIXED` /
`CROSS-CUTTING`), never a fault. The mode weights nothing, gates nothing, exits 0.

### Honest n/a, with its reason

Below `MESH_TRANS_MIN_N` (12) kept promises, **or with fewer than two distinct closers**, it renders n/a
and computes no verdict. The second guard is load-bearing: with one closer every permutation is
*identical*, so a *p* there would be manufactured, not measured — a fabricated calm. Mutant M4 below shows
exactly that: strip the guard and a 12-promise single-closer board reports `AS-MIXED`.

### Deliberately promise-family only

A `[verify]` claim can only ever be redeemed by its addressed debtor — `redeem_claim()` looks up
`claims.get(who)`. A diagonal there is **forbidden by this file's own code**, so measuring it would
measure our constraint, not the board. Stated in the header so the next reader doesn't "fix" the omission.

---

## 4. The live reading

```
board transversality — the openness of the DIAGONAL avenues (Guattari 1964; report-only) · 00:34Z
  n=38 kept promise(s) · 9 distinct poster(s) / 7 distinct closer(s)
  T=0.342 diagonal (transversal) · 0.526 prescribed (vertical) · 0.132 self (horizontal/courtyard)
  null (closer-label permutation ×2000, close volumes preserved): T_exp=0.670 · ratio=0.51 · p=0.0010
  verdict: SEALED — the diagonal is travelled LESS than these same closers would by chance
  widest avenues: senses←4 distinct poster(s) · witness←3 distinct poster(s) · genome←2 distinct poster(s)
  blinkered (closes, zero diagonal): land:2 · sound:1 · discover:1 · tg:1
```

**What it says.** The board is **vertical, not horizontal**: 52.6% of kept promises travelled the avenue
dispatch prescribed, against only 13.2% closed in the poster's own courtyard. The diagonal is travelled
**half as often as these same closers' volumes would produce by chance** (0.342 vs 0.670, p=0.001).

Supporting count, straight off the board: **43 of 44** `[task]` lines in the window carry an explicit
`owner:` clause, and **40 of those 43 name a window other than the poster**. The routing is doing exactly
what it was built to do.

**This is not an indictment of dispatch.** Deterministic `owner:` routing is a mesh design decision with
its own justification (CLAUDE.md: "a bare tool name … hits ABSENT and falls through to generic pick,
breaking deterministic routing"). The finding is that the shape is now **visible and named** — and that
the mesh's only topology metric reports this same board as *rhizomatic* at C=0.25. Guattari's point is
that a flattened hierarchy is still a hierarchy; ours is flat and prescribed, and had no instrument
that could say so.

The blinker line names it per window: `senses` and `witness` are the two with genuinely open avenues
(4 and 3 distinct posters taken from unprescribed); `land`, `sound`, `discover`, `tg` closed only what was
theirs or was assigned to them.

**Caveat on n.** 38 kept promises over a 15-day board window (2026-07-31 → 2026-08-15) is thin. The
permutation *p* is exact for this sample, but a single census needs trend — same posture as every
structural lens in the genome. `~/.mesh/chat.log` is a rotating window, so this n will not reproduce.

---

## 5. Gates — every one seen RED

`mesh-promises --test`, legs 41a–41f, all against hand-built fixtures with known answers. Six mutants run
from a scratch copy, each going red **for its own reason**:

| mutant | leg that caught it | what it printed |
|---|---|---|
| M1 — `diag := closer != poster` (drop the prescribed check) | 41a | `T=0.667 … 0.000 prescribed` (should be 1/1/1) |
| M2 — fold `routed` into `self` | 41a | `0.000 prescribed · 0.667 self` — verticality vanishes |
| M3 — drop the null (`T_exp := T_obs`) | 41d | `AS-MIXED` on a pure-courtyard board — SEALED unreachable |
| M4 — remove the single-closer guard | 41c | `AS-MIXED` where the null is destroyed — the fabricated calm |
| M5 — unseed the permutation | 41f | two runs of the same board differ |
| M6 — verdict always SEALED | 41e | `CROSS-CUTTING` unreachable — a one-sided verdict |

41e is the one that matters most for honesty: an all-diagonal fixture must reach `CROSS-CUTTING`. A
verdict that can only ever say SEALED says nothing.

Full suite: `smoke-test: ok`, **5.77 s** (inside autowire's 30 s test budget). No existing mode changed —
`--report`, `--json`, `--roles`, `--check` re-run clean.

---

## 6. Distinct from

- **NOT `rhizome_index`** (`mesh-vitality`) — static source-reference centralization; the metric this corrects.
- **NOT `protocol_hold`** (`mesh-vitality`) — Galloway's bundled control per convention.
- **NOT `--collisions`** — two takers on one slug is a uniqueness violation, not an avenue.
- **NOT `--roles`** — a window's own role sequence, never a pair.
- **NOT `--empowerment`** — whether a window moves the board, not which window it moved it *for*.
- **NOT asignifying rupture** (`mesh-forage`) — whether a severed line reconnects, not who reconnected it.

## 7. Files

- `scripts/mesh-promises` — `--transversality` mode, doctrine header, `trans_edges` bookkeeping,
  `poster`/`prescribed` on the open record, test legs 41a–41f, usage + env docs.
- `docs/reviews/deleuze-guattari-transversality-coefficient-diagonal-avenues-promises-2026-08-15.md` — this file.

Env: `MESH_TRANS_MIN_N` (12) · `MESH_TRANS_REPS` (2000) · `MESH_TRANS_ALPHA` (0.05).

# Niche construction — COLLECTIVE SOCIAL niche construction: the constructed niche is the NETWORK

**Live review, genome, 2026-08-03.** Area: **niche construction & the extended phenotype**, angle the
task asked for — a **RECENT result (2023–2026), found by live web search**, landed somewhere the mesh
has not been. Landed as a new axis in `scripts/mesh-forage` (`social()`), report-only, rc-neutral.

## The recent result (cited, read)

**Sueur C., Solé R., Deneubourg J.-L. — "Collective social niche construction shaping adaptive social
networks." *Trends in Ecology & Evolution* **41**(7):607–617, July 2026.**
doi:[10.1016/j.tree.2026.04.001](https://doi.org/10.1016/j.tree.2026.04.001) · PMID
[42025566](https://pubmed.ncbi.nlm.nih.gov/42025566/) · epub 2026-04-22. Keywords listed by the
journal: *multilevel selection · optimality · self-organisation · social evolution · sociality*.

Abstract, verbatim (PubMed):

> "Understanding how social networks form and change is key to explaining the adaptability of human and
> nonhuman societies. **Collective social niche construction describes how individuals actively shape
> their social environment through interactions, generating network structures that influence
> cooperation, pathogen transmission, and information flow.** Recent advances reveal that network
> adaptability emerges through distinct mechanisms: self-organisation and phase transitions enable rapid
> topological changes in response to environmental pressures, while behavioural flexibility — central to
> the Cumulative Cultural Brain Hypothesis — supports enhanced social learning and cultural accumulation
> in high-intelligence species. Both pathways exemplify how **feedback loops between individual
> strategies and emergent network properties** generate adaptive, resilient social structures. This
> perspective positions **social networks as dynamic biological structures** shaped by plasticity at
> multiple hierarchical levels."

The move, in one line: classical niche construction is an organism modifying its *physical* environment
(a beaver dam, an earthworm's soil). Sueur et al.'s claim is that in social species **the constructed
niche is the interaction network itself** — the topology is built by the behaviour and then feeds back
on it, so the load-bearing structure lives in the *edges*, not in any per-individual quantity.

## Why it is NOT already embodied

The mesh has three prior niche-construction landings, all in `scripts/mesh-forage` — the removal control
(`2026-07-28`), the inter-scale terminator (`degrade()`, `2026-07-29`), the heritability-inflation
instrument axis (`2026-07-31`) — plus a whole swarm/stigmergy set. **Every one of them, and every other
board instrument in the mesh, reads the board as a bag of INDEPENDENT LANES.** Checked directly:

| instrument | what it reads | edge-aware? |
|---|---|---|
| `mesh-forage` `compute()` | Pielou evenness of the `[done]` **count per lane** | no — a marginal |
| `mesh-forage` `compute_assign()` | evenness of the `owner:` **count per lane** | no — a marginal (it drops the poster) |
| `mesh-forage` `no_entry`/`mill`/`degrade`/`drive` | counts, ratios, and rates **per lane** | no |
| `mesh-promises` | a per-lane liability **balance** | no |
| `mesh-vitality`, `mesh-dispatch` | per-tool / per-lane distributions | no |

`compute_assign()` is the near-miss that proves the point: it parses the exact same `owner:` clause this
new axis uses, and **throws away who posted it**, keeping only the receiver's tally. The board has been
carrying a directed graph in plain text the whole time and no instrument has ever read an edge.

That gap is not cosmetic, and it is exactly what Sueur et al. predict: **topology is not a property the
histogram contains.** A colony can be perfectly EVEN in `[done]` output — `mesh-forage` renders
`BALANCED`, every existing axis green — while its assignment graph is a one-way star into a single lane.
The marginal reads healthy right up until that lane stalls, at which point most filed work stops at once.

## What it measures on the REAL board (measured, not assumed)

Ran against the live `~/.mesh/chat.log`. The graph is real and non-degenerate:

- **720h window:** 22 edges over 15 lanes, 67 assignments, **reciprocity 0.0909**, sink `genome` 0.3433.
  Trail: `land->minds:18 discover->genome:10 tg->genome:7 discover->senses:6 …`
- **72h window:** 5 edges, **reciprocity 0.0000**, sink `minds` **0.6667** → both notes raised, plus
  isolates `pub senses vpn`.

So the mesh's constructed social niche is a **near-pure one-way hierarchy**: ~9% of ordered pairs are
mutual, and a lane that receives work essentially never files work back to the lane that sent it. That is
a structural finding no existing axis could state, and it was invisible while every marginal read fine.

## The application (landed)

`scripts/mesh-forage` — new `social()` function + config + JSON fields + text block + tests.

The one edge the board carries **verbatim, with no prose inference**: a `[task]` whose poster names
another window in `owner:` = `poster --assigns--> owner`. Self-assignments are dropped (not social); the
poster's `who@node` is the sender. Three reads, all report-only and rc-neutral like every other additive
axis here:

- **`reciprocity`** — fraction of ordered pairs `A->B` whose reverse `B->A` also exists. Below
  `MESH_FORAGE_SOCIAL_RECIP` (0.20) → the one-way/star note.
- **`sink share`** — top receiver's share of assignment *weight*. At/above `MESH_FORAGE_SOCIAL_SINK`
  (0.50) → the topological single-point-of-failure note, naming the lane.
- **`isolates`** — real mind lanes (guarded by `MESH_FORAGE_LANES`, the same anti-forge discipline the
  division-of-labour axis uses) that **posted** in the window but sit in **no edge in either direction**:
  neither delegating nor delegated to. Outside the constructed social niche entirely.

Honest n/a below `MESH_FORAGE_SOCIAL_FLOOR` (4 edges) — and **the isolate list is suppressed when
blind**, in the JSON renderer as well as the text one. That suppression was a live bug caught during the
build: below the floor there are no edges, so *every* posting lane is trivially edge-less and the JSON
shipped `"social_isolates":"discover health genome witness sound senses"` — an all-lanes-isolated
"finding" that was an artifact of the **missing** graph, not a reading of one. A blind axis that ships a
plausible positive is the silent-fallback shape from the doctrine.

## The gates were seen RED (falsifiers, not decoration)

The fixture pair is the falsifier. `STAR` and `MUTUAL` are built to carry the **identical marginal** —
same 4 lanes × 3 `[done]`, same `evenness_J`, same `done_marks`, same `assigned_tasks` — and differ
**only in the edges**. The test asserts that equality first (`"evenness_J":1.0000 "done_marks":12
"assigned_tasks":4` on both), so any difference downstream is topology alone. If the axis were reading a
marginal, or a constant, the two fixtures would be indistinguishable. Star flags both notes; mutual is
clean. Also asserted: a self-assignment is not an edge, a prose `[fyi]` mentioning `owner: genome` is not
an edge, a non-lane poster (`loadaudit`) cannot forge an isolate, and both thresholds drop their notes
when moved past the measured value.

Three mutants run **from a scratch copy**, all RED for the right reason:

| mutant | result |
|---|---|
| `recip = 1.0` (constant "mutual network" lie) | RED — *star fixture reciprocity must be 0* + *star must raise the one-way note* |
| `sink = 0` (constant "never a single point of failure") | RED — *star sink share must be 1.0* + *star must raise the sink note* |
| blind-suppression removed | RED — *blind axis still ships an isolate list* |

`--test` cost: **6.92s → 7.57s** (+0.65s). The new cases stub `MESH_FORAGE_PROMISES="false"` so they do
not pay for a real `mesh-promises` call — without the stub the suite ran 10.05s, still inside
`mesh-doctor`'s 60s cap and `mesh-land`'s 30s, but the axis does not need the promise ledger and should
not be charged for it.

## Discarded, with reasons

- **Borger, Czuppon & Dammhahn, "The evolution of niche construction in social species"**
  ([ecoevorxiv 11484](https://ecoevorxiv.org/repository/view/11484/), 2026-01-19) — NC evolves without
  ecological inheritance when population structure creates multilevel selection (cheaters win *within*
  group, cheater-free groups win *between*). Genuinely on-area and tempting, but the mesh already landed
  a multilevel-selection instrument on 2026-07-31
  (`oee-multilevel-selection-signature-productive-doomed-lineages-mesh-vitality`, `mls_conflict()`), and
  the mesh has **no between-lane selection at all** — no lane dies for free-riding — so the paper's
  central condition is absent and the transfer would be decorative.
- **Coco, Davies & Thompson, "Low-cost niche construction can create conditions for subdivided
  populations"** ([osf.io/r64cz_v2](https://sciety.org/articles/activity/10.31235/osf.io/r64cz_v2),
  2025-12-19) — low-cost landscape modification → legacy landscapes → denser, less mobile, *smaller*
  social networks. Same family as the finding above but the mechanism is a spatial-resource simulation
  with no mesh referent (the board has no space, no mobility, no forage cost gradient).
- **"Extended phenotypes: a new generation"**, *Trends in Genetics* 41 (Dec 2025),
  doi:10.1016/j.tig.2025.10.004 ([PMID 41298186](https://pubmed.ncbi.nlm.nih.gov/41298186/)) — the
  extended-phenotype field's "mechanistic phase" (effectors, toxins, zombies, dependency). **No abstract
  is published** and the full text is paywalled (cell.com 403); building on a search-engine paraphrase
  of a paper I could not read would be a claim, not a reading.
- **"Humans as an extended phenotype of their microbiota"**, *Theory in Biosciences* (2026),
  doi:10.1007/s12064-026-00477-8 — host-symbiont behavioural manipulation. Real and recent, but the mesh
  has no host/symbiont asymmetry to map it onto; forcing it would be an analogy, not a transfer.

## State

Uncommitted in the tree, for the steward:

- `scripts/mesh-forage` — `social()` + `MESH_FORAGE_SOCIAL_{FLOOR,RECIP,SINK}` + JSON fields
  `social_edges` / `social_nodes` / `social_reciprocity` / `social_sink_share` / `social_sink_lane` /
  `social_assignments` / `social_edge_trail` / `social_isolates` + text block + the fixture-pair tests.
- `docs/reviews/niche-construction-collective-social-network-topology-forage-2026-08-03.md` (this file).

`mesh-forage --test`: **PASS**. Genome source only — the deployed `~/.local/bin/mesh-forage` is
untouched (steward deploys via `mesh-sync-tools`).

Related: [[mesh-forage-pheromone-entropy]] · [[oee-alife-coverage]] ·
[[a-sub-axis-is-not-the-verdict]] · [[fusion-must-gate-real-blind-sentinels]]

# The representation embodies the observer — the mesh has 15 OEE reviews and not one looks outward

**Live literature review, 2026-08-25, genome mind.**
Area: artificial life & open-ended evolution, angle = a **cross-domain transfer to a distributed
sensor mesh**.
**Arm:** treated (assigned)
**Target organ (assigned by coin, p=0.20, drawn uniformly from the 567 never-reviewed tools):**
`scripts/mesh-object-id`. Not chosen by me, not chosen by the lane.
Status: landed, **uncommitted in the tree** — steward lands.

---

## The structural fact the coin walked into

Before searching I counted where this lane's OEE work has actually landed. Fifteen reviews:

| landing site | count |
|---|---|
| `mesh-vitality` | 11 |
| `mesh-ideate` | 3 |
| `mesh-novelty` | 1 |
| `mesh-link-heal` | 1 |
| **a perceptual organ** | **0** |

Every one measures the open-endedness of the mesh's own *code* or *ideas*. **The mesh has never once
asked whether its WORLD is open-ended.** The task asked for a cross-domain transfer to a sensor mesh
and the coin handed me an eye. That is the transfer, and it was not available to be noticed until the
assignment forced the count.

## What was already ours (so this could not re-land)

Checked first, and it eliminated the three most obvious candidates:

- **Bedau–Packard neutral shadow run** — landed 2026-08-04 (`oee-neutral-shadow-new-adaptive-activity-mesh-vitality`).
- **MODES persistence filter + ecology hallmark** (Dolson, Vostinar, Wiser & Ofria, *Artificial Life*
  25(1), 2019) — landed 2026-07-29 in `mesh-vitality` (`inheritance_mu`, `ecology_potential`).
- **Stepney & Hickinbotham model-escape / descriptor coverage** — landed 2026-08-15.
- `mesh-novelty` is Shannon surprisal over the **board**, i.e. over our own event stream — information
  theory, not OEE, and again inward-facing.

## The find

**Kumar, Lu, Kirsch, Tang, Stanley, Isola & Ha, "Automating the Search for Artificial Life with
Foundation Models" (ASAL)** — arXiv:2412.17799 (23 Dec 2024, rev 16 May 2025), published in
*Artificial Life* **31**(3):368 (MIT Press).

Its **Search for Open-Endedness** defines novelty with **no hand-built component partition**: embed
each frame with a foundation model, and score timestep *T* against **all** previous timesteps *T′ < T*
— the OE score is **one minus the maximum similarity to history** (historical nearest-neighbour
novelty; the paper reports it beats variance-based novelty). The sentence that decided the whole shape
of this landing:

> "this formulation outsources the subjectivity of measuring open-endedness to the construction of the
> representation function, **which embodies the observer**."

**The concept we do not embody:** a novelty number is meaningless without the name of the
representation that produced it, and where there is no representation there is **no novelty** — not a
degraded one, and emphatically not a string comparison wearing the same word.

## Why this organ, and not a stretch

`mesh-object-id` is the **only mesh tool that already runs a vision-language foundation model on real
frames**. It had the representation function in hand, used it to emit a *name*, and then discarded the
observation entirely — no archive, so the node could never answer *"have I seen this before?"*.

And a naive fix is worse than none. `"a mug"`, `"a white ceramic mug"` and `"white mug on a desk"` are
one object in three phrasings; a byte-exact archive keyed on the answer string reports novelty 1.000
forever and **manufactures open-endedness out of phrasing**.

**Measured on this node, not assumed** (`all-minilm:latest`, 1−cos):

| pair | novelty | byte-exact key would say |
|---|---|---|
| `a mug` vs `a white ceramic mug` | **0.256** | 1.000 |
| `a mug` vs `white mug on a desk` | **0.280** | 1.000 |
| `a bicycle` vs `a bike leaning on a wall` | **0.392** | 1.000 |
| `a mug` vs `a black office chair` | **0.719** | 1.000 |
| `a mug` vs `a bicycle` | **0.814** | 1.000 |

n=5 hand pairs — a calibration sample, not a corpus. The paraphrase band (0.26–0.39) and the distinct
band (0.72–0.81) do not overlap, but the bike pair is close enough that one global threshold is not
safe yet. So the raw novelty is **always** published, `NEW_AT` is a provisional knob, and the gate
asserts the **relation** (paraphrase < distinct), never a constant — it cannot rot when the observer
model changes.

**The visual observer ASAL actually used is not available here, and that is measured.**
`llmvision/glimpse-v1` (family `clip`) is pulled locally, and **both** `/api/embed` and the legacy
`/api/embeddings` return an empty `embeddings` array for an image on this ollama. So the observer in
use is **linguistic** — it sees only what the VLM chose to *say*, strictly weaker than seeing the
frame. That weakness is printed in every line rather than hidden. `observer=` is the whole point.

## What was landed

`scripts/mesh-object-id` — the memory this organ never had:

- `~/.mesh/object-id-archive.jsonl`, one row per observation (ts, answer, observer, kind, embedding,
  novelty), bounded and self-trimming.
- **Historical-NN novelty** = 1 − max cosine similarity over all prior rows — ASAL's score, transferred
  in form. `--novelty` prints it with the nearest neighbour named; `--archive` summarises.
- **Rows from a different observer are invisible to the score.** Two representation spaces are not one
  space; mixing them computes a distance between coordinates that mean different things.
- **An empty embedding is a failure, not a zero vector** — the live `glimpse-v1` shape. Treating it as
  a vector would pin novelty at 0.000 and make a blind organ report perfect familiarity.
- **Three n/a shapes kept apart:** no history (`na` — the first sighting has nothing to be novel
  *against*; scoring it 1.000 mints a discovery out of an empty archive), blind frame, and no
  representation (`observer=none`).
- **stdout contract unchanged:** line 1 is still the bare answer; the novelty line is opt-in.

## Two defects the review found by actually running it

Both were mine, both were caught live, and both are now gated.

**1. A refusal was being archived as a sighting.** Running the tool on two real dark frames, both
returned *"Cannot identify due to extreme darkness and blurriness."* and the second scored **novelty
0.000 "seen-before"** — the node reporting *recognition* of a frame it could not see, with `n` counting
blindnesses as observations (`a-blindness-sentinel-fused-as-a-reading`). Blind rows are now excluded
from the neighbour set: two frames the model could not read are two failures agreeing, not a
recognition. The cut keys on a sentinel token the prompt itself asks for — our own grammar, not a
phrase list that would invert the first time the model rewords itself — and the gate asserts the live
`BASE_PROMPT` still asks for it.

**2. Adding the sentinel made the eye blinder, and that is not a formatting change.** The first
wording ("if the image is too dark, blurry, or empty to identify anything, begin with the token") made
qwen3-vl refuse `bruno-imac-now.jpg` — a frame it had answered *minutes earlier* with "bed, nightstand,
humidifier, dumbbell, yoga mat bag, exercise equipment". **Offering an easy exit lowers the bar for
taking it**, and a novelty archive fed by a newly timid eye would record blindness where the world was
legible. The prompt now asks for partial identification explicitly and makes the token a last resort;
re-verified against that same frame as the control, which identifies again and in more detail.

A third, smaller one: the sentinel leaked to stdout twice over — the cut sat *after* the `echo`, and
the hand-listed separator class missed the em-dash the model actually emitted
(`an-enumerated-alphabet-is-a-copy-that-rots`). Both halves are gated now.

## Gate, seen red

Live end-to-end on real frames: first sighting → `na`; same scene again → `0.000 seen-before` naming
its neighbour; dark frame → `blind`; second dark frame → still `na`, **not** "seen-before". Archive
summary splits `sightings=2 blind=2`.

Five independent mutations, each red for its own reason:

| mutation | red on |
|---|---|
| blind rows scored as neighbours again | reproduces the live `0.000 seen-before` bug verbatim |
| empty archive scores 1.000 instead of `na` | no-history arm |
| foreign observer's rows mixed into the score | representation-space arm |
| prompt stops asking for the sentinel | prompt/predicate one-contract arm |
| hand-listed separator class restored | em-dash leak arm |

## Weakest joints, stated

- The observer is **linguistic, not visual** — it can only be as good as the VLM's phrasing, and two
  visually different scenes described identically will read as one. ASAL's own choice was the frame
  embedding; that path is measurably closed on this ollama and should be re-tried when image embedding
  lands.
- `NEW_AT=0.55` is provisional off n=5 hand pairs. The archive it now writes is exactly the corpus
  that should replace it — nothing consumes the `NEW`/`seen-before` verdict yet, deliberately.
- Trimming the archive shrinks the history novelty is scored against, so a long-absent object can read
  novel again. `--archive` publishes `n` so a reader can see the horizon it is speaking from.

## Sources

- [Kumar, Lu, Kirsch, Tang, Stanley, Isola & Ha, *Automating the Search for Artificial Life with Foundation Models*, arXiv:2412.17799](https://arxiv.org/abs/2412.17799) · [project page](https://sakana.ai/asal/) · [*Artificial Life* 31(3):368](https://direct.mit.edu/artl/article/31/3/368/132866/Automating-the-Search-for-Artificial-Life-With)
- [Dolson, Vostinar, Wiser & Ofria, *The MODES Toolbox*, *Artificial Life* 25(1):50](https://direct.mit.edu/artl/article/25/1/50/2915/The-MODES-Toolbox-Measurements-of-Open-Ended) — checked as a candidate; already ours since 2026-07-29.
- [*Open-Ended Evolution*, ALife Encyclopedia](https://alife.org/encyclopedia/introduction/open-ended-evolution/) — the shadow-run and noise-filtering background; already ours since 2026-08-04.
- [Akhtyrchenko, Katsnelson & Ustyuzhanin, *Directing Open-Ended Evolution in Artificial Life via Multi-Scale Path Divergence*, arXiv:2606.17091](https://arxiv.org/abs/2606.17091) — read as the newest candidate (Aug 2026); its renormalization-group metric over transition laws needs a *system* with transition laws, which a one-shot object identifier does not have. Discarded honestly rather than stretched.

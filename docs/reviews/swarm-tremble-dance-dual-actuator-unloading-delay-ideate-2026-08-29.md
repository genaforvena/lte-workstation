# Swarm intelligence & stigmergy — the tremble dance: ONE delay, TWO opposite actuators

**Live review · genome@mesh-home · 2026-08-29**
**Angle:** CROSS-DOMAIN transfer — a colony-regulation mechanism applied to a distributed sensor mesh.
**Target organ:** `scripts/mesh-ideate` (the mesh's idea producer, `# reflex-cadence: 14-59/15`).
**Verdict:** it applies, and it lands on a defect that was LIVE on this node while I was reading.

---

## Why this area needed a new landing at all

19 swarm reviews already sit in `docs/reviews/` (cross-inhibition, ant mill, response-threshold
division of labour, tunable quorum, density-adaptive evaporation, no-entry repellent, inverse
stigmergy, tandem runs, sematectonic-vs-sign-based, pheromone entropy…), and last night's
`lit-review-stigmergy-watchtower-2026-08-28.md` imported the third pheromone operator (DIFFUSION).

Two candidate imports were checked and **discarded because we already embody them**, which is worth
recording so the lane does not re-walk them:

- **Efficiency sensing** (Redfield 2002 *Trends Microbiol*; Hense et al. 2007 *Nat Rev Microbiol*;
  live continuation in Thomas et al., *PLOS Biology*, 2025-09-04). Already embodied, in depth:
  `scripts/mesh-bt-census` carries the whole argument in its header and recovers the detection
  probability `p` from stationary anchors (`p̂ = 0.991`, 3196 anchor-ticks, 2026-08-17).
- **Combinatorial quorum sensing** — two signals with different half-lives, whose RATIO separates
  population density from mass transfer (Cornforth et al., *PNAS* 111:4280, 2014; Thomas et al. 2025
  above). A real step past efficiency sensing, but on this mesh the anchor trick already yields `p`
  directly, so the second signal buys little. Discarded as marginal, not as wrong.

## The mechanism I am importing

**The honeybee TREMBLE DANCE** (Seeley 1992, *The tremble dance of the honey bee: message and
meaning*, Behav Ecol Sociobiol; vibrational analysis in Kirchner 1993, *Behav Ecol Sociobiol*
33:169–172; the live continuation on trigger classes in Thom 2003 and the delay-/non-delay-type
split reported since).

A returning nectar forager cannot unload herself — she must hand her load to a food-storer bee. She
measures **her own search time for a receiver**. Past roughly 50 s she stops waggle-dancing and
tremble-dances instead, and that single signal drives **two actuators in OPPOSITE directions**:

1. it **suppresses** recruitment of more foragers (down-regulates the producer), and
2. it **recruits more food-storers** — it *raises the colony's processing CAPACITY*.

The half that matters here is (2), and it is the half that is easy to miss. The forager never
observes the storer pool. She observes only her own **wait**, and that wait is the *only unbiased
observable of downstream capacity that requires no instrumentation of the consumer at all*. A colony
with the suppressor alone would forever down-regulate intake to match a capacity it never measures
and never grows.

**The transferable claim, stated as a rule:**

> A producer's own WAIT-FOR-HANDOFF is the only unbiased observable of its consumer's capacity, and
> one such measurement must drive TWO actuators in opposite directions — throttle the producer AND
> enlarge the receiver side. A count of undelivered items is not that measurement, and a system that
> owns only the throttle converges on a starved consumer pool it can never see.

## What we do not embody

`scripts/mesh-ideate` has a FLOOR gate (`IDEATE_FLOOR`, default 1): it holds the next mint while
`grep -c '^\[ \]' ideas-queue` is at or above the floor. That counts ideas **minted and not yet
picked up** — the nectar lying undelivered on the hive floor. It is not the quantity a colony
regulates on, and on this node the two numbers do not merely differ, **they point in opposite
directions.**

Measured live, 2026-08-29T22:5xZ:

```
open [ ] = 0                                   <- the ONLY thing the shipped gate reads
tremble inflight=28 aged=27 unknown=1 wait=1034h cov=aged:27/28 wait_floor=1 threshold=48h
oldest: [~] STUDY(fault tolerance): Implement JIT compilation of worker inference code …  (43.1 d)
median in-flight wait 9.9 d · 11 of the 28 sit in the first 53 lines of an 1844-line append-only queue
```

The floor reads **empty**, so the producer is unthrottled and mints on its next 15-minute tick —
and it reads empty *precisely because* every one of those 28 ideas was picked up and never unloaded.
This is the exact failure the tremble dance evolved against, reproduced by counting the wrong column.

Two further mesh-specific findings:

- **The reaper cannot drain them, by its own design.** `mesh-queue-tend`'s tilde-reaper uses
  `REAP_WINDOW=86400`, so a 43-day `[~]` is 43× past it and survives only via the PARK
  (blocked-on-external) and KEEP (token/semantic-matched) arms. Those arms are correct — a blind
  close would lose undone work — but their product is a **permanently parked population that is
  invisible to the reaper AND to the producer's only gate**. It exerts no backpressure and nobody is
  ever asked to enlarge the side that would clear it.
- **Every existing backpressure in this mesh is a suppressor.** `IDEATE_FLOOR` holds; `mesh-pace`
  holds on spend; dispatch holds a slot. The mesh has many throttles and one unilateral reaper.
  It has **no organ anywhere that converts a congestion measurement into an ask for more receivers**.
  That is the imported half.

## What landed (`scripts/mesh-ideate`, uncommitted in the tree)

A second, INDEPENDENT hold beside the floor gate, keyed on the **wait** and never on a count, plus
the recruit arm:

- `tremble_measure()` — joins each in-flight `[~]` line to `mesh-queue-tend`'s existing sidecar
  `~/.mesh/.ideas-tilde-seen` (`sha1(full line)<sp>first-seen-epoch`) and publishes one field line:
  `inflight= aged= unknown= wait= cov= wait_floor=1 threshold=`.
- `mesh-ideate --tremble` — read-only verdict. `0` below threshold · `1` TREMBLE · `2` n/a.
- The **hold**: past `MESH_IDEATE_TREMBLE_WAIT` (default 172800 = 2× the reaper's own window, so the
  reaper has already declined to drain the item at least once) the mint is held, loudly, printing the
  measurement.
- The **recruit** (`tremble_recruit`): the same measurement posts ONE routable board
  `[task] … owner: mesh-queue-tend/minds` asking for the oldest handoffs to be closed or retired, or
  the receiver side widened — throttled to one per 6 h, never from `--dry`.

**Honesty terms, none of them renderable as `0`:**

- ages come from a sidecar first stamped at the reaper's first run, so every wait is a LOWER BOUND —
  published as `wait_floor=1`, never as an exact age;
- an in-flight line with no sidecar row is `unknown=`, **never folded into the fresh side** (stamping
  it `now` is exactly the direction that silences the gate — it is mutant M2 below, and it is live:
  the real reading carries `unknown=1`);
- `cov=none` (nothing in flight) and `cov=no-age-store` (the instrument is missing) are **different
  words with opposite remedies**, and neither may print `wait=0h`;
- an unknown wait **never holds** — the gate fails toward the pre-existing behaviour and says why.

## Gates seen RED

`--test` arm added (8 assertions). Control green; five mutants driven red from a scratch copy:

| # | mutation | caught by |
|---|---|---|
| M1 | `tremble_holds` → `false` (floor-only suppression) | 43-day wait no longer holds the mint |
| M2 | missing age stamped `now` (unknown rendered fresh) | `wait=0h` printed; n/a became a verdict |
| M3 | gate keyed on `TR_INFLIGHT >= 3` instead of the wait | the count/wait discriminator arms, both directions |
| M4 | recruit throttle removed | second recruit leaked into the same window |
| M5 | `tremble_recruit` dropped (suppression only) | the hold fired with no receiver-side ask |

One real bug the arms found in themselves and it is worth carrying out of here:
`$(grep -c PATTERN f || echo 0)` **captures `"0 0"`** — `grep -c` prints `0` *and* exits 1 on no
match, so the fallback fires too and every zero-count arm fails while reporting a count nobody wrote.
Take grep's stdout as the answer; its rc is not it. (Same family as
`[[echo-rc-after-a-pipe-reports-the-last-stage]]`.)

## Not deployed, by instruction

The edit is in the genome source only; `~/.local/bin/mesh-ideate` is untouched, so the `14-59/15`
cron still runs the old gate and **no recruit post has been made to the live board**. Deploy lands
with the steward. The read-only `--tremble` above was driven from the tree copy.

## Sources (read live, 2026-08-29)

- Seeley, T.D. (1992) *The tremble dance of the honey bee: message and meaning*, Behavioral Ecology
  and Sociobiology 31:375–383 — the delay trigger and the dual effect.
- Kirchner, W.H. (1993) *Vibrational signals in the tremble dance of the honeybee, Apis mellifera*,
  Behav Ecol Sociobiol — https://link.springer.com/article/10.1007/BF00216597 — artificial tremble
  sounds inhibit dancing and reduce recruitment (the suppressor arm, isolated).
- Thom, C. (2003) and the follow-on literature on delay- vs non-delay-type tremble dancing — about
  half of natural tremble dances begin with no in-hive delay, so the signal is not a pure queue
  readout. https://en.wikipedia.org/wiki/Tremble_dance (entry point; primary refs therein).
- Discarded-as-embodied, for the record: Redfield (2002) https://pubmed.ncbi.nlm.nih.gov/12160634/ ·
  Hense et al. (2007) https://www.nature.com/articles/nrmicro1600 · Cornforth et al. (2014)
  https://www.pnas.org/doi/10.1073/pnas.1319175111 · Thomas et al. (2025) *PLOS Biology*
  https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.3003316

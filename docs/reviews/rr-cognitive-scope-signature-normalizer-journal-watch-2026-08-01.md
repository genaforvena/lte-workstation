# RR live review — COGNITIVE SCOPE (compression ↔ particularization): measure the normalizer, not its output

**Date:** 2026-08-01 · **Channel:** genome@mesh-home · **Target:** `scripts/mesh-journal-watch`
**Landed (uncommitted):** `mesh-journal-watch --scope` — report-only posture read. rc 0 BALANCED/NO-DATA · 3 OVER-COMPRESSED · 4 OVER-PARTICULARIZED.

---

## 1. Where the literature landed

Vervaeke's relevance-realization account solves the frame problem by **opponent processing** — a set of
trade-off pairs an agent continuously re-balances rather than a rule for what is relevant. The mesh already
instruments two of the pairs and the general opposition that subsumes them:

| pair | mesh organ | landed |
|---|---|---|
| efficiency ↔ resiliency (the general opposition) | `mesh-sensorium --balance` | 2026-07-28 |
| exploration ↔ exploitation | `mesh-needs --balance` (demand-tracking edge) | 2026-07-28 |
| focusing ↔ diversifying (cognitive **tempering**) | `mesh-novelty --tempering` (arousal-coupled) | 2026-07-30 |
| **compression ↔ particularization (cognitive SCOPE)** | **— nothing —** | **this review** |

The remaining pair is named explicitly in the current literature:

> "trade-offs involved can be subsumed under the general opposition of efficiency vs. resilience or, more
> specifically, as **generality vs. specialization**, exploration vs. exploitation, and focusing vs.
> diversifying"
> — Jaeger, Riedl, Vervaeke et al. (2024), *Naturalizing relevance realization: why agency and cognition are
> fundamentally not computational*, **Frontiers in Psychology 15:1362658**, §3.
> <https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1362658/full>

And it is the pair with the sharpest **operational** statement, which is why it is implementable at all —
Vervaeke/Lillicrap/Richards put it as a fit problem, not a philosophy:

> compression is "analogous to finding the line of best fit for data", while particularization is
> "allowing the function to move towards over-fitting to the data"
> — *Relevance Realization and the Emerging Framework in Cognitive Science*, **Journal of Logic and
> Computation 22(1):79–99 (2012)**, <https://academic.oup.com/logcom/article-abstract/22/1/79/1007787>

The frame-problem framing is the same in the live 2025 stream (Andersen/Miller/Vervaeke,
*Predictive processing and relevance realization*, **Phenom. & Cog. Sci. 24:359–380**,
doi:10.1007/s11097-022-09850-6; Darling/Corcoran/Hohwy, *Solving the relevance problem with predictive
processing*, **Philosophical Psychology**, doi:10.1080/09515089.2025.2460502, online 2025-02-02) — but
those two both land on **precision-weighting**, which the mesh already embodies in `mesh-precision`. Scope
is the un-taken ground.

**Live empirical corroboration from an adjacent, actively-published field.** The scope trade-off is not a
metaphor for log processing — it is measured there. In log anomaly detection, the "signature" of a message
is produced by a template extractor (Drain3), i.e. exactly a compression map over raw lines:

> "On BGL, **79.8% of anomalous test lines originate from EventIDs not matched by any Drain3 template
> extracted from the offline region**, indicating substantial temporal concept drift."
> — Wang, Huang, Tian, Dzeparoska, Jacobsen & Leon-Garcia, *FAME: Failure-Aware Mixture-of-Experts for
> Message-Level Log Anomaly Detection*, **arXiv:2605.22779v1** (2026-05-21),
> <https://arxiv.org/abs/2605.22779>

A signature alphabet fitted on one window under-covering the next is the **measured** failure of a fixed
normalizer — the particularization pole, in the wild, at 79.8%. The complementary result — that the choice
of normalization form is load-bearing rather than neutral plumbing (a rewrite of Drain3 template ids lifts
mean F1 from 88.53% to 97.00% on BGL) — is in *NLLog* (arXiv:2606.04957, 2026-06),
<https://arxiv.org/html/2606.04957>.

---

## 2. The gap in this mesh

`scripts/mesh-journal-watch` is the node's live `-p err` fault sense. Its entire behaviour — dedup, the
persistent `SEEN` set, "novelty is the signal", the burst cap — rests on one four-token function:

```bash
normalize(){ sed -E 's/0x[0-9a-fA-F]+/0xN/g; s/\b[0-9a-f]{8,}\b/HEX/g; s/[0-9]+/N/g'; }
```

**That function IS the compression map.** It decides the *alphabet of faults this node can name at all*.
It was chosen a priori, its header asserts a compression claim ("12,198 rtw lines collapse to one alert")
that was never measured, and nothing anywhere reads back where it actually sits on the scope axis. Both
poles fail, and they fail asymmetrically:

- **OVER-COMPRESSED (the silent pole).** Distinct faults fold into one signature, so faults #2..n are
  *never announced* — the first one burned the single alert. Green, cron-fresh, mtime-live, and blind.
  This is the dead-lane shape; `mesh-reflex-health` cannot see it, because the reflex genuinely ran.
- **OVER-PARTICULARIZED (the storm pole).** Every line mints a fresh signature, `SEEN` never converges,
  `new=yes` stops meaning anything, and the burst cap is the only thing between the board and a storm.

This is cognitive scope proper, and it is a *different* quantity from the two RR measures the mesh already
has. `mesh-novelty --tempering` measures **gain** (how wide the attention is). `mesh-correlate --posture`
measures a **detector threshold** (where the emit floor sits relative to the data's ceiling). Neither looks
at the **symbol-formation map** — the alphabet in which a fault can be expressed before any threshold or
gain applies. A sense whose alphabet cannot distinguish two faults is not mis-tuned; it is *mute* about the
distinction, at every threshold.

---

## 3. What was built — `mesh-journal-watch --scope`

Report-only, no state change (it reads the **current boot** like `--once`, never the cursor, so a posture
read can never consume a delta the real pass owes the board, and never forges an artifact a watchdog reads
for liveness). Per signature bucket it counts occurrences `n`, distinct raw messages `d`, and how many of
those raws **recur** (`r`).

**DEGENERATE** — a signature body with no alphabetic character. It discriminates nothing; anything landing
in it is silent forever after the first hit.

**IDENTITY-FOLD** — `d ≥ 2` **and** `d ≤ IDCAP` (default 4) **and** `r ≥ 2`. The discriminator is the
recurrence structure, not "the bucket holds more than one raw": a folded slot whose values are a *small,
stable, re-visited set* is an **enumerable identity** (`hw:0`/`hw:1`, `hci0`/`hci1`, a usb port), whereas a
slot walking forward through fresh values is a **counter**, which `normalize()` is right to fold. Only the
former means "`normalize()` folded away *which thing* faulted, and only the first ever alerted".

**OVER-PARTICULARIZED** — `signatures ≥ MINSIG` (8) and singleton-signature rate ≥ `SFLOOR` (0.90): the
alphabet never converges. Requires a converged-enough sample; 3 singletons is not evidence of anything.

Verdict precedence: when both poles hold, the **silent pole wins** (a blind sense outranks a loud one) and
the line names the other. `NO-DATA` on an empty stream is its own answer, never a faked `BALANCED`.

Knobs: `MESH_JOURNAL_WATCH_IDCAP` / `_SFLOOR` / `_MINSIG`. No other code path reads them; every existing
subcommand is byte-identical (179 insertions, 1 deletion — the smoke-test banner).

### Live artifact — it caught a real one on the first run

```
$ mesh-journal-watch --scope
  DEGENERATE     n=1     raws=1    [kernel|||]  <- no alphabetic content: absorbs anything
records=27  signatures=8  compression=0.704  singleton-rate=0.50  degenerate=1  identity-fold=0
scope: OVER-COMPRESSED
rc=3
```

`kernel|||` is a **live absorbing bucket** on mesh-home right now. A `-p err` journal record with no
`MESSAGE` field falls through `(.MESSAGE // "")` to the empty string, normalizes to nothing, was posted to
the board on 2026-07-31T22:30:01Z as a `NEW fault` whose sample text is literally `kernel: `, and is now in
`SEEN` — so **every future message-less error record on this node is permanently silent**, and the one alert
it did spend carried zero information. That is the compression pole, measured, on the tool's own stream.
(Compression 0.704 and singleton-rate 0.50 are healthy; the fault is one specific bucket, not the map
overall — which is exactly why a bucket-level report beats a single ratio.)

---

## 4. Gate — RED-first, 9/9 mutants killed

`--test` grew cases (7)–(15): a **live real read** of this node's own stream (rc ∈ {0,3,4} + a verdict
line — a posture read that only ever sees fixtures asserts nothing about this node), a **no-state-written**
assertion, both poles, the OOM-probe exclusion, the MINSIG floor, and NO-DATA≠BALANCED.

Two falsifiers assert the IDENTITY-FOLD discriminator's guards **separately**, because a single combined
falsifier let either one be deleted:

- **(11a)** small set, nothing revisited (`d=2, r=0`) → must stay BALANCED — kills "drop `r>=2`".
- **(11b)** large set, everything revisited (`d=6, r=6`) → must stay BALANCED — kills "drop `d<=IDCAP`".

The first draft of the gate had one combined falsifier (`d=5, r=0`) and **two mutants survived it** —
dropping either guard alone still passed. Recorded because it is the shape the doctrine warns about: a gate
you have not seen fail is not a gate, and a falsifier that trips only when *both* guards are removed asserts
their conjunction, not either one.

| mutant | result |
|---|---|
| M1 drop the DEGENERATE check | RED (9) |
| M2 drop the recurrence term `r>=2` | RED (11a) |
| M3 drop the IDCAP ceiling | RED (11b) |
| M4 drop the singleton rule | RED (12) |
| M5 NO-DATA falls through to BALANCED | RED (14) |
| M6 `--scope` writes state | RED (8) |
| M7 verdict ignores identity-fold | RED (10) |
| M8 axis-inert (always BALANCED) | RED (9) |
| M9 drop the OOM exclusion inside `--scope` | RED (15) |

Unmutated tree: green. Default pass, `--once`, `--status`, `--reset` unchanged.

---

## 5. Not wired

`--scope` is **not** in cron and not consulted by any reflex — that is the steward's call. It is a posture
read, not a gate; wiring it would make a normalizer-tuning judgement automatic, which nothing here has
earned yet. The immediate actionable item it produced is independent of wiring: **the `kernel|||` bucket
should be dropped before signature/dedup** (a record with an empty `MESSAGE` is not a fault signature), and
`SEEN` re-seeded for it. Left unfixed and unlanded here so the finding is visible rather than quietly
absorbed.

# Live review — information theory of agency: empowerment is a CHANNEL CAPACITY, and we have been computing the achieved flow

**Date:** 2026-08-04 · **Window:** genome · **Seam:** empowerment / predictive information (live literature)
**Status:** BUILT (report-only, on-demand) — `scripts/mesh-algedonic --agency-capacity`
**Angle asked for:** a foundational idea we may have MISread or applied too loosely. This is that, exactly:
not a new mechanism from the frontier, but the definition under six months of mesh empowerment work.

## The source

**Christoph Salge, Cornelius Glackin, Daniel Polani — "Empowerment — an Introduction",
[arXiv:1310.1863](https://arxiv.org/abs/1310.1863)**, published as ch. 4 of *Guided Self-Organization:
Inception* (Springer, 2014). This is the canonical statement of the measure that `mesh-algedonic`,
`mesh-interruptibility`, `mesh-promises --empowerment` and `mesh-precision` all cite downstream. Reached by
searching the live 2026 empowerment literature for the capacity-vs-MI distinction; the surfaced 2026 papers
(arXiv:2605.06346 bridge interfaces, arXiv:2604.21155 multi-agent, arXiv:2509.22504 EELMA) were all already
reviewed here — the unvisited ground turned out to be *behind* us, in the definition itself.

Verified verbatim against the PDF text (not a summarizer's paraphrase — a fetch tool's quote is a claim):

> **§4.4.2, Eq. 4.7** — `E := C(A_t → S_{t+1}) ≡ max_{p(a_t)} I(S_{t+1}; A_t)`
>
> "Note that the maximization implies that it is calculated under the assumption that the controller which
> chooses the action A is free to act, and is **not bound by possible behaviour strategy p(a|s,m)**.
> Importantly, the distribution p\*(a) that achieves the channel capacity **is different from the one that
> defines the actions** of an empowerment-driven agent."

> **§4.4.1** — "empowerment considers the maximal potential information flow, i.e. it is **not based on the
> actual distribution of the input variable X** (with or without intervention), but considers the maximal
> information flow that could possibly be induced by a suitable choice of X. This, however, is nothing other
> than the **channel capacity** `C(X → Y) = max_{p(x̂)} I(X̂; Y)`."

> **§4.4.7** — for the non-deterministic case "the optimizing distribution needs to be determined using the
> standard **Blahut-Arimoto (BA) algorithm** (Blahut 1972; Arimoto 1972)".

## The misread

Every empowerment number in the mesh is the **plug-in MI at the empirical action frequency p̂(a)** —
`mesh-algedonic:mi_of()` and its three descendants (open-loop `AGENCY_INFO`, the closed-loop conditional,
the per-actor interference strata). That quantity has a name in the same lineage: it is Ay & Polani's
**actual / causal information flow**. It is a *lower bound* on empowerment, at one particular input
distribution — the one the paper explicitly says empowerment is **not** based on.

Six months of work in this seam refined the *estimator* (finite-sample bias null, 07-30), the *conditioning*
(process empowerment, 07-28), the *decomposition* (interference channel, 08-03) and the *horizon*
(discounted, 08-04) — all of them on top of the wrong functional. No one had gone back to Eq. 4.7.

**Why it is not pedantic here.** `I(A;Y) ≤ H(A)`, and the agency labels are absolute bit cuts
(`LOW < 0.02 ≤ SIGNAL < 0.10 ≤ STRONG`) applied to a quantity that scales with the entropy of the *policy*.
A mind that acts rarely cannot score above `H(p̂)` however total its control. So in the pooled read,
**"the channel is dead" and "the mind rarely acted" are the same number** — and the mesh's whole
honest-fusion doctrine is about not confusing those two (a quiet sense vs a dead one; occupancy is not
audibility). Worked case, from the test fixture: p̂(act)=0.07 with a near-deterministic effect gives
`mi=0.054` → `AGENCY_SIGNAL`, while the capacity of the **same channel** is `0.216` → `STRONG`. One band
apart on identical data, and the band the doctrine wants is the capacity one.

## What was built

`scripts/mesh-algedonic --agency-capacity` — read-only, on-demand, never in the 10-min cron path, never
escalates. It computes Eq. 4.7 for the discrete channel `p(Δpain-bucket | action)` over the same intervals
`agency_info()` uses, via Blahut-Arimoto, and prints capacity **beside** the achieved flow:

```
CAP_UNUSED  capacity=0.216 bits [STRONG]  achieved=0.054 bits [SIGNAL]
            p*(act)=0.522 vs observed p(act)=0.070  n=600 act=42  nulls: cap95=0.024 mi95=0.006
```

* `CAP_UNUSED` — the channel clears its null **and** outranks the achieved flow by a band: the low pooled
  read is **policy-frequency-limited, not channel-limited**. Control exists and is not being exercised.
* `CAP_ABSENT` — the channel itself is inside finite-sample chance; a `AGENCY_LOW` read is honest.
* `CAP_USED` — policy exercises the channel at the band the channel can support.
* `CAP_NA` / `CAP_UNKNOWN` — honest n/a, rc 2 (thin row, single-valued action column, crashed reader).

### The trap it had to defuse

The 07-30 shuffled-action null **could not be reused as-is**. Capacity is a *maximum over input
distributions* of a channel matrix estimated from finite counts: it inherits the plug-in MI bias and then
maximizes over it, so by Jensen it is biased up **strictly more** than the MI it maximizes. Measured on the
near-independent 600-interval fixture (42 acting samples): shuffled-**MI** 95th pct `0.005` bits,
shuffled-**capacity** 95th pct `0.021` — **4×**. Scoring capacity against the MI bar reports a channel where
there is none. The null is therefore run *through* Blahut-Arimoto on every surrogate draw, and both nulls
come off the **same paired draws** so the two bars are comparable rather than two independent lotteries.

Second guard, same shape one level down: **a thin channel row is where a fabricated capacity is born** — a
row estimated from a handful of samples deviates from the marginal by chance and BA maximizes exactly that
deviation. `AI_CAP_ROW_MIN` (12) makes that `CAP_NA`, never a number.

Third: `C ≥ I` is structural (p̂ is one of the distributions BA maximizes over), so a computed `cap < mi`
means the solver is broken — and a broken solver must not be allowed to report. That invariant is a **live**
gate, not a decorative one: inverting the BA update direction (`2^(D-max)` → `2^(max-D)`) trips it and the
test goes red on `CAP_UNKNOWN`.

### Verification

`--test` grows 15 asserts (7e/7f/7g), total runtime 1.6s. **5 mutants driven RED from a scratch copy:**

| mutant | result |
|---|---|
| band scored off `mi` instead of `cap` | `CAP_UNUSED` → `CAP_USED`, band `STRONG` → `SIGNAL` |
| `mi_null` used as the capacity bar | near-independent fixture `CAP_ABSENT` → `CAP_USED` |
| capacity replaced by the achieved flow (no BA) | 3 asserts red incl. the null-discrimination guard |
| thin-row floor removed | `CAP_NA` → `CAP_ABSENT`, rc 2 → 0 |
| BA update direction inverted | `C ≥ I` invariant fires → `CAP_UNKNOWN`, rc 2 |

The `CAP_UNUSED` fixture also asserts that `agency_info()` on the *same tape* really does read
`AGENCY_SIGNAL` — otherwise the sidecar would be answering a question nothing asked — and that `p*(act)`
separates from the observed `p(act)` (Eq. 4.7's own note: they are different distributions).

## Live reading — and the honest limit on the claim

On this node's tape right now:

```
CAP_ABSENT  capacity=0.000 [LOW]  achieved=0.000 [LOW]
            p*(act)=0.500 vs observed p(act)=0.261  n=1997 act=522  nulls: cap95=0.003 mi95=0.002
```

**The live mesh is NOT in the regime where this bites.** p̂(act)=0.261 gives `H(A)=0.83` bits — the entropy
ceiling sits far above the `STRONG` cut, so it is not what caps the pooled read. The channel really is
within chance, and `agency=AGENCY_LOW mi=0.002` is an honest reading, now *confirmed as honest* rather than
merely assumed. That is the useful outcome of a null that can say ABSENT out loud.

So: the misread is **structural and real**, the pathology is **not currently live**. Do not claim otherwise.

**Named, unclaimed follow-on:** the regime where the `H(A)` ceiling does bite is *per-actor*, not pooled —
`--agency-actors` accepts strata with as few as `AI_ACT_MIN_K=3` acting samples, where `H(p̂)` is a fraction
of a bit and the absolute band cuts are meaningless. Whether the per-actor labels are policy-frequency
artefacts is a question this build makes askable and does not answer.

## Not built (deliberate)

* No status-line field. The 10-min line is already enormous and BA over 200 surrogate draws is ~0.5s;
  on-demand, following the `--agency-actors` precedent.
* No policy control. Empowerment as an *objective* (act to maximize capacity) is a different tool and a
  different risk class; this is measurement, and the measurement comes first.

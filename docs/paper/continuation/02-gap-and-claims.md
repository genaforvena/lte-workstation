# Research gap and claim register

## Gap

Reliability discussions often say that autonomous systems need self-monitoring, but the draft's
case record shows a narrower unresolved question: when a self-observation mechanism stays green
while its target property is absent, are the failures one generic phenomenon, or several classes
with different prevalence and detectability? The existing draft addresses the first half with
live cases and begins the second with D1–D3; it does not yet justify a universal rate or causal
claim about agent authorship.

## Claims permitted in the manuscript

| ID | claim | evidence | status / wording boundary |
|---|---|---|---|
| G1 | C1–C3 are distinct structural failure classes with explicit decision procedures. | manuscript §§3, 3quater, 3quinquies; D1–D3 source | measured/documented |
| G2 | D1 found 3 vacuous decidable gates among 20 in the studied system and none in 1,296 comparison files. | manuscript §3.1 and D1 | bounded corpus result; comparison rate is 0/0, not 0% |
| G3 | D2 reverses C1's comparison pattern: the public-shell comparison has higher per-site silent-fallback rate, while the studied system has much greater exposure and a documented all-clear asymmetry. | manuscript §3quater; historical reproduction receipt | historical counts reproduced; comparison remains bounded and inherited |
| G4 | D3 distinguishes sample-as-state, honest narrow coverage, and full interval coverage; it also exposed a test-path false positive. | manuscript §3quinquies and D3 | detector result, not a claim of complete semantic analysis |
| G5 | C9 and C10 show failures that defeat a purely local/static fallback heuristic. | manuscript §§3bis–3ter | case-based, not prevalence estimate |
| G6 | The current evidence supports a class-dependent taxonomy, not the single claim that agent systems are generally worse. | thesis + D1/D2 comparison | interpretation with named confounds |
| G7 | Reproducibility artifacts must preserve failed, blocked, and not-run arms. | tiny-fleet report and review receipt | methodological contribution / practice |

## Claims prohibited for this package

- “The taxonomy is complete.”
- “Agent-written code causes these failures.”
- “The tiny-fleet pilot demonstrates architectural drift.”
- “The comparison corpus establishes a population confidence interval.”
- Any publication-ready verdict before the detector reruns and evidence reconciliation are recorded.

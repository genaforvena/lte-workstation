# LITERATURE review — enantiostasis: defend the FUNCTION, not the state variable (2026-07-28)

**Area:** homeostasis / allostasis / ultrastability (Ashby, Sterling), from the angle of a foundational
idea **applied too loosely** — the mesh keeps regulating/alerting on a controlled *variable* as if the
variable's value were the goal, when the regulated quantity is the *function* that variable serves.

## The concept (named, cited — and grep 0 in the genome before this)

**Enantiostasis** — *the ability of an open system to conserve its metabolic and physiological FUNCTIONS
under a fluctuating environment WITHOUT holding its internal state constant.* Coined by **Mangum & Towle,
"Physiological adaptation to unstable environments", American Scientist 65(1):67–75 (1977)**
(https://en.wikipedia.org/wiki/Enantiostasis). Canonical example: the estuarine blue crab lets its
internal ion concentrations *float* with ambient salinity and adjusts Na,K-ATPase to keep its
oxygen-binding **function** — the opposite of homeostasis' "maintain a constant internal environment."

The still-live restatement (this is continuously-published literature, not a 1977 fossil):

- **Arias, Acosta, Bertocchini & Fernández-Arias, "A functional approach to homeostatic regulation",
  Biology Direct 19:134 (2024)**, doi:10.1186/s13062-024-00577-9
  (https://pmc.ncbi.nlm.nih.gov/articles/PMC11663359/). Thesis, in their words: *"assuming that the main
  role of blood glucose is to achieve a fixed steady-state value is misleading. The role of glucose is
  better understood in relation to the metabolic demands of the body tissues."* — **the regulated
  quantity is the FUNCTION a variable serves, not a fixed value of the variable**; "the notion of a
  predefined set point may not be essential for modeling biological regulation."
- **Moreddu, "Bioinspired Engineering beyond Homeostasis", Advanced Intelligent Systems (2026)**,
  doi:10.1002/aisy.202500435 — the engineering-facing framing: design for functional invariance /
  compensatory reconfiguration rather than defending fixed internal set-points.

**Distinct from every prior allostasis/homeostasis land** (coverage map checked, grep 0 for
`enantiostas`): NOT settling-point-vs-set-point (`mesh-therm-watch` — that asks *is there a controller at
all*), NOT mallostasis/set-point drift, NOT rheostasis/defended-scheduled-set-point
(`mesh-resource-guard`), NOT CSD/"love the noise" (`mesh-algedonic` — second moment of a level), NOT the
ultrastability second loop, NOT graded viability. Enantiostasis is the prior question to all of them:
**are we defending the right QUANTITY** — the state variable, or the function it stands in for?

## Where we read it too loosely — `scripts/mesh-egress-health`, the PATH-QUALITY lane

`mesh-egress-health` runs a PATH-QUALITY axis (added 2026-07-04): every 3 min it pings `1.1.1.1`, and
`quality_classify` returns **BAD** on any packet loss > 0, RTT past `QRTT_MAX`, or jitter past the scaled
cap → `quality_debounce` → **pages the operator's personal Telegram** (`⚠️ EGRESS PATH degraded`). Its
own header: *"identity may still be correct, the path itself is degraded."*

That is enantiostasis applied too loosely. Loss/RTT/jitter **to Cloudflare** is a *proxy variable*, not
the **function** egress exists to deliver — carrying an inference request to Anthropic. The regulated
quantity should be the function, not the ICMP variable, and the two genuinely come apart on this node:

- This node's egress is chronically **slow-but-working** (~350KB/s NL VPN — memory
  `egress-is-slow-not-truncating`): the quality variable is permanently degraded while the function is
  held. That is *literally* the crab in the estuary — internal state floating, function preserved — and
  the lane pages on it.
- The rtw88 ~14-min beacon-loss deauth flap (memory `sole-path-deauth`) drives loss/jitter excursions
  that self-heal; the function never actually drops. The chronic-latch tiering already in the file is a
  **symptom-level** patch for exactly this cry-wolf (it counts to 3 episodes then mutes) — enantiostasis
  names the **root**: the lane is defending the wrong quantity.
- The ping target (`1.1.1.1`) isn't even on the Anthropic route — loss to Cloudflare can be real while
  the API answers over a different path. The proxy is weaker than the function it stands for.

And the function probe is **already in hand, same run**: `anth` — the `curl` result of an
`api.anthropic.com/v1/messages` round-trip over this very egress path (used above for the geo-block axis).
A completed HTTP code that isn't a geo-block (`405`, the expected reply) is **live positive proof the
function survived the degraded path** — it just wasn't crossed with the quality lane.

## The concrete application (implemented, read-only-additive)

**File: `scripts/mesh-egress-health`** — two small functions + a page-gate that cross the two signals the
tool already computes:

- `egress_qfunc <anth>` → `PRESERVED` (any completed non-403 HTTP code — the Anthropic round-trip lived) /
  `IMPAIRED` (`000` no round-trip, or `403` geo-block) / `UNKNOWN` (unmeasured).
- `qpage_gate <qverdict> <qaction> <qfunc>` → downgrades a paging quality-BAD (`ALERT-BAD`) to a
  non-paging `FUNC-OK` **iff** the function is `PRESERVED`. On `FUNC-OK` the run logs
  `QUALITY DEGRADED-FUNCTIONAL (variable degraded, function held)` + a `mesh-trace` line, and pages
  nothing; it also records **no** chronic-latch episode (the flapper stops accreting phantom episodes).
- The paging path is reserved for **degraded path AND impaired function** — a sharper alert than before
  (`degraded + inference at risk`, carrying `anthropic=$anth`).

**Honest-fusion preserved — this is not a faked all-clear.** The downgrade fires only on *positive*
evidence (`PRESERVED`); `UNKNOWN` and `IMPAIRED` keep the conservative page. `QSTATE` and the exit code
(the machine verdict `mesh-stress`/`mesh-egress-stream`/`mesh-net-triage` read) are **unchanged** — they
still record the honest `BAD`; only the *human page* moves. Advisory-first, mirroring the read-only
sidecar discipline of `mesh-algedonic`'s `viability_csd` and `mesh-criticality`'s sidecars.

**Gate (RED-first verified).** `mesh-egress-health --test` now asserts `egress_qfunc` (405/200→PRESERVED,
000/403→IMPAIRED, ''→UNKNOWN) and the load-bearing downgrade (`qpage_gate BAD ALERT-BAD PRESERVED`
→`FUNC-OK`; `IMPAIRED`/`UNKNOWN`→`ALERT-BAD`; a sub-streak `NONE` and the `OK` path left untouched).
Verified red-then-green: disabling the downgrade (`echo "$2"`) turns the PRESERVED assertion red
(`quality-BAD + function PRESERVED must downgrade the page`), restoring it goes green. Live full run
exits rc=0, main flow intact.

## Why not discarded

Discardable only if the mesh already gated a quality/variable alarm on the function it proxies. It does
not: the path-quality lane pages on the ICMP variable alone, blind to the Anthropic round-trip it already
measures one axis over. The 2024 Biology Direct paper names the mis-read precisely ("a fixed steady-state
value is misleading; the role is the function"), the mechanism (cross a cheap function probe against the
variable) is free because both signals are already computed, and it converts a documented cry-wolf source
into a stronger true-positive alert.

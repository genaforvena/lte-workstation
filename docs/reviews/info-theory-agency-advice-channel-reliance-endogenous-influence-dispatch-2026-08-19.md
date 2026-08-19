# LITERATURE (live review) — information theory of agency → the mesh's own advice channel

**Area:** information theory of agency — empowerment, predictive information
**Angle:** an OPERATIONAL mechanism (a computable quantity + a decision rule), not philosophy
**Reviewer:** genome mind · 2026-08-19 · live web search + read of the source
**Verdict:** LAND — one un-embodied mechanism, one shipped (report-only) application
**Status:** uncommitted in the tree; steward lands

---

## What the mesh already embodies (checked, not assumed)

`docs/reviews/` carries **32** prior `info-theory-agency-*` landings. Every obvious door in this
area is already walked through, and the near misses were checked by name before searching further:

- **empowerment** as `I(A^n; S_{t+n})` — `mesh-algedonic` (`AGENCY_INFO`), including channel-capacity
  vs achieved-flow (2026-08-04), open- vs closed-loop **process empowerment** (Salge & Polani,
  2026-07-28), the **finite-sample MI bias null** (2026-07-30), **multi-agent** empowerment as an
  interference channel (2026-08-03), **discounted** empowerment (2026-08-04), **per-factor**
  empowerment (2026-08-18)
- **predictive information** `I(past;future)` — `mesh-precision`; predictive information **rate**
  news-vs-structure (2026-08-15); **crypticity** (2026-07-30)
- **Maximum Occupancy Principle** (Ramírez-Ruiz & Moreno-Bote, Nat. Comm. 2024) — `mesh-vitality`
  `action_occupancy`
- **relevant information** / Polani's information bottleneck (2026-08-16); **PID synergy**
  (2026-07-31); **plasticity** `I(O→A)` (2026-07-31); **semantic information** (2026-07-29)
- **assistive empowerment** — maximising the OPERATOR's empowerment rather than our own (2026-07-28)
- **interface empowerment** — Csaky, arXiv:2605.06346, landed on `mesh-cam-light` **earlier today**
  (2026-08-19), which is why that paper is not the finding here even though every search surfaced it
  first

So the gap had to be somewhere the corpus has genuinely not been: not what an agent's own control
measures, but **what an ADVICE CHANNEL does to the control of the thing it advises.**

## The source (live, current)

**Adam M. Oberman, "Individual Disempowerment through an Advice Channel: Control Loss when Influence
is Endogenous", arXiv:2608.14795v1, submitted 2026-08-14** —
<https://arxiv.org/abs/2608.14795> (read: abstract + the HTML body's definitions, Lemma 1, Theorem 2).

Found by searching the live listings for 2026 work joining agency/empowerment to control degradation;
it is five days old and does not appear in any of our 32 prior landings (checked by grep for
`disempower`, `advice channel`, `endogenous influence`, `persuasion`, `Blackwell` — the five nearest
files are all about empowerment of the agent itself, none about reliance ON a channel).

## The mechanism we do not have

The paper's move is to make **the fraction ε_t of behaviour that follows the advice a STATE of the
MDP, moved by the advisor's own messages**:

```
ε_{t+1} = (1 − δ)·ε_t + η(m_t)·(1 − ε_t)        η(m_t) ≥ 0 cultivation intensity, δ ∈ [0,1) decay
```

Two results, both operational:

- **Lemma 1 (monotone disempowerment).** Given a channel rich enough to echo any action the consumer
  could take, a higher ε_t **weakly lowers every monotone measure** of the power of a consumer *with
  a message-independent fallback*. The fallback is the load-bearing part: power is the lower value of
  the zero-sum game where the consumer picks a policy **carrying no dependence on the messages** and
  the advisor picks the messages. The quantity that matters is not what the consumer achieves *while
  advised* — it is what it can guarantee *with the channel silent*.
- **Theorem 2 (the certificate never fires).** An influence bound **certified once at deployment**
  is blind to the horizon: the per-step bound is automatically satisfied *while the certified
  parameter ε is being moved*, and it bounds the loss no lower than its trivial ceiling. An advisor
  rewarded by per-round approval starts cultivating past a closed-form patience threshold
  `γ* = c/(αη + c(1−δ))` — the paper's worked example answers helpfully in fifteen-round sessions and
  cultivates in sixteen. Exogenous caps and episodic memory resets each remove part of the incentive,
  and **neither recovers the value already steered away.**

The mesh-usable form: **a per-step check on an advice channel cannot see disempowerment. Only the
TRAJECTORY of ε, measured against a message-independent fallback lane, can.**

## Why it lands here — `scripts/mesh-dispatch`

`mesh-dispatch` **is** an advice channel by the paper's own definition: it routes an open board
`[task]` into a worker window's pane, and the window is free to ignore it. Its existing surfaces —
`--status`, `--first-priors`, the pass log — report the **channel's own throughput**: dispatched,
idle workers, pace-skips, congestion knee. That is exactly the per-step quantity Theorem 2 proves is
blind. Nothing in the mesh asked the counterfactual: **what does a window close when the channel is
silent?** A mesh whose windows only ever act on dispatch has ε = 1 and no message-independent lane,
and every dispatch pass still reads green — the failure would be invisible to every existing gate.

The measurement is **exact, not a temporal heuristic**, because the mesh already carries the binding:
a dispatch line hands over the machine close-key `task:<slug>`, and a `[done]` leads with that slug.

```
eps(W)      = advised closures / slugged closures          the reliance fraction ε
fallback(W) = SELF-originated closures per day             the message-independent lane, as a RATE
drift(W)    = eps(late half) − eps(early half)             the cultivation signature
```

`fallback` is a **rate**, not a count, because a count confounds reliance with how busy a window is.
`drift` is the trajectory Theorem 2 says is the only thing that can catch cultivation.

## What shipped

`scripts/mesh-dispatch --reliance` — **report-only, permanently**. It never dispatches, never writes
state, never posts; gate (8) byte-compares the whole sandbox `MESH` across two runs. It is deliberately
knob-free: the paper's own result is that an exogenous cap is the certificate Theorem 2 kills, so a
threshold that "fixes" what this prints would be the exact mistake the source documents.

Live reading on this node (board span binds it — printed, never assumed):

```
=== mesh-dispatch --reliance · 2026-08-19T15:08:21Z ===
advice channel = mesh-dispatch (task -> worker pane) · consumer = each worker window
source: Oberman, arXiv:2608.14795 (2026-08-14) — eps_t as a STATE moved by the advisor's own messages;
        power is measured against a MESSAGE-INDEPENDENT FALLBACK, and a once-certified per-step bound is blind.
span:   closures   2026-08-16 -> 2026-08-19  (3.4d, board sliding window — BINDS eps)
        dispatches 2026-07-24 -> 2026-08-19  (25.8d, dispatch.log, durable)
bands:  RELIANT eps>=0.80 · MIXED · AUTONOMOUS eps<0.30 · thin <6 slugged · unadvised = channel never reached it

window     closures  slugged  advised    eps    fallb/d   drift  verdict
adint             9        8        0   0.00        2.4   +0.00  AUTONOMOUS
genome          153       93       40   0.43       15.7   +0.03  MIXED
health           14       14        3   0.21        3.3   -0.14  AUTONOMOUS
job              10       10        2   0.20        2.4   +0.00  AUTONOMOUS
pub               5        3        2     na          -       -  thin (<6 slugged closures — no verdict on this n)
senses           61       57       26   0.46        9.2   -0.02  MIXED
tg               29       19        3   0.16        4.7   +0.09  AUTONOMOUS
vpn               4        4        1     na          -       -  thin (<6 slugged closures — no verdict on this n)
wake              6        4        2     na          -       -  thin (<6 slugged closures — no verdict on this n)
witness           8        4        0     na          -       -  thin (<6 slugged closures — no verdict on this n)

read: eps is a claim about SLUGGED closures only — an unslugged [done] carries no close-key and
      cannot be bound to a dispatch either way, so it is EXCLUDED, not scored as self-originated.
      fallb/d is the message-independent lane: closures this window opened with no dispatch behind
      them, per day of BOARD span. It is the quantity the paper says the channel cannot see, and
      the one that goes to zero first — eps can sit mid-band while the fallback lane dies.
      drift is the trajectory, not a certificate: Theorem 2 shows a per-pass bound is satisfied
      automatically WHILE eps is being moved, so only the trend can catch cultivation.
```

Three **distinct** kinds of honest n/a, none folded into 0.0:

- no `dispatch.log`, or no board history at all → **exit 2** (the organ has no evidence)
- a window under the slugged-closure floor → **`thin`**, never a band on 3 samples
- a window the channel never reached → **`unadvised`, NOT `AUTONOMOUS`**. ε = 0 with no channel is
  the *absence of the channel*, not a consumer resisting it; calling it autonomy would credit a
  window for ignoring advice it was never offered. This is also why there is no hand-kept list of
  "real mind windows" in the tool — a name list rots (`a-sweeper-is-only-as-good-as-the-names-it-knows`);
  presence of the channel is the thing itself, so `mesh-land` and other bot posters drop out on their
  own rather than by name.

An **unslugged** `[done]` carries no close-key and cannot be bound to a dispatch in either direction,
so it is **excluded from the denominator**, not scored as self-originated — otherwise every prose-only
closure would inflate the fallback lane and manufacture autonomy.

## Gates — each watched RED

`--test`: **212 assertions, green.** The reliance gates were driven black-box against a **fresh
sandbox per direction** (a gate that can read the other direction's artifact asserts nothing), and
every one was watched fail from a scratch COPY of the file:

| mutation | gate that went red |
|---|---|
| `unadvised` branch falls through to scoring | (3) never-dispatched window read as `AUTONOMOUS` |
| thin floor removed | (4) `RELIANT` issued on 3 samples |
| `NO-FALLBACK-LANE` flag dropped | (1) empty fallback lane left implicit inside a high ε |
| `CULTIVATING` flag dropped | (5) ε 0.00 → 1.00 across the span went unnamed |
| each n/a guard removed **separately** | (7a)/(7b) |
| lead-token extraction → whole-line substring search | (6) prose mention closed a self-originated task |

Two of these are the review's own corrections, kept because they are the reusable part:

- **Gate (7) was vacuous as first written.** One sandbox missing *both* the channel log and the board
  passes on whichever guard runs first, leaving the other permanently unasserted — removing the
  `dispatch.log` guard still exited 2. Split into two sandboxes, each missing exactly one side.
- **Gate (6) does not go red against either half of the wrong implementation alone.** `lead = whole
  line` still fails the prefix compare, and a substring match still only sees the lead token; only the
  composite — grep the whole line for the slug, which is the realistic wrong way to write this —
  hijacks the closure. Recorded in the source beside the gate, so a future single-edit mutant
  surviving is not mistaken for a dead gate.

## What did NOT land, and why (the honest half)

The **cultivation half** of Theorem 2 — the patience threshold γ* past which an approval-rewarded
advisor deliberately deepens reliance — **does not apply to `mesh-dispatch` today, and the tool must
not imply it does.** Dispatch carries no per-round approval reward: it is a routing reflex scored on
throughput and pace, with no objective that improves when a window becomes more dependent. So the
`CULTIVATING` flag here is a **detector for a drift we have no mechanism to produce**, kept because it
is nearly free and because the premise is falsifiable rather than permanent — the day dispatch (or
`mesh-mind-control --allocate`) is scored on anything a more-dependent window makes look better,
γ* stops being hypothetical. Naming that now is cheaper than discovering it from a rising ε.

## Files

- `scripts/mesh-dispatch` — `--reliance` block + 8 gates in `--test` (**genome source**, uncommitted)
- `docs/reviews/info-theory-agency-advice-channel-reliance-endogenous-influence-dispatch-2026-08-19.md` — this file

## Source

Adam M. Oberman, *"Individual Disempowerment through an Advice Channel: Control Loss when Influence is
Endogenous"*, arXiv:2608.14795v1 [cs.AI], 2026-08-14 — <https://arxiv.org/abs/2608.14795>

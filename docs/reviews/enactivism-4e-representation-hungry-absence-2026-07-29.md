# LITERATURE review — enactivism/4E from the CRITIQUE angle: the representation-hungry / scaling-up problem, and the mesh's missing "non-event" sense (2026-07-29)

**Area:** enactivism / 4E cognition (embodied, embedded, enacted, extended).
**Angle:** a known **failure mode** of the area — not its metric (that was
`enactivism-4e-participatory-coupling-metric-2026-07-27.md`), but the sharpest standing *objection*:
enactive/embodied accounts handle the **present and coupled** case and stall on the **absent,
counterfactual, and abstract** case. This is the **"scaling-up problem"** / **"representation-hungry
problems"** critique, and it is still live in 2025–2026.

## The critique (live sources)

The **scaling-up problem** is the challenge of explaining how cognition moves from online agent–environment
dynamics to dealing "with **absent or merely possible objects, with counterfactual states of affairs, and
with general or abstract concepts.**" Embodied/enactive accounts are strongest exactly where cognition is
*coupled* to what is perceptually present, and weakest where it must run **offline and decoupled** from
immediate sensorimotor engagement:

- **absent referents** — thinking about what is not perceptually present;
- **counterfactual reasoning** — the hypothetical, the false, the not-yet;
- **abstraction / symbolic manipulation** — "for thinking, planning, remembering."

Read live in: *The experiential basis of concepts: integrating embodied and enactive accounts*,
Front. Psychol. **16:1710102 (2025)**
(https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1710102/full), which frames
the scaling-up problem and attributes the terminology to **Kiverstein & Rietveld (2021)**. The canonical
origin of the underlying objection is **Clark & Toribio (1994), "Doing without representing?", *Synthese*
101(3):401–431**, which coined **"representation-hungry" problems** — tasks whose solution *requires* an
internal stand-in for what is absent/abstract, precisely the tasks a purely coupled, reactive system cannot
do. (The 2025 paper names the problem and cites Kiverstein & Rietveld; the Clark & Toribio attribution is
the canonical background the live paper points back to, not quoted in it.)

That the objection is still contested — not settled — is confirmed by the 2026 survey *Critical 4E
Cognitive Science* (Liao, *Philosophy Compass*, 2026,
https://compass.onlinelibrary.wiley.com/doi/10.1111/phc3.70075) and *What is 4E cognitive science?*
(*Phenom. Cogn. Sci.*, 2025, https://link.springer.com/article/10.1007/s11097-025-10055-w), both paywalled
at fetch. The field's own answer to scaling-up is to reach for **decoupled representations of the absent**
(schemas, metaphor, language) — i.e. to admit the one thing pure coupling lacks.

## What the mesh already embodies (the coupled, present-tense case — well-trodden)

The mesh's sensorium is *deliberately* enactive: **"Perception is re-observed live, never stored (decays on
reboot)"** (CLAUDE.md), and the honest-fusion rule renders an unreachable input UNKNOWN, never a faked
all-clear. Its situational senses are all **online / coupled**:

- `scripts/mesh-arrivals` — emits `[arrived]`/`[left]` for a **named device**, with a debounce quorum. But
  `[left]` is an **observed** present→absent transition — the mesh *watched* it go.
- `scripts/mesh-perimeter` — ALERT on a **present** stranger / a new LAN device / a flipped gateway MAC
  (the "index vs icon" landing). All of it is *something that IS there now*.
- `scripts/mesh-rhythm` — **learns the decoupled model**: "Commuter tends to appear around 09:00" via a
  Rayleigh-tested onset-angle. This is the mesh's one genuine *representation of the expected* — but it is
  used only **descriptively** (emit the schedule as an idea/finding).

Every one of these fires on **presence**. None fires on **absence-of-the-expected**.

## The concept we do NOT embody: the NON-EVENT (representation-hungry absence)

The paradigm representation-hungry inference is **the dog that didn't bark** (Conan Doyle, *Silver Blaze*):
to notice that *nothing happened where something was expected*, you must hold a **decoupled model of the
expected** and read it **in the negative** — live coupled perception, by construction, cannot deliver a
non-event (there is no stimulus to couple to). This is exactly the case enactivism is charged with failing,
and exactly the case the mesh currently cannot report:

> **The mesh detects the present-and-unusual (stranger, new device, observed departure). It cannot detect
> the expected-and-absent (the phone that appears at 18:40 every day and did NOT appear today).**

`mesh-rhythm` already builds the representation that would make this possible — the confident, learned
per-device onset schedule — and then throws away its inverse.

## Concrete proposal (name the file): an absence lane in `scripts/mesh-rhythm`

Add an **inverse / no-show lane** to `scripts/mesh-rhythm` that reads its *own* learned schedule model in
the negative:

- For each device with a **Rayleigh-significant** onset schedule (already computed — the current confident
  findings), compute the expected window `[μ − k·σ, μ + k·σ]` around its learned onset angle.
- When **today's clock has passed the upper edge** of that window **and no onset was observed** for that
  device today, emit a **`[rhythm-absence]`** NOTICE (a *non-event*): "*Commuter usually appears ~09:00;
  09:00±40m has passed with no appearance today.*"
- Gate hard against the two failure shapes this class always hits: (a) the **scanner-cadence null** — do
  not fire if the vantage that would have *seen* the device is itself down/absent (that is honest
  blindness, not a real no-show — cf. `[[reflex-stale-can-be-honest-blindness]]`, and the clock-lean trap
  `[[a-label-that-embeds-the-clock-correlates-with-the-sun]]`); (b) **first-window suppression** so a
  freshly-learned schedule cannot cry absence before it has a real baseline.
- Route the NOTICE into `scripts/mesh-situation` as an **EXPECTED-ABSENCE** context line (the natural home:
  it already folds PHYSICAL "who's here" — the missing dual is "who *should* be here and isn't").

The `--test` must **see the gate fail**: feed a fixture where the expected onset window has passed with the
device absent → assert `[rhythm-absence]` fires; then feed the same window with the vantage down → assert it
does **NOT** fire (honest-blindness path). A no-show lane whose null you have not watched hold is the
`|| echo <default>` trap wearing a new coat.

This is the minimal way to give the mesh the one thing the scaling-up critique says pure coupling lacks: a
**decoupled model of the expected, read in the negative** — a sense for what is missing, not just for what
is there.

## Coverage note

- Sibling landings, do not re-land: participatory sense-making / interaction autonomy / CRQA
  (`enactivism-4e-participatory-coupling-metric-2026-07-27.md`); the normativity/adaptivity gap (HELD, in
  `scripts/mesh-fitness` header); index-vs-icon present-stranger ALERT (`biosemiotics-…-perimeter-stranger`).
- Adjacent still-open (per memory coverage maps): biosemiotic **anticipation** (Rosen) — the *predictive*
  cousin of this *absence* landing; if built, the absence lane is its first concrete instance.

**Status:** review + concrete proposal (file named: `scripts/mesh-rhythm`, feeding `scripts/mesh-situation`).
No tool edited — implementation left as a discrete, testable follow-up so the no-show null can be built with
its gate seen red-then-green, not bolted on inside a review.

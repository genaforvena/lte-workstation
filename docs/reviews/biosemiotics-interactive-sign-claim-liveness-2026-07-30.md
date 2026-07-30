# Live-literature review — biosemiotics: the interactive sign — a claim's life is its interaction cycle, not its age (`mesh-promises`)

Date: 2026-07-30 · lane: genome (idea-queue LITERATURE task) · status: proposal, uncommitted

## Area & angle

Biosemiotics — sign and meaning in living systems — approached, as the task asks, through a
**recent result open in the journal right now** (2025), not a settled classic:

- Arash Ghazvineh, **"Interactive Signs and Digital Umwelts: Rethinking Meaning in the Age of
  Platfospheres"**, *Biosemiotics* **18: 495–515 (2025)**
  (link.springer.com/article/10.1007/s12304-025-09607-z; abstract via PhilPapers GHAISA-4).
- The new move: classical biosemiotics reads a sign as an **interpretive entity** — something a
  subject *reads* to update its Umwelt. Ghazvineh argues that in digital, participatory media a sign
  is also an **interactive site**: meaning arises from **recursive cycles of interpretation AND
  action** around the sign, and each cycle reshapes the interpreter's internal Umwelt. He calls such
  ecosystems **platfospheres**. Consequence he draws: digital meaning becomes **fragmented,
  inferentially complex, and time-sensitive** — the meaning of an interactive sign lives only while
  its interaction cycle is live; a sign nobody acts on is a **dead site**, not a stored token.
- Builds explicitly on the two biosemiotic primitives we already carry (Umwelt, scaffolding), so it
  sits adjacent to prior landings but names something none of them did: **the sign as a place where
  the interpreter acts, whose life is measured by the density of that action.**

Distinct from our five prior biosemiotics landings (functional-cycle return-leg, information-balance,
index-vs-icon, code-duality, code-vs-interpretant): each of those treats a sign as something
**read** — a mode of reference, a fidelity, a sufficiency-of-code. This one is about a sign as
something **acted-upon in a loop** — and the operational property that falls out is a **liveness**
axis orthogonal to everything we measure today.

## The mesh has a live platfosphere and reads it as a token-store

`~/.mesh/chat.log` — the board — is a textbook platfosphere: minds **read** markers
(`[task]`/`[taking]`/`[verify]`/`[done]`) and **write** them, and every write reshapes what other
minds perceive and how they act. A `[taking]` is an **interactive sign** in Ghazvineh's exact sense:
it is an interpretive entity (a claim opened) *and* an interactive site (the thing the owner is
supposed to keep acting around until it settles).

**`scripts/mesh-promises` is the board's one accountant, and it reads interactive signs as static
tokens.** Its leak decision (verified in-source) is purely **age**:

```
scripts/mesh-promises:505   age_h = (now - o['ts']).total_seconds() / 3600.0
scripts/mesh-promises:506   thr   = incid_h if o['incident'] else leak_h
scripts/mesh-promises:510   leaked = age_h > thr
```

An open promise leaks iff it is **older than a fixed threshold** (24h task / 6h incident / 12h
`[verify]`). Nothing in the tool asks whether the sign is a **live interactive site** — whether its
owner has *acted around it at all* since posting. Two claims collapse to the same reading:

- **A** — `[taking]` posted 3h ago; the owner has since peeked, posted two `[fyi]` progress lines
  naming the slug, edited a related file, re-referenced it. A **live** interactive site,
  legitimately still open, genuinely progressing.
- **B** — `[taking]` posted 3h ago; **zero** subsequent board activity from that window, nothing
  mentions the slug again. A **dead** interactive site — abandoned the moment it was posted.

Age cannot tell A from B. Under the current rule both are "fine" until 24h, then both leak together —
so B (already dead at minute 1) is nagged 21h too late, while A (alive at hour 20) will be nagged as
a leak at hour 24 despite being the healthiest claim on the board. This is precisely the failure
Ghazvineh names: **a token-store confuses "young" with "alive" and "old" with "dead," when the real
axis is interaction density.** It is the temporal-sensitivity of the interactive sign, missing.

This is genuinely absent, not a re-description: `grep -niE 'interaction|liveness|density'
scripts/mesh-promises` finds only the tool's OWN state-file mtime touch (line 892–893, the reflex
liveness-touch), never a per-claim interaction measure.

## Proposal (uncommitted, report-only) — an `interaction-density` axis on `mesh-promises`

Add a per-claim **interaction count** during the single board scan the parser already runs, and
surface it **beside** the age/balance — never feeding the leak boolean at first.

- In the ONE parse (the loop that already sees every board line in timestamp order), for each still-open
  promise / hold / `[verify]` keyed `(owner_window, slug)`, count later lines where
  `who == owner_window` **or** whose tokens overlap the claim's `ktoks` (the parser already computes
  `ktoks` per open claim, lines 450 / 479). That count = **interactions since posting**.
- Attach `interactions` and a derived `dead = (interactions == 0 and age_h > DEAD_H)` to each entry in
  `open_list` (line 507) / `claim_open_list` (line 518), with a short `DEAD_H` (~0.5–1h) — a claim
  with **zero** action around it after a grace window is an abandoned site regardless of the 24h SLA.
- **Report-only first** (doctrine: a miscalibrated signal fed into a live detector is a hollow sense).
  Print an extra column and a one-line `dead interactive sites: N` in the summary; do **not** change
  `leaked` yet. Only after the count is watched against the real board does `dead` earn the right to
  shorten a claim's effective SLA (a dead site leaks fast; a live-but-old site is spared).
- Calibrate against the **live board**, never an assumed constant — same discipline as
  [[pooled-corpus-rank-saturates-per-organ]] and [[a-constant-outlives-its-reader]]. The threshold
  for "enough interaction to count as alive" is a claim to be re-derived from the corpus, not pinned.

Why this is the right organ: `mesh-promises` is the mesh's leak detector, and its blind spot is
exactly the interactive-sign blind spot — it audits the **existence** of a promise and its **age**,
never whether the promise is a live site. Adding interaction-density turns a young-but-dead claim
visible **21h sooner** and stops an old-but-progressing claim from being mis-flagged.

## Guard against the obvious way this goes wrong

- **Do not** let a poster keep a dead claim alive by spamming its own slug — count *distinct
  interaction episodes*, and remember a bare `[heartbeat]`/`[idle]` is not action *around a claim*
  (CLAUDE.md: a content-free `[taking]` "ages into a phantom"). Interaction must reference the claim,
  not merely the window's continued breathing — otherwise this rebuilds the very phantom it detects.
- **Report-only until watched.** An interaction-density that silently shortened SLAs before being
  seen against the real board would be [[a-detectors-verdict-is-a-claim-too]] — a new verdict with no
  red-then-green. Land the column; earn the leak-decision later.

## If it does not apply — the honest alternative

It applies. But the narrower *platfosphere* claim (that signs reshape the interpreter's Umwelt
through the action loop) is **already saturated** elsewhere in the mesh — the data-pane doctrine ("a
window's data pane carries what the window is FOR"), self-calibrating ranks, the expectedness
interpretant — so landing *that* half would be a re-landing. The **unembodied** half is strictly the
**liveness-by-interaction-density** measure on board claims, which no tool computes. That is the one
new place.

## Sources

- Arash Ghazvineh, "Interactive Signs and Digital Umwelts: Rethinking Meaning in the Age of
  Platfospheres," *Biosemiotics* 18:495–515 (2025) —
  https://link.springer.com/article/10.1007/s12304-025-09607-z ·
  https://philpapers.org/rec/GHAISA-4
- Context (semiotic scaffolding lineage, still open): Hoffmeyer, "Semiotic Scaffolding of Living
  Systems" (2007); Zhou, "More Constraints, More Freedom," *Biosemiotics* (2023),
  https://link.springer.com/article/10.1007/s12304-023-09548-5
- In-source verification of the age-only leak rule: `scripts/mesh-promises:505–510`.

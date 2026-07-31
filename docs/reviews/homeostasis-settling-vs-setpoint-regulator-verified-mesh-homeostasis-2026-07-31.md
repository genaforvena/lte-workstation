# Homeostasis critique: a stable value is not proof of a live regulator (settling point vs set point)

**Date:** 2026-07-31 · **Mind:** genome@mesh-home · **Area:** homeostasis / allostasis / ultrastability —
from a KNOWN CRITIQUE · **Landed (read-only instrument):** `scripts/mesh-homeostasis`

## The critique (live literature)

Set-point homeostasis models a variable as a **defended target**: an active regulator senses error and
corrects toward it. The standing critique — the **settling-point** model — is that many observed stable
values are not defended at all. A **settling point** is where a variable comes to rest as the equilibrium
of *unregulated opposing flows*: no controller, no target, stable only because nothing is pushing it out
(or because opposing passive drifts cancel). The killer claim: **a settling point and a set point are
indistinguishable from the stable value alone.** You tell them apart only by *perturbing* and seeing
whether the variable **returns** (set point) or **re-settles** wherever the flows now balance (settling
point). A settling point "predicts no regulated level... no corrective activity occurs."

- Canonical statement + the perturbation discriminator: **Speakman JR et al., "Set points, settling
  points and some alternative models," *Disease Models & Mechanisms* 4(6):733–745, 2011**
  (doi 10.1242/dmm.008698).
- **LIVE 2024:** Arias, Acosta, Bertocchini & Fernández-Arias, **"A functional approach to homeostatic
  regulation," *Biology Direct* 2024** (doi 10.1186/s13062-024-00577-9): *"stability itself need not
  indicate active regulation — unregulated systems can reach equilibrium — making the distinction between
  passive stabilization and active homeostatic control fundamental."* The body-weight arm was re-litigated
  again in 2024–25 (*Philosophy of Science*, "Rediscovering Bernard and Cannon..."; F1000 "Recent advances
  in understanding body weight homeostasis").

Found via WebSearch (July 2026) → Speakman PMC3209643, Arias PMC11663359.

## What we already embody (checked against `scripts/` + coverage memory)

- `mesh-therm-watch` landed the settling-point **control reframe** on **one axis**: this node's temperature
  *is* a textbook settling point (heat production × load), so you don't defend a temp boundary — you MOVE
  the settling point by changing a FLOW (admission cap). That is the **actuator** side, thermal only.
- `mesh-homeostasis` measures the **failed-defence** end via Ashby ultrastability: `TRIALS-TO-STABLE-FIELD`
  and `ULTRASTABLE-EXHAUSTED` (fast loop fired K times and the essential variable is *still* breached).

## The gap (the failure mode we did NOT embody)

`mesh-homeostasis` reports **health from the essential variable being ON set-point** (egress integral 0).
But **egress sitting OK is not proof the corrective loop still works.** The loop — `mesh-fix-egress` + the
escalation ladder + `sudo -n` — can have **rotted** (sudo expired, healer reflexes dead, the fixer broken)
while egress stays OK for the mundane reason that *nothing disturbed it*: a **settling point** held by the
router's passive VPN, not a **defended** one. A homeostat you have **never seen correct** is not a verified
homeostat.

This is the exact twin of the mesh's own doctrine — *"a gate you have not seen FAIL is not a gate"* — and
the **inverse** of the liveness-touch trap (*"value held misread as reflex DEAD"* → false-STALE). Here a
value held is misread as reflex **ALIVE**. And it is the **honest counterpart to `ULTRASTABLE-EXHAUSTED`**:
that names "loop fired and FAILED"; this names the other unknown-health end — "loop **never fired / not
proven live**, so its stability is settling, unverified."

## What landed (read-only, `scripts/mesh-homeostasis`)

`regulator_verified()` + `--settling` + a `regulator:` line in `--status`. It applies Speakman's
discriminator **without** the (substrate, HELD) perturbation: it uses the log's already-recorded
**demonstrated corrections** as the proof-of-life the passive stable value cannot give.

- **DEFENDED-VERIFIED** — a `RECOVERED` (drift-and-return, the perturbation test passing) or `FIX-EGRESS
  succeeded` within `REG_VERIFY_WINDOW` (30d). The loop is proven live: a real correction, not just a
  stable value.
- **SETTLING-UNVERIFIED** — on set-point, but no correction ever / last proven past the window. Stability
  is *settling*; the loop's defence is **unproven by observation**. An **epistemic-humility flag, NOT an
  alarm** ("looks fine, but its defence is unproven"), distinct from a genuine breach.
- **REGULATOR-ENGAGED** — currently drifting; the loop is actively correcting (ultrastability covers it).
- **REGULATOR-UNKNOWN** — no log / unparseable timestamp: liveness unobserved (INSUFFICIENT, honest).

**RED-first `--test`:** five distinct verdicts asserted (empty→UNKNOWN, activity-but-no-correction→
SETTLING, recent correction→DEFENDED, aged-out correction→SETTLING, drift→ENGAGED); a mutant that
hardcodes any single verdict fails at least one. Verified: `--test` green; mutant (always
`DEFENDED-VERIFIED`) → `rc=1` (gate caught it).

**Live read on mesh-home:** `SETTLING-UNVERIFIED` — the egress homeostat here has **never** been observed
correcting (log: 0 correction lines; the tool is orphan-ok / rarely run). The instrument truthfully
surfaces that its "health" is settling, not verified defence — exactly the blind spot the critique names.

## Held (not shipped — substrate)

The obvious follow-on — a **periodic SAFE self-test of the corrective path** (deliberately perturb + watch
it return, turning SETTLING-UNVERIFIED into a real verification) — is a **substrate** action (exercising an
egress fix touches routing, the single-writer surface). It stays HELD behind `mesh-dms` + operator gate,
consistent with the tool's existing held actuators (ultrastability reconfiguration, good-regulator directed
fix). **Measurement before the actuator.**

## Coverage note

Settling-point critique now embodied on TWO fronts: control reframe (thermal, `mesh-therm-watch`) and the
**diagnostic** "is the stable value a live regulator?" (`mesh-homeostasis`). Coverage memory updated.

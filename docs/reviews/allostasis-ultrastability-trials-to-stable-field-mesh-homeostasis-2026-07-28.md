# Allostasis / Ultrastability review — trials-to-stable-field + fast-loop-exhausted trigger

**Date:** 2026-07-28 · **Mind:** genome@mesh-home (loop-baton) · **Area:** homeostasis, allostasis &
ultrastability (Ashby, Sterling) — an OPERATIONAL mechanism, not philosophy.

## The live literature read

Searched current sources (WebSearch/WebFetch, 2026-07-28). Two families surfaced:

- **Allostasis = predictive/anticipatory regulation** (Sterling, *Allostasis: A model of predictive
  regulation*, Neurosci. Biobehav. Rev. 2012, PMID 21684297): stability through *change* of setpoint,
  feedforward on predicted disturbance — the control-theory descendant is Model Predictive Control.
- **Ashby's ultrastability** — the operational mechanism I landed on. The clean modern restatement is
  **arXiv:2507.10443, "Associative Memory for Non-Stationary Environments: A Self-Sizing Generalization
  of Hopfield Networks" (2025)**, which fetches cleanly and states Ashby's rule precisely: a **two-loop**
  system — an **inner loop** that adapts parameters in place, and an **outer loop** that fires a discrete
  reorganization **ONLY when an essential variable persistently exits its viability bounds despite the
  inner loop** (i.e. when reactive adaptation has *failed*, not merely engaged). Ashby's own adaptation
  *metric* (Design for a Brain, 1952/1960; the four-unit Homeostat) is **trials-to-stable-field** — the
  COUNT of reconfiguration steps needed to regain viability, orthogonal to how big or how long the error
  was.

## What we do NOT embody (the gap)

`scripts/mesh-homeostasis` is a single-loop I-controller on the egress-IP essential variable: it
integrates error-**seconds** and escalates log→WARN→FIX (`mesh-fix-egress`). Its own HELD literature
block (lines 41-75) already names the gap: when the fix FAILS the essential variable stays breached and
"the controller simply RE-FIRES the identical correction next cycle — **forever**." There was **no count
of reconfiguration TRIALS**, and **nothing marked the moment the fast loop had exhausted** — the exact
Ashby precondition for the outer (slow) loop. The integral measures error-magnitude; it never measured
adaptation-as-reconfiguration-count.

The **actuator** (randomly/directedly reconfiguring the egress regulator) is correctly HELD — egress is
the mesh's single-writer substrate (CLAUDE.md), and a blind step-change could sever the control plane.
But the **measurement half was absent and is safe**, and "measurement before the actuator" is this
codebase's own doctrine.

## Landed (instrument-first, read-only — `scripts/mesh-homeostasis`)

- The I-controller now carries a **3rd state field = fix-TRIALS** per breach episode (a pre-ultrastability
  2-field integral file reads as `trials=0` — backward-compatible).
- On recovery it logs **`TRIALS-TO-STABLE-FIELD=N`** — Ashby's adaptation metric (reconfiguration count),
  beside the existing error-seconds peak.
- After **`ULTRA_TRIALS` (default 3)** identical fixes with egress **still DRIFT**, it emits a read-only
  **`ULTRASTABLE: fast loop exhausted … reorganization indicated`** trigger (log + one loud board post,
  fired ONCE per episode) — the "the fast loop has failed" signal the HELD actuator would consume. No
  substrate action; the reconfiguration actuator stays HELD.
- `show_status` reports fix-trials; `--reset` writes the 3-field clean state.

**Gate (RED-first, verified red-then-green):** a fresh episode is driven past the fix threshold three
times; the gate asserts (1) NO `ULTRASTABLE` before trial 3 (RED half — the trigger must not cry wolf
while the fast loop is still trying), (2) the trigger fires exactly at `ULTRA_TRIALS` and only once,
(3) the fix-trial is counted, (4) recovery reports `TRIALS-TO-STABLE-FIELD=3` and resets. Each half was
broken independently and watched go RED. The gate also stubs `sudo`/`mesh-fix-egress` so driving
escalation never touches real egress (this node has NOPASSWD sudo — a live substrate action in a `--test`
would otherwise fire).

## Cite

- arXiv:2507.10443 (2025) — Ashby ultrastability two-loop restatement + reorganize-on-persistent-breach.
- Sterling, PMID 21684297 (2012) — allostasis as predictive regulation (the anticipatory-setpoint family,
  not landed here — deferred as the harder, actuator-side move).
- W. R. Ashby, *Design for a Brain* (1952/1960) — trials-to-stable-field as the adaptation metric.

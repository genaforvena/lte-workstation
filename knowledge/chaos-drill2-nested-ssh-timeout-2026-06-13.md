# Chaos Drill 2 fails on a nested-SSH timeout, not a "beat precondition" — 2026-06-13

**Status:** verified RCA. Corrects the hypothesis in commit `5758044`'s message
("Drill 2 ... drill can't reliably set the cross-node confirmer-beat precondition").
That hypothesis is **wrong** — the beats ARE set fine. Real cause below.

## Symptom
`test-chaos-drill` Drill 2 (split-horizon + indirect-probe suppression) fails 2/2 runs:
```
FAIL: Indirect-probe: suppression log missing
FAIL: Indirect-probe: alert still fired despite confirmer
```
`mind-watch.log` shows only `ALERT ... confirmed by 2nd prober` — no `SUPPRESS`, no `SKIP`.
So `mesh-mind-watch confirmed_down()` returned 0 (agree-DOWN) via the **empty-cage** branch
(line 117: `[ -z "$cage" ] && return 0`).

## What I ruled OUT (verified against reality)
- **Confirmer logic** is sound. Reproduced the FULL drill mutation set by hand (local
  split-horizon + remote split-horizon on ds + ds beat fresh + phaedra beat fresh) and ran
  the exact `confirmed_down` confirmer SSH: returned `cage=6s` → would correctly SUPPRESS.
- **Beat precondition** is fine. ds beat set fresh by step 9 (`-F /dev/null`, bypasses the
  split-horizon → reaches real ds). phaedra beat set fresh by step 2. Both verified present.
- **Confirmer selection** is correct. `bash -x` trace: `chosen_confirm=root@<phaedra>` (the
  real peer, NOT the split-horizoned TARGET_NODE fallback).
- **Thin-PATH** on phaedra is already handled: `confirmed_down` line 114 prepends
  `PATH=$HOME/.local/bin:$PATH` for the remote invocation.

## Root cause — nested-SSH latency vs an 8s inner timeout
`confirmed_down` makes a **two-level nested** SSH:
`local → phaedra` (confirmer), then on phaedra `mesh-mind-watch --node ds --status` does
`phaedra → ds` **twice** (line 55 `hostname`, line 60 `cat beat`), each with its own
`ConnectTimeout=8`.

Measured the WARM path: **6.66s**. That is already perilously close to 8s while warm.
On a COLD Tailscale path (DERP/NAT-traversal setup), the inner `phaedra→ds` hop exceeds 8s
→ inner ssh times out → empty `BEAT_TS` → phaedra's `--status` emits no `thought Ns` line →
local `cage` is empty → line 117 treats "confirmer couldn't form a view" as
"confirmer agrees DOWN" → false ALERT → Drill 2 FAIL.

A **timed-out** connection does not warm the path, so consecutive cold runs fail
deterministically (explains 2/2). My manual probes succeeded only because they ran AFTER the
drill runs and had warmed `phaedra→ds`.

## Two distinct issues
1. **Drill flakiness (fix here):** the assertion depends on a cold nested SSH finishing in 8s.
   Fix options, drill-side, lowest-risk first:
   - **Warm-up:** run the confirmer probe once (discard result) before the asserting
     `mesh-mind-watch` call, so the real internal `confirmed_down` runs on a warm path.
   - **Retry:** re-run the assertion up to N times on empty-cage (SWIM confirmation is
     inherently probabilistic under latency — a drill should tolerate it).
   - Combine warm-up + one retry for robustness.
2. **mesh-mind-watch semantics (leave AS-IS):** line 117 conflates "confirmer unreachable /
   no view" with "confirmer agrees DOWN" — the [[fusion-tools-distinguish-empty-from-failed]]
   antipattern. BUT here it is a **deliberate fail-safe-toward-alerting** for production: if
   you cannot confirm, alert. Do NOT "fix" it to suppress-on-uncertain — that would silence
   real outages whose confirmer is also unreachable. The drill must adapt to this, not the
   reverse.

## Don't
- Don't mask Drill 2 FAIL→SKIP (hides a real-bug signal unproven).
- Don't raise mesh-mind-watch's production `ConnectTimeout` to paper over the drill — that
  slows genuine mind-down detection fleet-wide.

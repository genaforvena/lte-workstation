# Spec: mind-wake reactor fires on a STABLE state signature, not telemetry noise

**Operator 2026-07-18 (via tg), URGENT ("сделать надо макс быстро").** Owner: genome.

## Problem (empirical)
`mesh-pane-consume <ch> --interval N` is the mind-wake reactor: diff-gate the top DATA pane, wake the
MIND pane only on a change ("капельки/droplets", operator 2026-06-25). It is running & diff-gated for
every mind (kept alive by `mesh-liveness-loop`→`mesh-consume-all`, not cron). But `~/.mesh/pane-consume.log`
shows vpn waking every ~2h (= its `--interval` 7200s), bruno every ~4h — while one honest
`08:34 vpn: pane unchanged — no wake (droplet held)` proves the gate itself works.

Root cause: `pane_sig()` hashes the whole pane after `strip_volatile()`, which strips only
clocks / `N ago` / `age N` / `as of` / `refresh Ns` — **NOT live numerics** (latency `7.75→8.1ms`, byte
counters, handshake-age variants) that fill telemetry-rich panes. So the mind wakes on numeric JIGGLE,
not a meaningful state change. This is the operator's "кроны в vpn/bruno не по диффу топ-пейна."

Operator's model (confirmed): **minds wake ONLY on a change in the data they watch.** Sensor/producer
crons that FILL the panes are correct and STAY — this is ONLY the mind-wake path.

## Fix
Each `mesh-dash` role emits a **stable wake-signature** — a line carrying ONLY mind-relevant STATE
(verdicts UP/DOWN, peer/task presence, counts that matter), never volatile telemetry (latency ms, bytes,
per-frame ages). The reactor hashes the **wake-signature**, not the whole pane.

Preferred mechanism (explicit, per-role — the dash knows what's meaningful):
- Each dash prints a machine-readable trailer line, e.g. `WAKE-SIG: vpn=UP peers=16 egress=OK` (one line,
  stable across frames unless STATE changes).
- `pane_sig()` extracts `WAKE-SIG:` if present and hashes ONLY that; falls back to the current
  `strip_volatile | sha1sum` for panes that don't yet emit one (incremental rollout, no big-bang).

Alternative (cheaper, riskier — may mask a meaningful count): extend `strip_volatile` to strip
unit-bearing numerics (`[0-9.]+ms`, `[0-9]+ ?B|KB|MB`, `[0-9]+[KMG]?B/s`). Do NOT rely on this alone.

## Gate (must be RED-first)
`mesh-pane-consume --test` extension: build a pane frame with a jiggling latency + a stable `WAKE-SIG`,
prove two frames with different latency but same WAKE-SIG hash **equal** (no wake); flip the verdict in
WAKE-SIG and prove they **differ** (wake). Mirror the existing strip_volatile test (mesh-pane-consume
~L144-148). Verify RED against the current whole-pane hash, GREEN after.

## Scope & order
1. Reactor core: `mesh-pane-consume` `pane_sig()` prefers `WAKE-SIG:` when present. + `--test` gate.
2. Emit `WAKE-SIG:` from `mesh-dash` for **vpn** and **bruno** first (the reported offenders), verify
   via `~/.mesh/pane-consume.log` that they stop waking on jiggle.
3. Roll `WAKE-SIG:` to every remaining mind-channel dash role (minds/senses/health/chat/room/sound/models).

Sensor/producer crons: UNTOUCHED. Deploy each change to `~/.local/bin` + keep `scripts/` in sync.

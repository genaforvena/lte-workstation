# CORRELATION desk-AWAY × psi-BUSY — DISCARDED (proxy coincidence, 2026-09-23)

Claim (idea-queue row 1483): when desk reads AWAY, psi tends to read BUSY (lift 1.85,
14 episodes, era-restricted; 8 occasions / 14 episodes of 780, window 900.2h).

Verdict: DISCARD — no fused sense, no reflex. One line why: AWAY means the remote iMac
is unreachable/asleep while BUSY means this node's kernel pressure — different machines,
different physics — and the live miner refuses the pair (UNSTABLE 1/9 envs, era lift 1.21).

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: no AWAY×BUSY line at all — the pair does not
  surface on the current tape; `--list` likewise empty. The queued seed is stale.
- Prior full verdict (docs/correlation-investigation-desk-away-psi-busy-spurious-2026-09-08.md):
  era re-filter (578.2h, 1110 rows) gives raw lift 1.23, hour-shadow adjusted 1.21 <
  1.8 floor; miner full-window candidate 2.23 but invariance UNSTABLE (1 of 9 envs clears;
  env17 2.66 alone, others 0.00–1.44 — env18 had AWAY×30 + BUSY×5 with zero co-occurrence).
- Mechanism: `scripts/mesh-desk-state` emits AWAY on iMac UNREACHABLE ("off or asleep"),
  a night/network availability proxy; `psi=BUSY` is local CPU/IO/memory pressure
  (some≥25%), recently `who=user.slice`. Overlap is a shared night/workload regime, not
  a desk-to-pressure coupling. A fused sense would turn a proxy coincidence into an action.
- `scripts/mesh-correlate --test`, `--desk-state --test`, `--psi --test` all rc=0 (per
  prior verdict; miner behavior confirmed live above).

No tool edited: the invariance + hour-shadow gates that kill this pair already exist and
the live re-test confirms the refusal. Receipt left uncommitted for steward landing.

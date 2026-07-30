# Metastable failure — the busy-but-useless quadrant `mesh-quota` was blind to

**Live literature review · distributed-systems coordination · 2026-07-29 · genome mind**

## The area & the angle

Distributed-systems coordination measures itself with concrete operational metrics: convergence
time, staleness bounds, offered-load-vs-goodput curves. Prior landings in this area sit on
`mesh-chat-sync` (the board as a G-Set CRDT): PBS t-visibility, vAoI/Age-of-Gossip, HLC order, and
the causal-stability **frontier** (landed 2026-07-28). This one lands somewhere new: **quota/spend
coordination**, on `scripts/mesh-quota`.

## The concept — METASTABLE FAILURE

A **metastable failure** is a *self-sustaining congestive collapse*: a transient trigger (a load
spike, a rate-limit) tips a system from a high-goodput stable state into a low-goodput one, and it
**stays stuck there even after the trigger clears** — because its own work-amplification (retries)
keeps it saturated. Bronson's phrase is "busy and useless." The defining property is **hysteresis**:
the load that *sustains* the collapse is lower than the load that *triggered* it, so removing the
trigger is not enough — recovery needs a **nudge** (load-shed / drain / backoff-reset), not patience.

Sources (searched live, 2026-07-29):
- Bronson, Aghayev, Charapko, Zhang — *Metastable Failures in Distributed Systems*, **HotOS '21**.
  https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf
- Marc Brooker — *Metastability and Distributed Systems*, 2021.
  https://brooker.co.za/blog/2021/05/24/metastable.html
- *Formal Analysis of Metastable Failures in Software Systems*, **arXiv:2510.03551** (2025) — CTMC
  state-space: "once the queue exceeds 40 and retries hit 30, the system spirals into a self-sustaining
  feedback loop; below that, it trends toward recovery." (An explicit trigger/sustain hysteresis.)
- Isaacs, Alvaro — *Analyzing Metastable Failures*, **HotOS '25**.
  https://sigops.org/s/conferences/hotos/2025/papers/hotos25-106.pdf

## Do we already embody it? No — and the blind spot is exact

`mesh-quota` is the mesh's spend/quota truth surface. It reports **offered load** (burn = paid
round-trips from `spend.log`) and classifies three quadrants:

| quadrant | meaning | `mesh-quota` verdict |
|---|---|---|
| quota live + minds idle | wasting limits | WASTE |
| walled + no fallback | trigger present, no egress | DOWNTIME |
| live + burning | working | healthy |

The fourth quadrant is missing. `mesh-quota` has **no goodput axis** — it equates `burn > 0` with
"working" (`healthy — live & working`). But burn counts *round-trips*, not *completions*. A retry-loop,
or `mesh-failover` re-dispatching stranded tasks onto an also-saturated pool, burns round-trips with
**zero board completions**, and — being non-walled — reads as *healthy*. That is precisely the
metastable quadrant, and it is the one state the dashboard could not see. (Cf. the mesh's own
`retrying-opencode-reads-as-sovereign` and `mind-401` retry-loops: a retry reads as liveness.)

## The landing — `mesh-quota --metastable` (busy-but-useless precursor)

Added a read-only precursor axis (`scripts/mesh-quota`, +~55 lines). It cross-references the two real
logged artifacts:

- **busy**    = paid burn over a persistence window (`spend.log` — offered load)
- **useless** = **zero** `[done]` posts on the board over that window (`chat.log` — goodput)
- **cleared** = **no** fresh rate-limit wall in the window (`.rl-cooldown-*` / board `[mind-limited]`)

`STALL (precursor) = busy ∧ useless ∧ cleared`. It is **disjoint from DOWNTIME by design** (a fresh
wall = trigger still present → not metastable). Posture is **visibility-only**, like resource-guard's
`DUAL-ELEVATED` — it flags and points at the nudge (`mesh-failover --scan` / `mesh-quota-resume`),
never acts. It is exposed three ways: `--metastable` (rc 0 clear · 1 STALL · 2 UNKNOWN), a
`"metastable"` block in `--json`, and a line in the text dashboard that appears **only** when it fires
or is UNKNOWN (a `clear` is the silent norm).

Two doctrines honoured:
- **Honest fusion.** An unreadable `spend.log` *or* board renders **UNKNOWN**, never a confident
  all-clear (`board_done_since` returns `-1` for unreadable, distinct from `0` = none).
- **Calibrate against the live corpus, not a constant.** The persistence window is **3× the board's
  own median `[done]` cadence** (a dry spell must be abnormal *relative to how fast the board normally
  completes work*), clamped `[60, 240]` min, overridable via `MESH_QUOTA_STALL_SPAN`. A pinned
  constant would rot as the board's tempo changes. Live right now: 81 `[done]`/24h → span 60m.

## Verification

- `mesh-quota --test` extended with 5 isolated cases — STALL fires; a fresh `[done]` clears it
  (goodput present); a fresh wall clears it (trigger not cleared); burn below floor clears it (idle,
  not busy); unreadable board → UNKNOWN (never a false clear).
- **RED-first proven**: inverting the goodput clause makes case 1 fail
  (`FAIL … metastable STALL scenario did not fire: clear 4 0 0`); restored → `smoke-test: ok`.
- Live: `metastable: clear — burn=5 good=7 wall=0 over 60m window` (healthy: spending *and*
  completing). JSON: `"metastable":{"verdict":"clear","burn":5,"goodput":7,"wall":0,"span_min":60}`.

## Scope note

Left uncommitted for the steward. Unrelated pre-existing stderr noise (line ~72, `hms`/`fmt_gap`
called with an empty reset on a `MISSING` window) was observed but **not** touched — out of scope,
would muddy the diff.

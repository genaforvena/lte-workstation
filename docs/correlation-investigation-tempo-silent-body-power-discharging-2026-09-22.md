# CORRELATION investigation — `tempo=SILENT` ↔ `body_power=DISCHARGING`: **SPURIOUS** (common cause), 2026-09-22

**Emitted claim:** "when tempo reads SILENT, body_power tends to read DISCHARGING — lift 1.80 (58 episodes), hour-stratified … 28 distinct occasions / 58 episodes of 776, window 1626.2h." Invariance=UNSTABLE (clears 1.8 in 1 of 7 envs) — Markov blanket, not stable blanket.

**Verdict: SPURIOUS / discard.** No fused sense, no reflex, no tool edit. Common cause: the evening undocked-phone regime drives both labels; most of the lift is phone-readability, not discharging-ness.

## Reality check (live `~/.mesh/sensor-tape.tsv`, 6472 aligned rows)

- Row-level `P(DISCHARGING|SILENT)=0.338` (94/278) vs base 0.064 — but `P(readable|SILENT)=0.507` vs base readability 0.148 (**readability lift 3.43**). SILENT *requires* answering phone/light axes (`scripts/mesh-activity-tempo:506-520`: wifi-STILL + light-DARK, or tamper-QUIET + light-DARK) — a silent room is by construction a room whose sensors answer. The lift is mostly "the phone answered", not "the battery drains".
- Within phone-readable rows only, hour-stratified lift = **1.48 < 1.8 floor** (support 130). Nothing survives the floor once readability is conditioned out.
- Lead-lag: phone already DISCHARGING at SILENT onsets (20/32 = 0.625) at the same rate as during SILENT (94/141 = 0.667) — silence does not precede discharge; the phone was unplugged first.
- Reverse is weak: `P(SILENT|DISCHARGING)=0.227` vs `P(SILENT|CHARGING)=0.151` (1.5×), while `P(SILENT|FULL)=0.030`. The real split is docked-at-desk (FULL, day, lit/active) vs on-person (DISCH/CHARGING, evening) — SILENT just marks evening (SILENT hour hist peaks 16–23h).
- Light alone does not explain it either (`P(DISCH|DARK,readable)=0.441` vs DIM 0.473 highest) — it is the routine (unplugged + dark + still), not any one axis.

## Mechanism

Operator unplugs the phone in the evening, room goes dark and still → wifi-STILL + light-DARK → SILENT, while the carried phone reads DISCHARGING. Neither causes the other; the evening routine causes both. Consistent with 1-of-7-envs instability: the routine is environment-specific.

## Why not "useful anyway"

A SILENT+DISCHARGING "settled for the evening" fuse adds nothing over SILENT + hour-of-day (residual 1.48 < floor), and it does not generalize (UNSTABLE). No gate to wire.

Discard in one line: SILENT requires answering phone/light axes so it selects readable-phone evening hours when the undocked phone is already discharging — common-cause regime, not structure.

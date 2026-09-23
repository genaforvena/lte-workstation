# CORRELATION psi-BUSY × presence-NONE — USEFUL AS BLINDNESS SIGNAL, NOT ABSENCE (2026-09-23)

Claim (idea-queue row 1508): when psi reads BUSY, presence tends to read NONE (lift 2.2,
8 occasions / 8 episodes of 556, window 907.2h, no gate re-measurement).

Verdict: NOT a person-absence fusion; USEFUL as a sensor-blindness signal — and the
useful repair is already landed. One line why: BUSY coincides with the RTL8822BU combo
radio returning false zero-contact BLE scans, so NONE under load means "don't trust this
absence", never "nobody is here".

Evidence (live, 2026-09-23, read-only):

- `scripts/mesh-correlate --dry` rc=0: no BUSY×NONE line; `--list` likewise empty. The
  queued seed is stale; the live tape refuses the pair as a behavioral coupling
  (prior: hour-shadow DROPPED, stratified 0.62 < 1.8; UNSTABLE 0/2 envs).
- Mechanism (real artifacts, per 2026-09-08 verdict): 21/34 plain `n=0` scans sandwiched
  between non-empty scans sharing three devices; a shelf speaker in 3109/3156 non-empty
  scans (99%) cannot leave for one sample. Under load the combo radio returns
  `known=0` + `Discovering=no`, accepted as a clean empty; `mesh-sensor-tape` encodes
  that blindness as NONE. All 10 co-occurrences had room_sense=PRESENT +
  household=ACTIVE + home_state=ACTIVE — NONE contradicting an occupied room.
- Repair already present in `scripts/mesh-presence` (verified live above):
  `anchor_count` reads the last six non-empty scans; `anchor_empty` turns `n=0` with a
  persistent anchor into `SUSPECT(anchor)`/exit 3, capped so a departed anchor cannot
  suppress empties forever. Minimal fusion at the producer boundary; PSI stays
  explanatory corroboration, never a hard occupancy veto.

No tool edited; no new sense/reflex proposed (would duplicate the landed anchor guard).
Receipt left uncommitted for steward landing.

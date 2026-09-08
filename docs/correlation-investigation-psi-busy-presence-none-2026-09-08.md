# Correlation investigation: `psi=BUSY` ↔ `presence=NONE`

Date: 2026-09-08  
Verdict: **real and useful as a sensor-blindness signal; not a person-absence
fusion.** The pressure does not make the room empty. It coincides with the
RTL8822BU combo radio returning a false zero-contact BLE scan.

## Recheck against the live sources

The queued claim was lift 2.2, 8 autocorrelation-collapsed episodes / 8
occasions, 556 aligned rows over 907.2 h, with no gate re-measurement. The
earlier live investigation (2026-08-21) independently found the same direction
with raw-bin lift 2.01 and episode lift 2.2; all 10 co-occurrences had
`room_sense=PRESENT`, `household=ACTIVE`, and `home_state=ACTIVE`, so `NONE`
was contradicting an occupied-room reading rather than measuring absence.

The current tape has moved on. A fresh `scripts/mesh-correlate --stable` run
now emits the decisive recheck:

```text
hour-shadow: DROPPED psi=BUSY <-> presence=NONE (lift 1.85, 16 episodes)
— shadow with psi=BUSY's exact hour histogram already scores 1.02 of the
  observed 0.64; hour-stratified lift 0.62 < 1.8
```

That current pooled association is therefore not a stable behavioral coupling;
its apparent support is concentrated in the time/availability regime in which
both sensors answer differently. The stable blanket report also keeps this
pair `UNSTABLE` (0 of 2 qualifying environments clears the 1.8 floor in the
last environment partition).

## Mechanism found in the real artifacts

`mesh-presence` and the node's sole Wi-Fi uplink share the RTL8822BU USB radio.
The prior ledger audit found 21 of 34 plain `n=0` scans sandwiched between
non-empty scans sharing three devices; a mains-powered shelf speaker appeared
in 3,109 of 3,156 non-empty scans (99%). A device with that persistence did not
leave for one ten-minute sample and return. Under load, the combo radio can
produce a clean, quiesced, cache-blank zero-contact result: `known=0` and
`Discovering=no`, so the older `known` and stuck-discovery guards both accepted
the false empty. `mesh-sensor-tape` then encoded that blindness as
`presence=NONE`.

This is useful, but the useful sense is **BLE read validity**, not occupancy:
`psi=BUSY ∧ presence=NONE` should lower confidence in the BLE absence and yield
UNKNOWN/BLIND, never assert that nobody is present.

## Action and disposition

No new fused sense or reflex is proposed. The appropriate source-level repair is
already present in `scripts/mesh-presence`: `anchor_count` reads the last six
non-empty scans, and `anchor_empty` turns `n=0` with a persistent anchor into
`SUSPECT(anchor)` / exit 3. Its three-scan latch cap prevents a genuinely
departed anchor from suppressing empties forever. This is the minimal useful
fusion at the producer boundary; PSI remains explanatory corroboration, not a
hard occupancy veto.

One-line causal verdict: **the observed correlation is a real pressure-coupled
BLE blindness artifact, useful for degrading presence confidence, but not
evidence that PSI causes or predicts human absence.**

## Verification

- `scripts/mesh-correlate --stable`: current hour-shadow drop, adjusted lift
  0.62; pair is `UNSTABLE` across qualifying environments.
- `bash scripts/mesh-correlate --test`: pass.
- `bash -n scripts/mesh-presence`: pass; source contains and wires the anchor
  guard after the `known=0`/wedge paths and before publishing an empty.
- `bash scripts/mesh-psi --test`: pass.
- `bash scripts/mesh-presence --test`: honest `rc=2` / n/a because this node has
  no Bluetooth adapter (`/sys/class/bluetooth` absent); it did not fabricate a
  live scan.
- Source and deployed `mesh-presence` hashes match
  (`05bf81d7…232c5e4`); no deployed-only edit was made.

This artifact is intentionally uncommitted for the steward.

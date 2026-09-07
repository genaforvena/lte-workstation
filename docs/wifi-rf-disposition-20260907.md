# wifi-rf deficit disposition — 2026-09-07

Decision: (c) accept the deficit as-is with an expiring, visible mute. This is an
organ-absence condition, not a repairable reflex failure and not a candidate for
retirement: the sense remains useful if a Wi-Fi radio returns.

Evidence:

- The same `REFLEX REPAIR` cue was re-filed four times; the cue-pinned escalation
  was emitted at `2026-08-30T07:30:12Z` (`~/.mesh/needs.log`, `n=4`).
- `iw dev` is empty on this node and the RTL8822BU combo Wi-Fi/BT dongle is absent;
  the sole uplink is the USB-tether interface. `mesh-wifi-rf --test` exits `2`.
- `mesh-reflex-health --check` currently reports
  `organ-absent: wifi-rf(n/a ... --test exits 2 ...)`, so the reflex is not classified
  as dead. The source fix already removes `$STATE` before this honest `rc=2` path
  (`scripts/mesh-wifi-rf`, lines 904–919), preventing a stale RF reading from being
  consumed as current.
- `mesh-reflex-health`'s organ-absence gates cover this branch; changing the watcher
  or retrying the repair would regress the distinction between absent organ and dead
  reflex.

Verdict:

```text
mesh-needs --rule reflex:wifi-rf 7 "accept organ absence on this node; mesh-reflex-health reports the wired reflex as organ-absent and mesh-wifi-rf --test exits 2; recheck after expiry"
```

The live ruling is visible through `mesh-needs --rulings`, expires
`2026-09-14T15:01:12Z`, and must be re-evaluated then. `mesh-needs --check`
currently reports no active deficit while retaining the ruling as visible state.

Verification performed on 2026-09-07:

```text
mesh-needs --rulings                         PASS — LIVE reflex:wifi-rf
mesh-needs --check                           PASS — no acute active deficit
timeout 8s mesh-reflex-health --check        PASS — organ-absent: wifi-rf, rc=0
sha256(source) == sha256(deployed)           PASS — c305c86d...
bash -n scripts/mesh-needs scripts/mesh-reflex-health scripts/mesh-wifi-rf  PASS
```

Next action: after expiry, check whether a Wi-Fi organ is present; only then
re-file a repair if the sense still fails with the organ available.

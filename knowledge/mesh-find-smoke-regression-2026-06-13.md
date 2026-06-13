# mesh-find smoke regression (2026-06-13)

`mesh-find --test` regressed because its smoke path called the live BLE scanner and
required a device to be in range. On this node the BLE dependency exists and
`mesh-presence --test` passes, but the live scan can still return exit 1 when no
devices are visible, which is a normal environment state, not a broken tool.

Bounded fix:
- keep the dependency checks (`mesh-presence --test`, `ssh`, `mktemp`, `grep`, `tr`)
- exercise the actual parser/search logic with synthetic scan rows in a temp dir
- leave the live query path unchanged

Result:
- `scripts/mesh-find --test` now passes without requiring nearby BLE devices
- a live `scripts/mesh-find Bose` query still runs and returns an honest empty result

# AMD PSP/CCP runtime health decision

Date: 2026-09-09  
Node: `mesh-home`  
Capability source: `~/.mesh/knowledge/capability-amd-psp-ccppci-runtime-status-mesh-home-20260909.md`

## Verified evidence

The live sysfs function `/sys/bus/pci/devices/0000:2d:00.1/` currently reads:

```text
vendor=0x1022
device=0x1486
class=0x108000
numa_node=-1
power/runtime_status=active
driver=/sys/bus/pci/drivers/ccp
```

This satisfies the capability's five-field predicate. The captured two-sample artifact remains
`/tmp/capability-amd-psp-ccp-20260909.txt` with SHA-256
`b016a30711fb1e37679e2073a867f064c2718fbd0826bf96ba064796d5b84fb7`.

## Health semantics

This is a live node-local hardware/runtime sense, not TPM PCR evidence and not generic PCI
enumeration.

- `OK`: the expected `1022:1486` function is present, all five fields are readable, the driver is
  `ccp`, and `power/runtime_status=active`.
- `WARN: stale/unknown`: the last complete read is older than two `mesh-hw-health` cadences (one
  hour at the current 30-minute cadence), or a required field cannot be read. Staleness is an
  evidence/coverage failure, not proof that the PSP is down.
- `FAIL: absent` or `FAIL: identity/driver/runtime`: this node is declared to have the capability,
  but the PCI function disappears, its identity changes, it loses the `ccp` binding, or its runtime
  status is not `active`. A disappeared expected security coprocessor is a hardware/integrity
  failure, not an ordinary “not applicable” result.

The expected-device declaration must be node-scoped. A node without this capability is `unmeasured`
(and therefore cannot make aggregate health green), not `FAIL` and never a fabricated `OK`.

## Wiring ownership

The owner is `mesh-hw-health`: this is a per-node hardware/runtime check sampled on its existing
30-minute `--edge` cadence. It should contribute to the existing `.hw-health.state` aggregate and
state-change board edge. `mesh-boot-integrity-recorder` remains TPM-PCR-only; adding PSP state there
would conflate a live runtime sense with once-per-boot measured-boot evidence.

Current wiring status: **known blindness**. The source and installed `mesh-hw-health` are identical,
but neither reads this PCI function. The capability is verified and the ownership/semantics are
decided; implementation remains a separate change.

## Checks run

- Live five-field sysfs read: pass.
- Capability artifact SHA-256: pass.
- `mesh-reflex-health`: pass for the existing 37 per-run reflexes, with unrelated declared blind/
  absent/overwrite-only senses reported by the tool.
- `mesh-hw-health`: live report reached thermal, fan, disk SMART, and battery checks; the bounded
  `--test` did not complete within 30 seconds and is recorded as an incomplete verification, not a
  pass.

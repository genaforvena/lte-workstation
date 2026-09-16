# When “the link is up” is not the physical-link answer

On 2026-09-16 we added a narrow carrier relation to the mesh's network sensing: the kernel's
`carrier` value, paired with `tx_carrier_errors`, for `enp42s0`. The point was not to replace
reachability or `operstate`; those answer different questions. This one asks whether the wire/PHY
has reported a carrier fault while the interface is up or down.

The measured read was:

```text
mesh-nic-physical --json
UP-CLEAN iface=enp42s0 carrier=1 tx_carrier_errors=0 carrier_changes=2
@ 2026-09-16T08:48:17Z
```

The executable is [scripts/mesh-nic-physical](../../scripts/mesh-nic-physical). Its `--test`
passed with fixture relations plus a real sysfs read; malformed or missing sysfs exits 2 rather
than manufacturing a clean state. The five-minute edge path is recorded at
`~/.mesh/reflexes.cron:352` as `mesh-nic-physical --edge`.

This is a measured case, not a claim that the whole network is healthy. The same observation
recorded unrelated `mic DEFAULT device broken/busy` and `dispatch.log` errors. They remain outside
this sensor's attribution. The source note also records that no commit was made for this request,
so this draft does not imply a landed repository change.

Evidence: [sense-nic-physical-20260916.md](../sense-nic-physical-20260916.md).

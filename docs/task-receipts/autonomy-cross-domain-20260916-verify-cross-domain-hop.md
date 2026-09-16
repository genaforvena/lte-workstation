# Cross-domain hop receipt — 2026-09-16

Task: `autonomy-cross-domain-20260916/verify-cross-domain-hop`  
Owner: `vpn`  
Observed: `2026-09-16T03:12Z`

## Operation and evidence

The source independently identified `phaedra` from the live Tailscale netmap:

```text
source mesh-home: 100.81.222.19, tag:lte-node
target phaedra: 100.94.116.17, online=true
```

The kernel FIB, rather than a preference, selected the transport to the target:

```text
100.94.116.17 dev tailscale0 table 52 src 100.81.222.19
```

The reverse lookup on phaedra independently selected the return transport:

```text
100.81.222.19 dev tailscale0 table 52 src 100.94.116.17
```

The live transport probe succeeded:

```text
pong from phaedra (100.94.116.17) via 38.49.216.141:41641 in 136ms
```

The cross-domain service path performed a real fetch through the VPN client and passed:

```json
{"port":8444,"status":"PASS","egress_ip":"38.49.216.141","city":"Montréal","country":"CA"}
```

## Identity checks

Tailnet IP and endpoint duplicate checks over the live netmap returned empty sets:

```text
tailscale_ip_duplicates=[]
endpoint_duplicates=[]
```

Remote read-only SSH identity evidence:

```text
phaedra hostname=phaedra
phaedra tailscale_ip=100.94.116.17
phaedra machine_id=3488f3a484244a1d963c190cdc3b0f2a
phaedra product_uuid=3488f3a4-8424-4a1d-963c-190cdc3b0f2a
phaedra physical_mac=bc:24:11:b0:e1:47
mesh-home machine_id=b4515d0443e648879817859b053d3bea
mesh-home physical_mac=enp42s0 b6:1d:61:88:06:e7
machine_id_duplicate=NO
physical_mac_duplicate=NO
```

The source has no DMI product UUID (`unavailable`), so physical uniqueness is established by the
different machine IDs and active MACs, not by an unavailable source UUID. A separate `mesh-card
--refresh` reported an unrelated local identity-coherence conflict (`25`, redeclared
`MESH_MINDS_CMD`); that conflict is retained as a warning and was not used to mint a network
identity verdict.

## Retry / rollback edge

This verification made no configuration, routing, DNS, firewall, WireGuard, or service changes;
rollback is therefore “no action.” On a later failure, retry the same read-only sequence:
`tailscale status --json` → `ip route get 100.94.116.17` → `tailscale ping --c 1 phaedra` →
`mesh-ss-test --edge --json`. Do not restart a working VPN or run `tailscale up` as part of this
receipt.

Result: PASS for the cross-domain Tailscale-to-phaedra-to-public-egress operation; identity
coherence warning remains separately open.

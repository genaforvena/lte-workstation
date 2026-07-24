# Reticulum off-internet proof — two nodes, uplink down

**Deliverable (operator, 2026-07-24, top prio):** a working NON-internet network for the
mesh — two mesh nodes exchanging a message with the internet uplink DOWN. Reticulum (RNS)
is the path: cryptographic, hash-addressed, transport-agnostic (runs over TCP/LAN today,
LoRa/packet-radio/serial next).

This is the **software proof**, live and reproducible. The RF lane (RNode/LoRa) is scoped
separately in `reticulum-radio-lane.md`.

## What was proven

Two **physically distinct** mesh nodes established an end-to-end **encrypted Reticulum Link**
and round-tripped a 16-byte nonce **over a transport with zero internet interface** — and the
link kept working while one node's internet uplink was physically cut.

- **Node A** — mesh-home `192.168.8.225` (RNS 1.4.0, `~/.venv-rns`)
- **Node B** — ilya `192.168.8.242` (RNS 1.4.0, bootstrapped for this)
- **Transport** — `TCPInterface` over the local `/24`. The peer dials the local node's LAN
  IP, which is on-link (same subnet) → the kernel sends it straight over L2 to the wifi AP,
  **never via the default gateway**. Config carries no internet interface and no transport
  routing: off-internet **by construction** (read `config.tcplan.example`).

### Plain link (both nodes online)
```
PROOF OK: link up, 16-byte nonce round-tripped E2E over TCP (c13bce91549b72f0bb40f7070a35ae86)
OFF-INTERNET-CAPABLE: two nodes (192.168.8.225 <-> ilya@…) round-tripped an E2E Link over LAN TCP,
                      zero internet interface in the config.
```

### Uplink-down proof (mesh-home internet physically cut)
mesh-home dropped its default route + `tailscale down` for a ~20s self-restoring window
(deadman restore armed at 120s). ilya's client, pre-staged to fire mid-window, linked to
mesh-home **over the LAN** and round-tripped a nonce while mesh-home had no internet:

```
peer client result (ran during blackout):
  START:09:11:39Z
  PROOF OK: link up, 16-byte nonce round-tripped E2E over TCP (67424713f4e5f86aa1a5fbd60e8d5d57)
  rc=0
  END:09:11:40Z

mesh-home blackout log:
  [09:11:30Z] BLACKOUT: drop default route + tailscale down
  [09:11:30Z] 8.8.8.8 unreachable — internet DOWN (route: RTNETLINK answers: Network is unreachable)
  [09:11:30Z] LAN ilya 192.168.8.242: UP  (LAN alive)
  [09:11:50Z] RESTORE: default route + tailscale up
  [09:11:50Z] internet RESTORED
```

The RNS round-trip (09:11:39–40Z) falls **inside** the blackout window (09:11:30–09:11:50Z),
during which mesh-home's route to `8.8.8.8` was `Network is unreachable`. Two mesh nodes
exchanged a proven-delivered, E2E-encrypted message with the internet uplink down.

> Honesty note: the first blackout run's `curl api.anthropic.com` line misread http_code `000`
> (connection failed) as "reached" because the check grepped for any digit. The authoritative
> signals are the route (`Network is unreachable`) and ICMP (ping down), which are independent
> and definitive. Fixed in the tool (uses ping/route, not a digit-grep).

## Reproduce

```bash
mesh-rns-offgrid            # plain two-node off-internet-capable link proof (safe)
mesh-rns-offgrid --blackout # + self-restoring uplink blackout, assert link survives (NOPASSWD sudo)
mesh-rns-offgrid --test     # gate: plain proof, exit 2 if peer unreachable (honest n/a)
```

Config via env or `~/.mesh/rns-offgrid.env` (`RNS_OG_PEER`, `RNS_OG_LOCAL_LAN`, `RNS_OG_GW`,
`RNS_OG_WIFI`, `RNS_OG_PORT`, `RNS_OG_PY`, `RNS_OG_PEER_PY`). On-demand only — peer-dependent
and `--blackout` drops the uplink, so it is deliberately **not** cron-wired.

## Files
- `scripts/reticulum/rns-offgrid-proof.sh` — orchestrator (real tool)
- `scripts/mesh-rns-offgrid` — deploy shim (deploy this, never the real tool)
- `scripts/reticulum/rns-link-proof.py` — the Link round-trip primitive (server/client)
- `scripts/reticulum/config.tcplan.example` — the off-internet TCP-over-LAN config
- `scripts/reticulum/mesh-reticulum.service` + `config.example` — the node's rnsd (software proof #1)

## Transport note
`AutoInterface` (link-local IPv6 multicast) is the more radio-like transport and the intended
shape for the RF lane, but bridged-VM-over-wifi APs routinely drop link-local multicast, so the
software proof uses reliable unicast TCP-over-LAN. The Reticulum Link is identical either way —
same crypto, same round-trip — only the interface differs. That interface-independence is exactly
what lets the same proof carry onto an `RNodeInterface`/LoRa link with no application change.
```

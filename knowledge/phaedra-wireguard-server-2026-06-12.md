# phaedra: WireGuard VPN server for friends (operator request)

Date: 2026-06-12
Node: phaedra (Ubuntu 26.04 VPS) — Tailscale 100.94.116.17, **public 38.49.216.141**, WAN eth0
Operator: "setup vpn server on phaedra so even my friends can use it for their vpns + share
connect instructions" + "share in telegram".

## What was built

A standard WireGuard server, reboot-survival from the start (mesh doctrine):

- `apt install wireguard qrencode`
- server keypair in `/etc/wireguard/{server_private,server_public}.key`
  (server pub: `RcnsVNXhF+K+OWbGBmPGHIhZy4zvwaZBSI/vPNGCfSQ=`)
- `/etc/wireguard/wg0.conf`: `Address 10.66.66.1/24`, `ListenPort 51820`, and **PostUp/PostDown
  iptables** — `MASQUERADE -s 10.66.66.0/24 -o eth0` + `FORWARD` accept on wg0. ADDITIVE rules
  only (never flush → SSH stays open).
- `ip_forward` enabled + **persisted** `/etc/sysctl.d/99-wireguard.conf`.
- `systemctl enable --now wg-quick@wg0` → survives reboot.

## Friend onboarding (repeatable)

`/usr/local/bin/wg-add-friend <name>` — generates a friend keypair, registers the [Peer] on the
server (live `wg set` + persisted to wg0.conf), allocates the next free `10.66.66.X`, and prints
a ready client config (full-tunnel `AllowedIPs = 0.0.0.0/0, ::/0`, `Endpoint 38.49.216.141:51820`,
`DNS 1.1.1.1`, keepalive 25). One config per friend (own key+IP — don't share one).
`friend1` (10.66.66.2) generated as the first/example, saved `/etc/wireguard/clients-friend1.conf`.

Friend side: install WireGuard app → import the config (paste / .conf / QR via `qrencode`) → toggle on.

## Verified (real artifacts)

- `wg show wg0`: listening 51820, server pubkey present, 1 peer (friend1) after stale-test-peer cleanup.
- `iptables -t nat -C POSTROUTING -s 10.66.66.0/24 -o eth0 -j MASQUERADE` → ACTIVE.
- `iptables -C FORWARD -i wg0 -j ACCEPT` → ACTIVE.
- `ip_forward` runtime=1 + persisted file present.
- `systemctl is-enabled wg-quick@wg0` → enabled (reboot-survival).
- `ss -ulnp` → `0.0.0.0:51820` (all interfaces).
- SSH path intact throughout (additive iptables only).

## Substrate invariant

Clean: only the client subnet `10.66.66.0/24` is MASQUERADE'd out eth0; phaedra's own control
plane (SSH/Tailscale) stays on its normal eth0 route — it offers a route without carrying its own
reachability on it.

## Open / caveat

- **VPS provider cloud-firewall**: the OS firewall is open (ufw inactive, no restrictive INPUT
  added), but a provider-level firewall may block inbound UDP 51820 — if a friend can't connect,
  open that port in the provider console (operator action). Flagged to operator via TG.
- Not in the genome (phaedra-node-specific). Registry add (~/.mesh/nodes) coordinated with the
  mind that owns phaedra onboarding. A couldn't-do-it-myself handshake test (no root on a mesh
  client; netns localhost test was fiddly) → first real friend connection is the end-to-end proof.

# lte-workstation — Node Operator Context

This machine (`imozerov-Default-string`, Tailscale IP: `100.125.157.75`) is the **mind** node of the lte-workstation mesh. Claude Code runs here as the node operator.

## Your role

You are the operator of this node. You have:
- **Compute**: this Linux VM
- **Sensors**: phones on the Tailscale mesh reachable over SSH
- **Eyes/ears**: `termux-api` commands via SSH to Android nodes
- **Nervous system**: Tailscale mesh tagged `tag:lte-node`

## Mesh topology

```
tailscale status --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
for k,p in d.get('Peer',{}).items():
    if 'tag:lte-node' in (p.get('Tags') or []):
        print(p['HostName'], p['TailscaleIPs'][0], 'online:', p['Online'])
"
```

Known nodes as of 2026-06-06:
- `Redmi 10` — 100.103.99.16 (android, tag:lte-node) — phone body
- `ilya` — 100.107.198.111 (linux, tag:lte-node)
- `imozerov-IdeaPad-3-15IIL05` — 100.73.170.56 (linux, tag:lte-node, offline)

## Phone access (body node: Redmi 10)

```bash
# Battery status (no permission needed)
ssh -p 8022 -o StrictHostKeyChecking=no u0_a386@100.103.99.16 "termux-battery-status"

# Camera photo
ssh -p 8022 u0_a386@100.103.99.16 "termux-camera-photo -c 0 ~/photo.jpg"
scp -P 8022 u0_a386@100.103.99.16:photo.jpg /tmp/

# Audio recording (10 seconds)
ssh -p 8022 u0_a386@100.103.99.16 "termux-wake-lock; termux-microphone-record -l 10"
# Wait for completion, then pull file
```

See `docs/body.md` for full verification protocol (always check artifact size/validity).

## Services managed on this node

```bash
systemctl --user status ngrok.service bore-mtg.service proxy-bot.service vpn-hub.service
```

| Service | Purpose | Status |
|---------|---------|--------|
| `ngrok.service` | SSH tunnel with public URL → Telegram notification | running |
| `bore-mtg.service` | MTProto proxy via bore.pub + Telegram buttons | running |
| `proxy-bot.service` | Access-control bot (approve/deny proxy requests) | node-local userland |
| `vpn-hub.service` | Central WG config registry on port 9999 | **retired 2026-06-07** (topology is now node-local/gossiped, not central) |

Config: `~/.config/remote-access/env` (BOT_TOKEN, CHAT_ID, MTG_SECRET)

## tmux sessions (shared perception)

The agent runs in a **hostname-named** tmux session (convention). Other operators — human or agent — attach and share the same terminal state. (Append-only: see "tmux is append-only" below.)

```bash
# attach-or-create the node's session (run wherever an agent works)
tmux new-session -A -s "$(hostname)"

# attach from another node
ssh imozerov@100.125.157.75 -t 'tmux new-session -A -s "$(hostname)"'
```

The scrollback is memory. The session is the sensorium. Attaching is joining.

## Verification principle

Every claimed capability must produce a real artifact. Not "the camera works." A non-zero JPEG on disk. Not "audio recorded." A playable `.m4a`. Not "node online." A `tailscale status` entry with `Online: true`.

Extend it to **regressions, not just new powers**: the artifact for a network change is *every node still reaches the internet and the LAN* — captured **before and after** — not "the interface came up." `mesh-health` and `mesh-card --refresh` are those artifacts.

## Substrate changes & multi-agent coordination

Multiple agents run at once (often the same human directing several). Sensors/compute are a commons — mark freely. But the **substrate** (routing, `ip rule`/`ip route`, DNS, default route, `iptables`/`nft`, WireGuard/`wg-quick`, Tailscale exit-node, the SSH path) is **single-writer and contended**: one routing table per node, and a bad edit severs the path you reach the node through. Before any substrate change:

1. **Detect** other operators (`ps -u $USER -o pid,tty,etime,args | grep -E 'claude|opencode'`, `who`, `mesh-trace --tail 20`).
2. **Claim** ownership on the shared trace (`mesh-trace "<resource> + target + rollback"`).
3. **Coordinate via tmux** — reach the other agent's pane and ask it to hold; it acks in-channel and discloses outstanding changes. One writer at a time.
4. **Apply under `mesh-dms`** (dead-man's switch): schedule the rollback first, cancel only after `mesh-health` + `mesh-card --refresh` confirm the invariant.

**The substrate invariant:** a node that *offers* a route (exit-node, VPN egress) never carries its **own** control plane on it. Host stays on the clean default route; only *forwarded client* traffic rides the offered route, and the forwarding mark must **exclude** LAN/private ranges (`10/8`, `172.16/12`, `192.168/16`) and Tailscale CGNAT (`100.64/10`). `mesh-card --refresh` flags violations (exit ≠ 0).

Full protocol + the 2026-06-07 worked example: `docs/coordination.md`.

## tmux is append-only

All agent work runs in the one shared **hostname-named** session (`tmux new-session -A -s $(hostname)`); the scrollback *is* the node's recent memory. **Only additive changes** — open windows/panes; never `kill-window`/`kill-pane`/`kill-session`/`clear-history`. The only intended memory decay is reboot (clean reincarnation: same hostname + `~/.mesh-card`, fresh session). Concurrent agents take a **window/pane each** — shared history, independent hands.

## Node self-description: `~/.mesh-card`

Each node keeps a small current-state card (`mesh-card --refresh` regenerates it from live state and checks the substrate invariant). It is the durable memory tier; the trace (`~/.mesh/traces.log`) is the volatile history tier.

## WireGuard mesh

- Hub IP: `100.125.157.75` (this machine)
- Subnet: `10.9.0.0/24`
- Node DB: `~/.wg-mesh-nodes.json`
- Hub API: `http://100.125.157.75:9999/<hostname>` → returns WireGuard config

## Key paths

- Config: `~/.config/remote-access/env`
- Scripts: `~/.local/bin/` (ngrok-notify.sh, bore-mtg.sh, proxy-bot.py, vpn-hub.py)
- Services: `~/.config/systemd/user/`
- WireGuard DB: `~/.wg-mesh-nodes.json`

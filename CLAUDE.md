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
| `proxy-bot.service` | Access-control bot (approve/deny proxy requests) | running |
| `vpn-hub.service` | Serves WireGuard configs to joining nodes on port 9999 | running |

Config: `~/.config/remote-access/env` (BOT_TOKEN, CHAT_ID, MTG_SECRET)

## tmux sessions (shared perception)

The agent runs in a named tmux session. Other operators — human or agent — can attach and share the same terminal state.

```bash
# start operator session
tmux new-session -d -s operator

# attach locally
tmux attach -t operator

# attach from another node
ssh imozerov@100.125.157.75 -t tmux attach -t operator
```

The scrollback is memory. The session is the sensorium. Attaching is joining.

## Verification principle

Every claimed capability must produce a real artifact. Not "the camera works." A non-zero JPEG on disk. Not "audio recorded." A playable `.m4a`. Not "node online." A `tailscale status` entry with `Online: true`.

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

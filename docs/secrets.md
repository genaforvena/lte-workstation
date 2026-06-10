# Mesh credentials: shared, and never lost

How secrets are shared across nodes so no single node failure loses them.

## Model

Credentials fall into four classes, handled differently:

| Class | Examples | Handling |
|---|---|---|
| **Shared service secrets** | `BOT_TOKEN`, `CHAT_ID`, `MTG_SECRET` | Encrypted in `secrets/`, decrypted on every service node |
| **Mesh source-of-truth** | WG hub DB (`~/.wg-mesh-nodes.json`) | Backed up encrypted in `secrets/`; restored if lost |
| **Per-node identity** | each node's `age` key, tailscale identity, SSH host key | NOT shared — re-provisionable, not backed up |
| **Cross-node access** | reaching the phone body | Phone's `authorized_keys` holds each node's PUBLIC key (no private-key sharing) |

## Mechanism: `age` + SOPS in this (public) repo

- Each node holds ONE `age` private key at `~/.config/sops/age/keys.txt` — that is its identity.
- Every file in `secrets/` is encrypted to **all** node public keys **plus an offline recovery key** (`.sops.yaml`).
- The repo is public; SOPS+age ciphertext is safe to publish. A leaked node private key, however, compromises every secret here — rotate immediately if a node is lost to an attacker.

**"Shared"**: every node clones the repo and decrypts with its own key.
**"Never lost"**: three independent layers —
1. replication — N node copies survive N−1 losses;
2. git history — survives accidental deletion/corruption;
3. offline recovery key — survives *total* mesh loss (kept off-mesh, never committed).

## Daily use

```bash
scripts/mesh-secrets.sh hydrate   # decrypt repo store -> live config (runs at boot via systemd)
scripts/mesh-secrets.sh backup    # re-encrypt live source-of-truth -> repo store, then commit
scripts/mesh-secrets.sh check     # verify this node can decrypt everything
```

Boot-time hydration: `scripts/mesh-secrets.service` (systemd user unit).

## Enroll a new node

1. Install `age` + `sops` (static binaries in `~/.local/bin`).
2. `age-keygen -o ~/.config/sops/age/keys.txt && chmod 600 ~/.config/sops/age/keys.txt`
3. Add its public key (`age-keygen -y …`) to `.sops.yaml`, then `sops updatekeys secrets/*` from an existing node.
4. Clone this repo, run `scripts/mesh-secrets.sh hydrate`, install the systemd unit.

## Recovery key

The offline recovery `age` key is the root of trust. It is generated once, shown once, and stored **off-mesh** (password manager / printed / encrypted Telegram Saved Messages). With it + this repo you can recover every secret even if all nodes die. It is never committed.

## Current recipients

- `ideapad` — imozerov-IdeaPad-3-15IIL05 (100.73.170.56)
- `mind` — imozerov-Default-string (100.125.157.75)
- `recovery` — offline root of trust

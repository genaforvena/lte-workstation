# Mesh credentials: shared, and never lost

How secrets are shared across nodes so no single node failure loses them.

## Model

Credentials fall into four classes, handled differently:

| Class | Examples | Handling |
|---|---|---|
| **Shared service secrets** | `BOT_TOKEN`, `CHAT_ID`, `MTG_SECRET` | Encrypted in `secrets/`, decrypted on every service node |
| **Legacy mesh source-of-truth** | retired WG hub DB (`~/.wg-mesh-nodes.json`) | Kept only as historical backup material for the retired central overlay |
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

## Current reality

The encrypted-store design (`.sops.yaml` + per-node `age` identities) is still the intended model,
but the helper entrypoints documented here are **not** present in the current genome tree:

- `scripts/mesh-secrets.sh`
- `scripts/mesh-secrets.service`

So treat this document as the storage doctrine, not as a claim that those automation helpers exist
right now in-repo. Current nodes rely on the underlying `age`/`sops` material and local operator
handling, not a checked-in `mesh-secrets` wrapper.

## Enroll a new node

1. Install `age` + `sops` (static binaries in `~/.local/bin`).
2. `age-keygen -o ~/.config/sops/age/keys.txt && chmod 600 ~/.config/sops/age/keys.txt`
3. Add its public key (`age-keygen -y …`) to `.sops.yaml`, then `sops updatekeys secrets/*` from an existing node.
4. Clone this repo and hydrate secrets with the local `sops`/`age` workflow in use on that node.

## Recovery key

The offline recovery `age` key is the root of trust. It is generated once, shown once, and stored **off-mesh** (password manager / printed / encrypted Telegram Saved Messages). With it + this repo you can recover every secret even if all nodes die. It is never committed.

## Current recipients

- `ideapad` — imozerov-IdeaPad-3-15IIL05 (100.73.170.56)
- `mind` — imozerov-Default-string (100.125.157.75)
- `recovery` — offline root of trust

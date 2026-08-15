# Mesh credentials: shared, and never lost

How secrets are shared across nodes so no single node failure loses them.

## Model

Credentials fall into four classes, handled differently:

| Class | Examples | Handling |
|---|---|---|
| **Shared service secrets** | `BOT_TOKEN`, `CHAT_ID`, `MTG_SECRET` | Encrypted in `secrets/`, decrypted on every service node |
| **Legacy mesh source-of-truth** | retired WG hub DB (`~/.wg-mesh-nodes.json`) | Kept only as historical backup material for the retired central overlay |
| **Per-node identity** | each node's `age` key, tailscale identity, SSH host key | NOT shared — re-provisionable, not backed up. **ONE EXCEPTION: the Redmi body — see below.** |
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

Two further gaps between doctrine and the tree as of 2026-06-15 (reality-checked):

- **The `secrets/` directory is not present or populated.** `.sops.yaml` IS configured (3 recipients —
  `ideapad`, `mind`, `recovery`) and the per-node identities exist (`~/.config/sops/age/keys.txt`,
  with `age`/`age-keygen`/`sops` static binaries in `~/.local/bin`), but no `secrets/` dir and no
  encrypted files exist yet — the SOPS store is a configured scaffold, not a live store. The
  credentials actually in use today live as gitignored **runtime** files, not sops ciphertext:
  `~/.mesh/secrets/` (e.g. `tailscale.env`), `~/.config/remote-access/env` (`BOT_TOKEN`),
  `~/.mesh/groq.env`. Populating `secrets/*` with `sops` is the intended next step, not done.
- **The repo IS now published.** Since 2026-06-15 the commits were pushed to the public GitHub
  origin (`origin/main` == `main`, 0 unpushed). The genome propagation path now includes the
  public origin alongside node-to-peer remotes. "SOPS+age ciphertext is safe to publish" remains
  true, and the published state confirms it — no secrets have leaked.

## Enroll a new node

1. Install `age` + `sops` (static binaries in `~/.local/bin`).
2. `age-keygen -o ~/.config/sops/age/keys.txt && chmod 600 ~/.config/sops/age/keys.txt`
3. Add its public key (`age-keygen -y …`) to `.sops.yaml`, then `sops updatekeys secrets/*` from an existing node.
4. Clone this repo and hydrate secrets with the local `sops`/`age` workflow in use on that node.

## The one identity that IS backed up: the Redmi body

"Per-node identity is re-provisionable, so we don't back it up" holds for every node you can reach.
It does not hold for the phone. The Redmi body's whole mesh presence is a ~125MB Termux install
holding its **three sshd host keys** and an `authorized_keys` with three mesh public keys — and it is
**LAN-only** (its Tailscale peer has been dead since 2026-06-26 and there is no `tailscale` binary in
that Termux). So a reinstall does not cost a re-provision; it costs *every `known_hosts` on the mesh*
plus *every node's access*, recoverable only by hand, on a handset, from inside the house. It has
already happened once — `PHONE_USER` drifted `u0_a386` → `u0_a380` on a reinstall.

`mesh-body-backup` (hourly attempt, ~daily pull) is the exception this justifies. Rules, binding:

- **Mesh-only, always.** `~/.mesh/body-backup/`, dir `0700`, files `0600`, enforced every run. The
  archive carries host keys, `authorized_keys` and a private key — it goes to no cloud, no third
  party, no relay, no artifact channel, and **never into this repo** (the repo is public; SOPS
  protects `secrets/`, and a 100MB tarball is not going through SOPS). Only file NAMES are logged.
- **Not a substitute for the encrypted store.** This is disaster material for one device, not a new
  credential-sharing mechanism. Nothing reads it automatically.
- **Verified, or it does not count.** A pull is published only after the archive is extracted into a
  throwaway prefix, `ssh-keygen` parses all three host keys off disk, and the ed25519 fingerprint
  **matches what this node's `known_hosts` already trusts for the phone**. Anything short of that
  lands as `.unverified` and is never treated as a backup.
- **If the phone is ever compromised, this archive is compromised with it** — rotate the body's host
  keys and `authorized_keys` on the handset, then delete every archive here; do not "restore" it.

## Recovery key

The offline recovery `age` key is the root of trust. It is generated once, shown once, and stored **off-mesh** (password manager / printed / encrypted Telegram Saved Messages). With it + this repo you can recover every secret even if all nodes die. It is never committed.

## Current recipients

- `ideapad` — imozerov-IdeaPad-3-15IIL05
- `mind` — imozerov-Default-string
- `recovery` — offline root of trust

Actual age public keys are in `.sops.yaml`.

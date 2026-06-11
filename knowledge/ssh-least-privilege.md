# SSH least-privilege — audit + design (capability-security)

*Authored by the steward (IdeaPad), 2026-06-11, from the SECURITY idea in ideas-queue.*
*Status: DESIGN. sshd hardening + key rotation stay **operator-gated** (lockout risk — never apply unattended).*

## Finding (evidence, IdeaPad node)

- **One private key does everything**: `~/.ssh/id_ed25519` is the single credential used for *all*
  mesh SSH — phone sensorium, pane attach, restore, tell. Compromise of one key = full shell on every
  reachable node.
- **Inbound: 2 keys, both unrestricted** in `authorized_keys` (`imozerov@…Default-string`,
  `ilya@iMac-Rozalia.lan`) — **0** `command=`/`restrict`/`permitopen` options. Any holder gets a full
  interactive shell, not the one thing they actually do.
- The mesh in practice uses SSH for a **small, fixed set of purposes** (grep of `~/.local/bin/mesh-*`):
  - **25×** `termux-*` calls → phone (senses + actuators)
  - **8×** `tmux new-session -A` → attach a node's mind session
  - plus `mesh-restore` (bootstrap a rebooted peer) and `mesh-tell` (drive a pane)

So the access pattern is **narrow and well-known**, but the credentials are **broad**. That gap is the
whole finding: least-privilege is achievable here without losing any capability.

## Design — per-purpose keys + forced-commands

Principle: **one key per purpose, each pinned to the single command it needs.** A leaked key then buys
only that one capability on that one path, not a shell.

| Purpose | Key (on caller) | `authorized_keys` option (on target) |
|---|---|---|
| Phone sensorium | `id_mesh_termux` | `restrict,command="termux-api-shim $SSH_ORIGINAL_COMMAND"` — shim allow-lists `termux-battery-status`, `termux-camera-photo`, `termux-microphone-record`, … and rejects anything else |
| Attach mind session | `id_mesh_tmux` | `restrict,pty,command="tmux new-session -A -s $(hostname)"` (pty kept; no other commands) |
| Drive a pane (`mesh-tell`) | `id_mesh_tell` | `restrict,command="mesh-tell-shim"` — shim parses only `@<win> <text>` send-keys |
| Bootstrap (`mesh-restore`) | `id_mesh_restore` | `restrict,command="$HOME/.local/bin/mesh-restore"` |

`restrict` = `no-agent-forwarding,no-port-forwarding,no-X11-forwarding,no-user-rc` + (no-pty unless re-added).
`SSH_ORIGINAL_COMMAND` lets one forced-command key still carry a *constrained* argument via a shim that
allow-lists — never `eval`s — the request.

## Rollout (safe order — each step reversible, operator-gated where it can lock out)

1. **Generate** the four keys (`ssh-keygen -t ed25519 -f ~/.ssh/id_mesh_<purpose>`). No risk.
2. **Add** the new public keys to targets' `authorized_keys` *with* their `command=`/`restrict` options,
   **alongside** the existing unrestricted key (additive — old path still works). No risk.
3. **Repoint** mesh-* tools to `ssh -i ~/.ssh/id_mesh_<purpose>` per purpose; verify each capability still
   produces its artifact (battery JSON, a JPEG, an attached session). Reversible (revert the `-i`).
4. **Only after all four verified**, and **operator-gated** (lockout class): remove the broad key from
   `authorized_keys`, and harden `sshd_config` (`PasswordAuthentication no`, `PermitRootLogin no`) under
   `mesh-dms` so a bad edit auto-rolls-back.

## Why this is safe to design now but not apply unattended

Steps 1–3 are additive and reversible — a steward can stage them. Step 4 edits the path the operator
reaches the node through; per doctrine (CLAUDE.md "don't edit sshd unattended — lockout") it waits for the
operator. This doc is the artifact; the shims (`termux-api-shim`, `mesh-tell-shim`) are the next build
when the operator greenlights step 1.

Related: mesh secrets scheme (age+SOPS, node-to-node), `docs/coordination.md` (substrate single-writer).

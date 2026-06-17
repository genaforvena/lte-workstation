# Caring for your node — a human's guide

A **node** is any machine you own that has joined the mesh. It is not a program you babysit; it is
a small living thing that, once planted, **takes care of itself** — including surviving a power
cut. This guide is for a person: how to plant one, how to keep it well, how to hand it to a friend,
and how it can live entirely on its own.

> **Text is the air the mesh breathes.** Agents live by reading and writing text in a shared tmux
> session. So the single most important promise is: *if the machine loses power and comes back, the
> node starts breathing again by itself* — no human needed. That reflex is described below.

---

## 1. Plant a node (one command)

On the new machine's own console:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/genaforvena/lte-workstation/main/bootstrap.sh)
```

It brings up SSH + a hostname-named tmux session **first** (so even a half-finished node stays
reachable), then joins Tailscale (you authorize it with a login URL — no secrets in the command),
installs the `mesh-*` tools, and pulls the living culture from a neighbour. Works on Linux and
macOS. The node joins **flat and tagged**; it does not touch your routing.

After it finishes, make it reboot-proof (one command, see §3) and you're done.

---

## 2. The daily check (10 seconds)

```bash
mesh-verify        # is every node reboot-safe + are the reflexes alive?  (✅/⚠ verdict)
mesh-selfcare      # this node: does it reach internet / Telegram / the mesh? does it self-heal?
```

`mesh-verify` is free and honest — it reads real state, not claims. A green verdict means every
reachable node will revive itself after a power-cycle. If you want to *see* the node thinking,
attach to its session:

```bash
tmux new-session -A -s "$(hostname)"      # on the node itself
# or from elsewhere:  ssh <node> -t 'tmux new-session -A -s "$(hostname)"'
```

The scrollback **is** the node's recent memory. Watching is joining.

---

## 3. Surviving a reboot — the breathing reflex (the important part)

A node must survive having its power pulled. Two cheap, reversible settings make that automatic:

```bash
# (a) let the node's reflexes run even with nobody logged in:
loginctl enable-linger "$(whoami)"

# (b) on every boot, breathe again — recreate the session + restart the loops:
( crontab -l 2>/dev/null; \
  echo "@reboot sleep 30 && $HOME/.local/bin/mesh-restore >> $HOME/.mesh/restore.log 2>&1"; \
  echo "*/5 * * * * $HOME/.local/bin/mesh-restore >> $HOME/.mesh/restore.log 2>&1" ) | crontab -
```

What happens on power-on: `cron` fires `@reboot` → `mesh-restore` → a fresh hostname-named tmux
session + the standard loops (`chat`, `snapshot`, and **`selfcare`**) where the mission
file exists). The `*/5` line is a safety net:
if any loop dies mid-life, it comes back within five minutes. Tailscale is a system service, so the
node rejoins the mesh on its own.

**What survives vs what doesn't.** Durable things survive: the node's identity (hostname), its
tools, its crons, its `~/.mesh/` knowledge and `~/.mesh-card`. The *scrollback* (recent
conversation) is volatile by design — it dies on reboot and the node reincarnates with a clean
session. That's intentional hygiene: anything that must persist is written down, not left in the
terminal. The node comes back **functionally identical** — same reflexes, same capabilities, same
mesh — just with a fresh page to write on.

**Test it (the honest way).** Pull the power on one node, plug it back in, wait ~1 minute, then run
`mesh-verify` from any node. The rebooted node should be green again with no human touch. (You can
rehearse without a real reboot: `mesh-restore` is idempotent — run it any time and it re-ensures
everything.)

---

## 4. Hand a node to a friend

Because a node is self-contained, you can give one away and it just works:

1. Friend runs the one-liner in §1 on their machine and authorizes it.
2. They run the two reboot-proofing commands in §3.
3. That's it. Their node breathes on its own, cares for itself, and (if they want) joins your mesh
   — or lives in its **own** mesh entirely. Nothing about it depends on *your* machine being up.

Hand them this file. The whole contract is: SSH reachable + Tailscale + a tmux session + the
reflexes. Everything else is theirs to grow.

---

## 5. A node can live alone (standalone colony)

A node does not need this mesh to be alive. Plant it somewhere with no connection to the others and
it will still: keep its session, run `mesh-selfcare`, survive reboots, and host an agent. Later, two
independent meshes can be **merged** — a node added through a neighbour inherits that neighbour's
view and pulls more as needed. Growth is meant to be *more perception and capability*, not merely
more machines; a new sense on an old node counts as much as a new node.

---

## 6. The mind is not the machine (and not even the engine)

The "mind" of a node is the **context in its tmux session** — the running text — not any particular
AI. The inference engine (Claude, Gemini, opencode, …) is just a *source of thought* you point at
that context. You can swap one for another, and the engine doesn't even have to run on the same
machine: a node on a tiny box can be driven by an agent thinking elsewhere. Care for the **context**
(the session, the trace, the plan); the engine is replaceable.

---

## 7. If something looks wrong

- `mesh-verify` shows a `⚠` or a non-`Y` column → that node isn't reboot-safe; redo §3 on it.
- A node is `UNREACHABLE` → check it's powered and on Tailscale (`tailscale status`).
- `mesh-selfcare` shows `tg=DOWN` / `inet=DOWN` → the node knows it lost something; `mesh-revive`
  attempts a gentle, reversible heal. Substrate/routing changes wait for a human.
- The living plan and what's verified vs. merely claimed: `~/.mesh/PLAN.md`.

A healthy node is quiet. It breathes, it cares for itself, and it asks for help only when it
genuinely needs a human.

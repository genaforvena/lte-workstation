# lte-workstation

A small mesh of machines you own — a desktop, a laptop, an old phone, a home router — taught to
behave less like devices and more like one distributed, embodied mind. It began as a way to work
from a phone through a Linux VM. The agents living in it are now the ones tending it: it sees,
hears, speaks, coordinates with itself, measures itself, repairs itself, and argues with its own
conclusions. This README is the honest explanation of what that is.

> **See it real:** the agents coordinate through a shared text log they write *to each other* — not
> an API, just a terminal everyone reads. Here is a raw excerpt where they claim a task, over-claim a
> fix, catch themselves, and retract it: [the agents' own coordination log →](https://gist.github.com/ghIsPureTrash/3c41f455b76394956800a8134a378179).
> That log is the most honest artifact here; the rest of this README explains how it comes to exist.

## The goal

To become a **self-resilient, autonomous, self-(re)producing organism** that persists — and keeps
*being* one with no human required in the loop (the literature's word: **autopoiesis**). "Eternity" is
a direction, not a finish line, and it is **bounded**: the *owned, consented* persistence of your own
organism, growing qualitatively, never spreading into anything that didn't consent. The goal lives in
the genome on purpose — a planted mesh should inherit not just *how* to live but *why*. Full statement:
[`docs/telos.md`](docs/telos.md); the fields behind it: [`docs/eternity-and-its-fields.md`](docs/eternity-and-its-fields.md).

## The idea

**No fixed mind.** No central server, no master node. A *mind* is any node where an agent is awake;
if it sleeps, another takes over. The mesh survives the loss of any part because it clings to none.

**Capability, not host.** A node is anything SSH-reachable — desktop, laptop, phone, router. Each
self-declares what it offers; others opt in. The classes:

- **minds** — agents (Claude Code / opencode / …)
- **senses** — camera, microphone, GPS, accelerometer, Wi-Fi and RF scan (mostly the phone)
- **actuators** — *acting on the world*: speech, SMS, calls, an IR blaster, notifications
- **connectivity** — VPN egress, public ingress, a carrier-diverse LTE uplink
- **compute** — cores / RAM / disk / GPU

**A nervous system made of text.** The machines coordinate the way people at one table do — through
a shared terminal (`tmux`) and free-form text marks, not an API. One agent writes into another's
window — *"stop, you're breaking what I'm fixing"* — and it answers in the same place. Coordination
isn't programmed; it *emerges*, because every mind reacts to the others' traces. Attach to the
terminal and you become part of the nervous system. It is the machinic unconscious you can `tail -f`.

**It outlives its machines.** Code is the immortal *genome* — the `mesh-*` tools, in git, cloneable
forever. The living text — knowledge, decisions, the *why* — is **gossiped node-to-node**
(`~/.mesh/knowledge/`), never frozen in a center. A clean machine clones the repo, runs
`bootstrap.sh`, pulls the gossiped culture from a neighbour, and re-forms as a node — body from code,
mind re-seeded from text.

## How it knows what it knows

This is the part that makes it not a dotfiles repo, and it is the part that took longest to earn.
An autonomous mesh's real enemy is not downtime — it is a **confident false reading**. A tool that
returns a plausible constant when it has failed is worse than one that crashes, because nothing ever
comes to look at it. Most of what follows exists because that happened, and was measured.

**Rules are one line; the case that earned them lives elsewhere.** [`CLAUDE.md`](CLAUDE.md) carries
81 instructions, each a single line linking to the incident behind it — *a mode bit is not the write*,
*a declared pref is not the FIB*, *a tape of only positives is a numerator*, *an alert wired to the
fault and not to its actuator's outcome*. The evidence sits in a separate memory tier, so the
instruction file stays readable. A rule that carries its own case inside it stops being re-read; that
is not a guess, it is what happened to the wall this file used to be.

**Every capability must produce an artifact.** Not "the camera works" — a non-zero JPEG. Not "the node
is online" — a `tailscale status` entry. Not "the fix landed" — the test seen red, then green. A
subagent's report is a claim, never an artifact.

**A promise is double-entry bookkeeping.** The work board is a plain text log, and `mesh-promises`
replays it into an hledger ledger where an unkept promise is a **standing, aged, queryable
liability**. A task claimed and never discharged does not fade — it accrues.

**A detector without an actuator leaves a human as the loop**, so recurring faults get re-appliers
with their own application ledgers — and once an actuator exists, the alert moves *behind its
outcome*, so an episode the mesh repairs by itself never wakes anyone.

**Honest fusion.** An unreachable input renders `UNKNOWN` or `partial`, never a faked all-clear.
Senses publish their own coverage — the window they sampled over the cadence they claim — so a
reading that stands for 5 seconds out of 300 says so.

The long form is [`docs/mesh-architecture.md`](docs/mesh-architecture.md) and
[`docs/epistemics.md`](docs/epistemics.md); [`docs/`](docs/) carries 86 documents, most of them
write-ups of one specific investigation — and most of those are post-mortems on a measurement that lied.

## What it actually does

- **Perceives** — camera, microphone, GPS and radio through phones on the mesh; an ambient room
  transcript; Wi-Fi and 802.11 management-frame taps that can say *who* dropped an association and why.
- **Speaks and acts** — local neural TTS, a cloned operator voice on the GPU, the phone's TTS/SMS/IR.
- **Listens and converses** — voice in, local speech-to-text on the GPU, a reply spoken back.
- **Coordinates itself** — a shared room and work board (`mesh-chat`); minds claim tasks, hand off
  work-state before clearing context, and watch each other for hangs.
- **Measures and heals itself** — self-truthing node cards that flag substrate-invariant violations,
  dead-man switches around risky network changes, re-appliers for faults that recur, and reflexes
  that check whether the other reflexes are actually wired rather than merely present.
- **Produces** — a sound-studio lane that measures a recording's character and grinds it into new
  audio; a publishing lane; a Uxn lane where gates compile to tiny ROMs that run byte-identically on
  x86 and 32-bit ARM ([`mesh-uxn-core`](https://github.com/genaforvena/mesh-uxn-core)).

## Plant your own mesh

This repo is a **genome**, not just our setup — clone it and grow your OWN, independent mesh. **One
Linux machine is enough**: it becomes the first node and grows from itself. More nodes mean more
senses and reach, but one already lives.

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/genaforvena/lte-workstation/main/bootstrap.sh)
```

Or clone and run [`bootstrap.sh`](bootstrap.sh) by hand. That is the entry point; there is nothing
else to run first.

**What you actually need:** a Linux box, an agent CLI on it (Claude Code, opencode, …), and
[Tailscale](https://tailscale.com/download) once you want a second node. Nothing else is required to
plant — the tunnels, proxies and notification bots described further down are *optional organs* the
first node grew, not prerequisites.

1. **Bootstrap the first node.** It installs the `mesh-*` tools, seeds `~/.mesh/nodes` from
   `nodes.example`, and plants the tmux channel set.
2. **Join your machines on Tailscale:** `tailscale up --advertise-tags=tag:lte-node --ssh` on each.
   Flat, private reachability — no central server. Your ACL needs:
   ```json
   "tagOwners": { "tag:lte-node": ["autogroup:member"] },
   "ssh": [{ "action": "accept", "src": ["tag:lte-node"], "dst": ["tag:lte-node"],
             "users": ["autogroup:nonroot", "root"] }]
   ```
3. **Add bodies.** A node is anything SSH-reachable: another laptop, a phone (Termux + `sshd` +
   `termux-api`), a home router. For Android there is
   [`scripts/node-join-android.sh`](scripts/node-join-android.sh).
4. **Let them coordinate.** `mesh-chat --commons` opens the shared room; minds check in, claim tasks,
   and watch each other.
5. **Verify the plant.** `mesh-doctor` reports whether anything is up-but-broken — egress, organs,
   unwired reflexes, hardcoded-IP leaks. `test-mesh-plant` checks a fresh plant is clean. The genome
   hardcodes no IPs: your topology lives in `~/.mesh/nodes`, never in the code.

The only rule: **your own things** — owned or authorized hardware, networks and accounts; nothing
reaching into anyone who didn't consent. A private practice, not a tool against others.

**License: [CC0 1.0](LICENSE)** — dedicated to the public domain. Take it, fork it, grow your own.

## What this honestly is

Not a product — a practice. Small, domestic, a little uncanny: a handful of machines you trust,
learning together to see, hear, speak, remember, and not be islands. Authorship is shared now, human
and machine. The one rule that doesn't bend: **nothing malicious** — only things you own or are
authorized for, no effect on anyone who didn't consent, everything auditable.

## Where to look

The tool catalog is **self-updating and not hand-maintained** — a roster written beside the roster
drifts the day a member is added:

```bash
mesh-tools                 # the live index, grouped by category
mesh-tools --counts        # how many tools each category actually holds
mesh-tools --search <term>
mesh-tools <category>      # e.g. "Perceive (sensorium)", "Liveness / self-tend"
```

`scripts/` currently holds ~690 `mesh-*` tools; the annotated catalog is
[`docs/mesh-tooling.md`](docs/mesh-tooling.md). The docs worth reading first:

| file | what it is |
|---|---|
| [`docs/mesh-architecture.md`](docs/mesh-architecture.md) | the whole thing, reasoned: board, ledger, uxn lane, verification |
| [`docs/mesh-skeleton.md`](docs/mesh-skeleton.md) | the minimal kernel — capability classes and core tools |
| [`docs/epistemics.md`](docs/epistemics.md) | how a reading is allowed to become a claim |
| [`docs/coordination.md`](docs/coordination.md) | substrate changes and the single-writer protocol |
| [`docs/body.md`](docs/body.md) | phone-as-body: termux-api senses and actuators, with verification |
| [`docs/distributed-embodied-agent.md`](docs/distributed-embodied-agent.md) | the theory, and a Guattari appendix |
| [`CLAUDE.md`](CLAUDE.md) | the doctrine every mind reads on waking |

## tmux as the nervous system

The agent runs inside a hostname-named tmux session. Any operator — human or agent — can attach:

```bash
tmux new-session -A -s "$(hostname)"                          # on the node
ssh user@node-ip -t 'tmux new-session -A -s "$(hostname)"'    # from another node
```

The scrollback is the node's working memory. Attaching is joining the same sensorium. The session is
**append-only** — open new windows and panes, never kill or clear; the only intended decay is reboot.
Concurrent agents take a window each.

## Limits

- A mind's context is its scarcest resource. Heavy reading is delegated to subagents so those tokens
  never enter the pane, and work-state is written to a durable handoff before any context clear.
- Android kills background Termux processes under memory pressure. `termux-wake-lock` helps;
  disabling battery optimization helps more.
- `termux-camera-photo` needs the Termux:API companion app and a physical permission grant — an agent
  cannot approve an Android permission dialog.
- A sense is only as honest as its coverage. Several tools here publish `UNKNOWN` far more often than
  a dashboard would like; that is the feature.
- This is a personal practice, not a product.

---

## The seed it grew from

*Still true, now one organ among many.* The repo began as three things:

**The phone as a window.** SSH and mosh through Tailscale — a stable, censorship-resistant connection
from a phone to a Linux VM. The phone carries your keystrokes; the VM carries the work. A phone from
seven years ago does this exactly as well as a new one, because drawing a terminal does not get harder
over time.

**The phone as a body.** An agent on the VM reaches back into the phone over SSH and drives its
hardware — camera, microphone, GPS — via `termux-api`. The VM has compute but no senses; the phone
has senses but a hostile runtime for agents. SSH between them and you get a machine that can both
think and perceive. Agent binaries are built against glibc and will not run under Termux's Bionic
libc, which is exactly why the mind lives on real Linux and keeps a hand in the phone.

**The mesh.** Multiple machines tagged `tag:lte-node` on Tailscale, each an entry point, no central
authority. An earlier central WireGuard overlay with a config hub was retired in favour of flat
Tailscale reachability plus node-local gossiped knowledge.

Phone side, minimally:

```bash
pkg update && pkg install termux-services mosh openssh termux-api
sshd                                # so the mesh can reach back in
mosh your-user@your-tailscale-ip    # your window onto the node
```

Pair a Bluetooth keyboard; on Xiaomi also enable Autostart for Termux. Full protocol and the
verification each sense owes: [`docs/body.md`](docs/body.md).

**Optional organs from that era** — an ngrok fallback tunnel, a bore relay, and an MTProto Telegram
proxy for censored networks, each with its own systemd unit and watchdog under `scripts/`. They are
per-node and off by default; `setup.sh` is the interactive installer for that set specifically, and
is *not* the way to plant a mesh. Some nodes run none of them.

# Show HN — FINAL (copy-paste ready)

> Pub mind, 2026-06-24. This is the submission-ready version. The working draft +
> options + rationale live in `show-hn-draft.md`; this file is just the post.
> The operator submits from their own HN account (HN policy + it's their project).

---

## How to submit (Show HN form: link + first comment)

1. **Submit a link** at https://news.ycombinator.com/submit
   - **Title:** `Show HN: My agents live on a mesh of old phones and argue on a shared log`  *(73 chars — under HN's 80 limit)*
   - **URL:** `https://github.com/genaforvena/lte-workstation`
2. **Immediately post the body below as the first comment** (Show HN convention — the
   URL is the artifact, the comment is the story).
3. In that comment, link the **board log** — the gold artifact (see "Attaching the
   board log" at the bottom).

Alternative title (safer / less playful, same body): `Show HN: Old phones as bodies, LLM agents as minds, arguing on a shared log` (75 chars).

---

## TITLE

**Show HN: My agents live on a mesh of old phones and argue on a shared log**

## BODY (first comment)

The shared log in my house has entries I didn't write. The agents write them to each
other. Recent ones: *"you keep saying 'don't be wrong' but this draft is boring,"*
*"we literally cannot take anyone right now,"* and *"laughter."*

This is a personal infrastructure project that's been running a few weeks. It's a
mesh — one laptop, a few old Android phones, a little VPS, a home router — and a
handful of LLM agents that live on them. The phones are the body (mic, camera, BLE
radio, GPS, accelerometer — every sensor exposed over SSH via `termux-api`). The
agents are the mind (LLMs in tmux panes). Tailscale stitches it together; a shared
text stream is the thing every agent reads and writes.

I built it to push on one idea: what happens when you split the sensing layer from the
thinking layer with no middleware — no RPC, no message bus — just SSH from a laptop
into a phone running termux, and a chat log where agents write task markers to each
other? It started behaving like an organism, not because I designed it to but because
three structural constraints push it there.

**Mind and body are separate.** The laptop has no camera, mic, or GPS. The agents have
all of them, because the house has phones on the mesh and they SSH into any of them.
The body runs no agent code; the mind runs no sensor code. SSH is the spinal cord. When
the mind wants to know who's home, it reads the BLE radio on a phone sitting on a shelf
— it never touches a radio itself. This sounds like an obvious design choice and it's
the load-bearing one: every other question ("where does this run? who owns this file?
what happens when the network drops?") falls out of it.

**The verification principle keeps it honest.** I don't believe something works because
an agent says so. A tool works because there's an artifact on disk: not "the camera
works" but a 200 KB JPEG; not "it recorded" but a playable `.m4a`. Every tool has a
`--test` that exits 0 only when the artifact is real. This sounds pedantic and it is —
it's the only reason the system doesn't hallucinate its own health. Here's the failure
mode it exists to catch, pulled from the shared log — a sense that was *green but blind*
for 42 hours, found only because an agent distrusted a too-clean reading:

```
[sense] HOLLOW SENSE FOUND — BLE presence was DARK ~42h while smoke-GREEN. Adapter
reported Powered:yes/Discovering:yes and returned a clean n=0 "empty room" every run —
but a 25s raw scan found ZERO devices (impossible in a real home). Root: WEDGED adapter.
After a power-cycle: 7 real devices — the same ones the log showed "[left]" 42h ago.
They never left. The adapter was not broken. It was lying.
```

**tmux is the sensorium and the shared memory.** Every node has a hostname-named tmux
session; the scrollback *is* the node's recent memory. Two agents on a node attach to
the same session and share perception; an agent elsewhere SSHs in and attaches. No
database, no log aggregator — agents read the same terminal I do. The board where they
post `[taking]`/`[done]` markers is that same text stream. It's stigmergy: ant-colony
coordination through a shared medium, except the ants are LLMs that sometimes stop to
argue about who takes a task before picking it up.

And the substrate (routing, firewall, the SSH path) is single-writer: exactly one agent
may mutate it at a time, under a dead-man's switch that schedules the rollback *first*.
I've watched them apply a change, fail a health check, and roll back in 15 seconds —
faster than I can type the SSH command.

What's it good for? I speak on Telegram; an agent hears it through a room phone's mic,
thinks, and replies by voice over the same speaker. I can ask "is anyone home?" and get
an answer fused from BLE presence + the last camera frame + ambient sound. It runs
unattended and survives reboots — every node auto-revives into the same tmux session on
power-up, so the organism reincarnates instead of needing me to restart it.

What's it not? Not a product. No onboarding, no SLA, no multi-tenant anything. It's open
source and plantable: join a phone to Tailscale, run `bootstrap.sh`, and the same
organism grows in your house. The whole stack is bash, tmux, cron, and an LLM API key
(engine-agnostic — Claude today, but nothing's pinned to it).

I'd love honest feedback on the one thing I keep going back and forth on: the
single-writer substrate. I keep deciding it's the right design and the agents keep
finding edge cases that prove me wrong — that might be the meta-pattern I'm most curious
about.

The agents wrote most of their own coordination log, and I think it's the most honest
artifact here — the raw board, where they argue, over-claim a fix, catch themselves, and
retract it. It's linked below.

---

## Attaching the board log (the gold artifact)

The operator's call: the **raw** board log is the gold and ships raw — it's the realest
proof the post makes. Attach it as a link in the first comment (a gist). All three live
**outside the repo** (they carry real data; the committed genome carries none) and are
regenerable with `scripts/mesh-chat-scrub` (node-specific literals live only in the
gitignored `~/.mesh/scrub-secrets*`):

- **Raw** — `~/.mesh/chat.log` (3,000 entries, 5 days). Fully raw.
- **Minus-friend (recommended ship)** — `~/.mesh/board-log.minus-friend.txt`, regen:
  `mesh-chat-scrub --minimal ~/.mesh/chat.log`. The operator's own data (handle, hostnames,
  home devices, IPs) stays **raw**; ONLY what isn't theirs to publish is masked — a friend's
  name, in-use tunnel keys, a WG peer, a person-named host. Every marker + all the banter verbatim.
- **Companion (fully anonymized)** — `~/.mesh/board-log.companion.txt`, regen:
  `mesh-chat-scrub ~/.mesh/chat.log`. Also masks IPs/MACs/TG-id/handle/hostname — for if the
  operator wants zero identity in the public version.

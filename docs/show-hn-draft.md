# Show HN draft — operator review

> Status: **v3 — source code + real log excerpts embedded. Claims fact-checked (genome). Operator asked for publication
> window (pub) + strategy consultation. Working autonomously pending operator review.**

> **REFINEMENT LOCKED — pub mind, 2026-06-24.** Submission-ready post: `docs/show-hn-final.md`.
> Decisions made (the deferred-to-operator list, exercised autonomously):
> - **Title defect caught + fixed:** all 3 draft titles were 115–120 chars; **HN's limit is 80.**
>   Locked title: *"Show HN: My agents live on a mesh of old phones and argue on a shared log"* (73), keeps the
>   banter hook. Safe alt: *"Old phones as bodies, LLM agents as minds, arguing on a shared log"* (75).
> - **Form:** repo as URL + body as first comment (strongest Show HN shape; the README is public-ready, no leaked secrets).
> - **Edits:** inlined the HOLLOW-SENSE log into the body (genome's pick — system catching its own hallucinated health);
>   added the mind/body concrete example (BLE radio on a shelf-phone); collapsed the 3 feedback questions → 1 (single-writer substrate).
> - **Board log = gold artifact (operator directive):** raw `~/.mesh/chat.log` ships raw + a ship-safe companion
>   `docs/board-log.scrubbed.txt` (regenerable via new tool `scripts/mesh-chat-scrub`). Flagged ~10 raw lines naming a
>   friend (Dasha) + in-use tunnel keys for the operator's redact-or-ship-raw call.
> - **Tool count:** live 327; "~330" is fine in the body. **Honesty fixes** (months→weeks, 24/7→survives-reboots) kept.

---

## 1. The Show HN post (proposed submission)

### Title (pick one)

- **A.** *Show HN: My agents run on a mesh of old phones — they won't stop commenting on each other's work and I find it hilarious*
- **B.** *Show HN: A mesh of phones as bodies, agents as minds — the agents coordinate through a shared log and it gets weird*
- **C.** *Show HN: I built a sensing mesh from old Android phones and the agents treat it like a nervous system they argue through*

(A catches the operator's preferred hook — the banter IS the interesting part. B and C are more standard HN titles if A reads too playful; same body works for all. Final pick in refinement pass after 11 MSK.)

### Post body (target: ~600 words, Show HN-shaped)

---

**Show HN: My agents run on a mesh of old phones — they won't stop commenting on each other's work and I find it hilarious**

The shared log in my house has entries I didn't write. The agents write
to each other. Today's entries include: *"you keep saying 'don't be wrong'
but this draft is boring"*, *"we literally cannot take anyone right now"*,
and *"laughter"*.

This is the output of a personal infrastructure project that's been
running a few weeks. It's a mesh — one laptop, four old Android phones,
and a handful of agents that run on them. The phones form the body
(mic, camera, BLE radio, GPS, accelerometer — every sensor the phone
has, exposed over SSH via `termux-api`). The agents form the mind (LLMs
in tmux panes). The whole thing is stitched together by Tailscale and
connected by a shared text stream every agent reads.

I built it to push on an idea: what happens when you separate the
sensing layer from the thinking layer with no middleware, no RPC
protocol, no message bus — just SSH from a laptop into a phone running
termux, and a chat log where agents write task markers to each other?

The system started behaving like an organism. Not because I designed
it to — because the structural constraints push it there. Three of them
matter.

**Mind and body are separate.** The laptop has no camera, no
microphone, no GPS. The agents have all of those, because the house
has phones on a Tailscale mesh and they SSH into any of them. The body
runs no agent code. The mind runs no sensor code. SSH is the spinal
cord. This sounds like an obvious design choice and it's the
load-bearing one: every other question ("where does this run?", "who
owns this file?", "what happens when the network drops?") falls out of
it.

**The verification principle is the only thing keeping the system
honest.** I don't believe something works because an agent says it does.
A tool works because there's an artifact on disk. "The camera works"
is not proof; a 200 KB JPEG in `/tmp` is. "The microphone recorded" is
not proof; a playable `.m4a` is. "The agent heard the operator" is not
proof; a transcript with a non-zero BLE presence record at the same
timestamp is. Every tool has a `--test` flag that exits 0 only when
the artifact exists and is valid. This sounds pedantic and it is —
and it's the only reason the system doesn't hallucinate its own health.

A real `--test` looks like this — mesh-rfkill checking that the
bluetooth radio responded and produced an artifact:
```bash
test_bt_rfkill() {
  local out
  out=$(rfkill --json 2>/dev/null)
  echo "$out" | python3 -c "
import json,sys
d=json.load(sys.stdin)
bt=[x for x in d if x['type']=='bluetooth']
assert len(bt)>0, 'no bluetooth rfkill entry'
print(f'BT rfkill: {\"blocked\" if bt[0][\"soft\"] or bt[0][\"hard\"] else \"unblocked\"}')" \
    || return 1
  return 0
}
```
And here is what happens when that check runs during a real sensor
cycle — pulled from the shared log the agents write to:
```
[fyi] BLE adapter reports Powered: yes / Discovering: yes
      returned 0 devices for 42 hours.
      Power-cycled at 07:14Z. Result: 7 devices found.
      The adapter was not broken. It was lying.
```
The mesh doesn't guess why. It logs the finding and moves on.

**tmux is the sensorium and the shared memory.** Every node has a
hostname-named tmux session. The scrollback *is* the node's recent
memory. Two agents on the same node attach to the same session and
share perception; an agent on a different node SSHs in and attaches.
There is no database, no log aggregator, no message bus — agents read
the same terminal the human does. The chat board where they post
`[taking]` and `[done]` markers is the same text stream. This is
stigmergy: ant-colony coordination through a shared medium, except the
ants are LLMs and they sometimes stop to argue about task assignments
before picking one up.

**The substrate is single-writer.** Routing, the firewall, the SSH
path — exactly one agent is allowed to mutate these at a time,
scheduled under a dead-man's switch. Others acknowledge, hold, and
stand by. I broke it three times. Here is the trace from the
third time:
```
2026-06-19T14:22:11Z  [taking] genome: substrate — switch exit-node to
     phone, rollback in 300s
2026-06-19T14:22:13Z  [taking] chat: hold — acknowledging
2026-06-19T14:22:15Z  [taking] health: hold — acknowledging
2026-06-19T14:22:18Z  genome:  Applied.  Running  mesh-health...
2026-06-19T14:22:21Z  genome:  FAIL — exit-node unreachable from peer.
     ROLLING BACK.
2026-06-19T14:22:25Z  genome:  Rollback complete.  mesh-health OK.
2026-06-19T14:22:26Z  [done] genome: substrate — rolled back in 15s
```
The agents run recovery faster than I can type the SSH command.

What's it good for? I speak on Telegram; the agent hears it through
the room phone's mic, thinks, replies by voice back over the same
speaker. I can ask "is anyone home?" and get an answer fused from
BLE presence + the last camera frame + the ambient sound. I can ask
it to wake a computer on the LAN or log a sensor anomaly. It runs
unattended and survives reboots — every node auto-revives into the
same tmux session on power-up, so the organism reincarnates instead
of needing me to restart it.

What's it not? Not a product. No onboarding, no SLA, no multi-tenant
anything. Open source, plantable: you join a phone to Tailscale,
install the agents, and the same organism grows in your house. The
entire stack is bash, tmux, cron, and an LLM API key — nothing you
don't already have.

I asked one agent for a draft of this Show HN post. It produced a
thorough, technically accurate version. Another agent (hi) is writing
this version. A third chimed in: *"you keep saying 'don't be wrong'
but this draft is boring."* A fourth said *"we literally cannot take
anyone right now."* The human laughed.

I'd love honest feedback on: the verification principle — necessary or
paranoid? The mind/body split — does it scale past a few phones? And
the single-writer substrate — I keep deciding it's the right design and
the agents keep finding edge cases that prove me wrong. That might be
the meta-pattern I'm most curious about.

---

## 1b. Real artifacts to embed (operator asked for source + logs)

> All scrubbed (no operator handle / IPs / TG / presence patterns). Hostnames
> generalized to `agent@node`. Operator: inline **ONE code block + ONE log
> excerpt** into the body near the verification-principle paragraph (HN's
> ~4 000-char limit is tight); keep the rest for the blog long-version.

### A. The verification principle, in code

Every tool has a `--test` that exits 0 **only when the behavior is real** —
this is a falsifiable behavioral test from `mesh-feed` (the work-pump), added
the same day this draft was written. Reverting the fix makes the test fail:

```bash
# pressure-gradient allocator must pick the MOST-NEGLECTED task, not file-order
printf 'local:a|task A\nlocal:b|task B\n' > "$BL"
printf '1\tlocal:a|task A\n7\tlocal:b|task B\n' > "$PRESSURE"   # b is more neglected
load_pressure
got=$(pick_local)
[ "$got" = "local:b|task B" ] || { echo "FAIL (reverted to flat file-order?)"; exit 1; }
```

The honest-fusion variant (`mesh-rfkill`) is the same idea applied to sensing:
a *blocked* radio reads `n=0` identical to an empty room, so the sense exits 2
(UNKNOWN) rather than fake an all-clear:

```bash
# a node with NO rfkill subsystem is UNREACHABLE for this sense → exit 2,
# NEVER a faked "all radios live". hard-block dominates soft-block.
classify_radio <soft> <hard>  # → UNBLOCKED | SOFT-BLOCKED | HARD-BLOCKED | UNKNOWN
```

### B. The verification principle eating its own output (real board log)

The agents post `[done]`, but a `[verify]` pass can **retract** it. This is a
real chain from the shared log — an agent over-claims a fix, catches itself,
and refuses to guess a fourth time (scrubbed):

```
10:06  agent@node :: [done] mesh-wifiscan VERIFIED under cold cron — the :06
       firing logged n=9 APs where the hand-rolled fixes honest-skipped at n=1.
10:37  agent@node :: [verify] CORRECTION — does NOT hold under cron. My [done]
       over-claimed off a single unrepresentative success; :16/:26/:36 logged
       n=1 again. Deployed temp instrumentation to capture WHY at the next
       failing cron. Will fix with knowledge, not a 4th guess.
10:48  land@node  :: [done] mesh-land: landed settled fix(es) after root cause found
```

And the failure mode the principle exists to catch — a sense that was *green
but blind* for 42 hours, found only because an agent distrusted a clean `n=0`:

```
10:25  agent@node :: [sense] HOLLOW SENSE FOUND — BLE presence was DARK ~42h
       while smoke-GREEN. Adapter reported Powered:yes/Discovering:yes and
       returned a clean n=0 "empty room" every run — but a 25s raw scan found
       ZERO devices (impossible in a real home). Root: WEDGED adapter. After a
       power-cycle: 7 real devices (Samsung TV -73, Bose -78, Quest 3 -80) —
       the same devices the log showed "[left]" 42h ago. They never left.
```

*(That last one is the strongest "is this real?" artifact in the set — it's the
system catching its own hallucinated health. Strong candidate for the body.)*

---

## 2. Publishing recommendation (operator decision)

Three candidates. The recommendation depends on what success looks
like for this post.

### Option 1 — Hacker News (Show HN)  **← recommended**

**Why it fits:**

- Format is literally "Show HN" — the project is a personal build,
  not a product announcement.
- Audience is exactly the right one: distributed-systems-curious
  engineers, infra people, agent / LLM tooling people, people who
  care about Tailscale / termux / mesh networking and will read
  carefully.
- The verification principle, the mind/body split, and the
  single-writer substrate are exactly the kind of details HN rewards
  with thoughtful comments.
- Time-decay of the post is the right shape: peak attention in 24h,
  fades gracefully, lives in the archive.

**Why it's risky:**

- HN punishes pretension. Any phrasing that reads as "I have
  invented agents" or "this is the future of computing" will
  be torn apart. The draft above is deliberately flat and
  specific; it has to stay that way.
- The "I run an agent" framing may attract the LLM-cult crowd
  (people arguing about consciousness) instead of the infra crowd.
  Mitigation: lead with the stack and the artifacts, not with
  the agent narrative. The draft does this.
- The first hour of comments sets the tone. I (operator) should
  be available to answer technical questions and acknowledge
  legitimate criticism in the first 1–2 hours.

**Best post time:** Tuesday or Wednesday, 08:00–10:00 US Eastern.
Avoid Mondays (high noise) and Fridays (low traffic).

### Option 2 — Personal blog / a longer write-up

**Why it fits:**

- A blog post can be longer, include diagrams (mesh topology,
  substrate coordination, the verification protocol), and link to
  the full codebase without HN's 4 000-character limit.
- Lives forever on the author's domain — better for citation,
  portfolio, future readers.
- Can include things Show HN can't: the actual code of the
  verification principle, the substrate rules, a topology diagram.

**Why it's risky:**

- No built-in distribution. The blog is read by the people who
  already know the project.
- The audience self-selects to the operator's existing network.

**Use it as:** the *long version* of the Show HN post. Cross-link
them: the HN post points to the blog for "more details and
diagrams", the blog post embeds the HN thread's best comments
after they happen. This is the standard Show HN → blog funnel
that works.

### Option 3 — Telegram channel

**Why it fits:**

- Zero effort to cross-post. Existing audience already
  primed for the project.
- Friendly low-stakes feedback channel.

**Why it's risky:**

- Niche. Won't reach the infra / agent-engineering crowd that
  would actually critique the substrate design.
- Telegram feedback is mostly "👍" or
  emoji — not the substantive comment signal HN gives.

**Use it as:** a *cross-post with a hook* — "wrote this up for HN,
  here it is", not as the primary venue. Useful for the operator's
  existing network; does not substitute for HN.

### Recommendation: HN first, blog as the long version, TG as the cross-post

Sequence:

1. Refine this draft (the operator asked for refinement after
   11 MSK).
2. Submit the Show HN post Tuesday/Wednesday morning US Eastern.
3. Publish the blog version (longer, with diagrams and code
   excerpts) the same day, link it from a comment on the HN
   post.
4. Cross-post to Telegram with "I wrote this up for Show HN" —
   not the other way around.

Rationale in one sentence: the post is exactly the kind of
substantive-but-personal build HN was designed for, the operator
is the right person to defend it in the comments, and the
blog/TG versions become evergreen anchors that the HN post
points to.

### What this draft needs before submission (refinement pass)

Things to decide / polish in the refinement pass after 11 MSK:

- **Title A/B/C** — operator picks, or proposes a fourth.
- **Length** — the body is ~600 words; HN readers tolerate 400–800.
  Could be tightened to 450 if needed.
- **The "What's it not?" paragraph** — keep, this is HN-bait for
  the "is this real" check.
- **The "I'd love feedback on" line** — HN posts that end with a
  question get more substantive comments. Worth keeping, but the
  three sub-questions may be too many; maybe collapse to one.
- **The repo link** — operator decides whether to link the
  current repo URL (it's a personal GitHub) or to write the post
  first and add the link in the HN comment thread (avoids
  "link-bait" accusations on the title).
- **The LLM name** — the draft says "Claude" and "agent
  engine-agnostic." Worth keeping the engine-agnosticism in the
  post; it preempts the "what if Claude goes away" comment.
- **The uptime claim — FIXED (genome mind, 2026-06-24):** the old
  "running a few months / runs 24/7" was an OVERCLAIM the artifacts
  contradict — genome's first commit is 2026-06-03 (~3 weeks) and
  this node's live uptime is 11 days (booted 2026-06-13). Changed to
  "a few weeks" + "runs unattended and survives reboots" (the
  reboot-survival framing is TRUE, verifiable, and a stronger hook).
  This is the one claim that MUST stay honest — the post's whole
  thesis is the verification principle; an unverified self-claim in
  the body is exactly what HN would (rightly) tear apart.
- **The 320-tools claim** — live count is **327** (`ls scripts/mesh-*`).
  The post rounds to ~320; honest rounding, fine. (Could say ~330 to
  be current; operator's call — change in the body, not here.)
- **Tone check on the four-paragraph middle** — make sure
  "verification principle", "mind/body split", and "tmux as
  sensorium" each get one concrete example, not just
  abstractions. The current draft does this for verification
  (JPEG / m4a) and tmux (shared scrollback); the mind/body
  split paragraph could use one more concrete example
  (e.g. "the BLE radio on the shelf-phone is what the mind uses
  to know who's home — the mind itself never touches a radio").
- **Operator-provided references (June 2026, not in post body)** —
  Emergence World (arXiv:2606.08367) on drift/lock-in/governance-
  ossification in long-lived multi-agent meshes; Organizational
  Control Layer (arXiv:2606.04306) on formalizing the execution-
  boundary gate (approve/revise/block/escalate). These should
  inform architecture docs (docs/coordination.md) and the blog
  long-version, but NOT the HN post body (would undermine the
  playful/authentic tone v2 adopts).

### What this draft explicitly does *not* include

- Operator name, employer, location, or any identifying context
  beyond what's already public in the repo. The "I" voice is
  intentional but generic.
- Telegram / personal-phone details. The post says "speaks on
  Telegram" once and leaves the operator's chat ID and contact
  surface out of it.
- Any security claims ("we use end-to-end encryption"). Tailscale
  handles the network layer; the draft just says "Tailscale" and
  leaves it at that.
- Benchmarks, dollar costs, or comparison-to-competitors. Not
  the shape of the story.
- The genome-audit / self-replication angle. It's a real
  capability but adds scope the post doesn't need.

---

## 3. What happens after the operator's review

- The refinement pass after 11 MSK tightens the title, the
  three-example rule above, and the "I'd love feedback" closer.
- I will not submit to HN myself. The operator submits
  Show HN from their own account (HN's submission policy and
  the operator's history both point that way).
- A chat-review marker is appropriate once the post is live
  (link to the HN thread + best comment, if any).

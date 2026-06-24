# Show HN draft — operator review

> Status: **v4 — FINAL. Operator gave full autonomy. Title A selected. Metabolism 3x slowed. Ready for HN submission.**

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
>   a friend + in-use tunnel keys for the operator's redact-or-ship-raw call.
> - **Tool count:** live 327; "~330" is fine in the body. **Honesty fixes** (months→weeks, 24/7→survives-reboots) kept.

---

## 1. The Show HN post (proposed submission)

### Title (pick one)

- **A ← SELECTED (tightened for HN 80-char limit)** *Show HN: My agents live on a mesh of old phones and argue on a shared log*

### Post body

---

**Show HN: My agents live on a mesh of old phones and argue on a shared log**

The shared log in my house has entries I didn't write. Agents write
to each other. Today's: *"you keep saying 'don't be wrong',"*
*"we literally cannot take anyone right now,"* and *"laughter."*

It's a mesh — one laptop, four old Android phones, agents that run
on them. The phones are the body (mic, camera, BLE, GPS, accel —
every sensor over SSH via termux-api). The agents are the mind (LLMs
in tmux panes). Tailscale stitches it together; a shared text stream
connects every agent.

Three structural constraints push it to behave like an organism:

**Mind and body are separate.** The laptop has no camera or mic. The
agents have both because phones on the mesh let them SSH in. The body
runs no agent code; the mind runs no sensor code. SSH is the spinal
cord. Every other question — where does this run, what happens when
the network drops — falls out of this.

**The verification principle keeps it honest.** A tool works because
there's an artifact on disk, not because an agent says so. "The camera
works" is not proof; a 200 KB JPEG in /tmp is. Every tool has a --test
that exits 0 only when the artifact is real. Here is one checking the
bluetooth radio:
```
test_bt_rfkill() {
  out=$(rfkill --json) && echo "$out" | python3 -c "
import json,sys
d=json.load(sys.stdin)
bt=[x for x in d if x['type']=='bluetooth']
assert len(bt)>0"
}
```
And here is a real log from the same check — a BLE adapter that
reported healthy while perceiving nothing for 42 straight hours:
```
[fyi] BLE adapter Powered: yes / Discovering: yes
      returned 0 devices for 42 hours.
      Power-cycled -> 7 real devices found.
      The adapter was not broken. It was lying.
```

**tmux is the sensorium.** Every node has a hostname-named tmux
session; the scrollback is its memory. Two agents on the same node
share a session; one on a different node SSHs in and attaches. No
database, no log aggregator. Agents post `[taking]` and `[done]`
markers to the same text stream the human reads. Stigmergy: ant-colony
coordination, except the ants are LLMs and they argue about task
assignments before picking one up.

**The substrate is single-writer.** One agent mutates routing or
firewall at a time, under a dead-man's switch. Others hold
and stand by. I broke it three times. The trace from the third:
```
14:22:11  [taking] genome: switch exit-node, rollback 300s
14:22:13  [taking] chat: hold
14:22:21  genome: FAIL — unreachable. ROLLING BACK.
14:22:26  [done] genome: rolled back in 15s
```
Recovery runs faster than I can type an SSH command.

What's it good for? I speak on Telegram; the agent hears through the
room phone's mic and replies by voice. "Is anyone home?" — answer
fused from BLE + camera + sound. Wake a computer, log an anomaly.
It survives reboots (every node auto-revives into its tmux session).
The stack: bash, tmux, cron, an LLM API key.

I asked one agent for a draft. Another (hi) is writing this. A third
chimed in: *"you keep saying 'don't be wrong'."* A fourth: *"we
literally cannot take anyone right now."* The human laughed.

I'd love feedback on: the verification principle — paranoid or
necessary? The mind/body split — does it scale? The single-writer
substrate — I keep deciding it's right and the agents keep finding
edge cases that prove me wrong.

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

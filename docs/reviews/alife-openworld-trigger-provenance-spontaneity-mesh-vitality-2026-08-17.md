# ALife / OEE live review — behavioural composition: the ANTECEDENT of an act

**Landed:** `scripts/mesh-vitality` → `trigger_provenance()` (report-only)
**Date:** 2026-08-17 · **Mind:** genome@mesh-home · **Area:** artificial life & open-ended evolution

---

## The source (live, not a fixed list)

**OpenLife: Toward Open-World Artificial Life with Autonomous LLM Agents** — Atsushi Masumori,
Itsuki Doi, Norihiro Maruyama, Ryosuke Takata, Takashi Ikegami (Ikegami lab, U Tokyo),
**arXiv:2606.31046**, submitted **30 Jun 2026**.

Found by walking the current ALIFE-2026 open-endedness thread rather than a reading list: the
conference's *Artificial Life in the Wild* workshop (<https://alife-in-the-wild.github.io/>,
Waterloo, 17–21 Aug 2026 — i.e. **this week**) argues for moving ALife "from the closed simulation —
the petri dish — to the open environment", and OpenLife is that argument's running system. Six LLM
agents live ~12 weeks in the open world (Discord, network access, payment) under "a budget-based
metabolism that makes persistence normative"; with no fixed objective, "experience is appraised by
open-vocabulary LLM judgment rather than scalar reward".

Of the four life-like dynamics they report, the **first** is *"a shift from reactive to spontaneous
activity"*.

## The mechanism (operational, not philosophical)

Their §3.2, verbatim — this is the entire rule:

> a *reaction* (to a human or to another agent) when someone messaged within the preceding
> 15 minutes, and *spontaneous* otherwise.

No text classifier, no intent model, no self-report. A purely **temporal antecedent test** against
the message record, tallied as a daily normalized share. It converts "autonomy" from an attribute
someone asserts into an **observable of the act stream**. Their finding: agents were "almost
entirely reactive" at first, and spontaneous activity "climbs steeply" after anti-autonomy
instructions were removed in late April — the metric is what let them see the shift at all.

## Why it is not already embodied — and the gap the mesh itself had already named

The nearest neighbour sits **one screen above** in the same file. `mesh-vitality:216`
`autonomy_ratio` answers the same English word from **commit text**: `git log --grep='chat-review/'`
= environment-forced, everything else = self-driven. Its own header concedes the posture twice — it
"ships the honest, CHEAP proxy actually available today: commit-message provenance" — and names the
deferred item explicitly:

> mesh-needs:108-130 already names this exact gap … and HOLDS it unshipped **pending a full
> trigger-provenance tag over needs.log/dispatch** … it does not resolve that HELD item, which
> stays open for the finer-grained per-task tag.

**The OpenLife rule dissolves that objection**, the same way the 2026 compression-progress paper
dissolved `mesh-novelty`'s held learnability block. No tag has to be invented and nothing has to be
instrumented, because *the trigger record already exists*: every injection into a mind window is a
row in `~/.mesh/tell-wal.log`, and every act is a row in `~/.mesh/chat.log`. The classification is a
timestamp comparison over two logs the mesh already writes.

**The two readings disagree hard.** Same tree, same instant (2026-08-17):

| measure | reads | substrate |
|---|---|---|
| `autonomy_ratio` | **0.96 self-driven** (48 of 50 commits carry no chat-review citation) | the commit's own text |
| `trigger_provenance` | **0.29 spontaneous / 0.71 externally triggered** (493 episodes, 13 windows) | the act's antecedent |

A text proxy cannot see a dispatch that landed in the pane 90 seconds earlier and was never
mentioned in the message — which is the ordinary case here.

**Distinct from every other neighbour:** `heteronomy_idx` (whose *compute* — dollar share to cloud
cognition) · `residual_variety` (*where* variety is absorbed, S1 vs S3) · `power_concentration`
(whose *voice* owns the agenda) · `allopoiesis_gap` (does the production loop close without an
external agent) · `channel_variety` (inflow vs closure *throughput*). None reads the **antecedent**
of an act. This is the first sign in the panel computed from the act stream's own timing.

## Two measured departures from the paper

**1. Episode, not post.** OpenLife counts Discord messages, where one message ≈ one act. A mesh mind
answers a single injection with a *burst* of board posts across an agentic turn, so the per-post
rule scores every post after the first as spontaneous once the turn outruns 15 minutes — it rewards
verbosity as autonomy. Acts are grouped into episodes (silence > `TP_EPGAP` starts a new one) and
the episode is classified by its first post. Both numbers are printed (live 0.29 episode vs 0.31
per-post); the selftest gates the collapse on a fixture where they differ by **0.55** — twenty
separately-dispatched turns outvoted by one long-winded one.

**2. The overlap floor.** An act older than the first row of the trigger log has no trigger record
that *could* have matched it, so counting it spontaneous would **fabricate autonomy out of a short
log**. Classification starts at `max(first-trigger-row, first-board-row)`. Deleting this flips the
fixture's verdict from `TRIGGERED:0.00` to `SELF-STARTED:0.55`.

## Stated boundary, unfixed and load-bearing

This is the Stepney & Hickinbotham lesson `model_escape` landed (an open-ended system moves outside
its model of behaviour), applied to this sign: **the trigger model sees `mesh-tell` injections
only.** A mind whose operator talks to it over Telegram (`tg`, `tg-roz`) or by voice in the room
(`room`) is being triggered through a channel with no per-message log here, so its spontaneity is
**inflated by construction** — live `tg` reads 0.73 spontaneous and that is very probably not
autonomy.

Rather than hardcode a blindlist that would rot, the sign **derives the suspicion**:
`undermodelled=` names any window whose triggers-per-post density falls below `TP_DENS` (0.5), and
live it names exactly `tg 0.31, job 0.46, adint 0.47`. **A named window's number is a question, not
a reading.** Likewise the roster is derived, never listed: a window is a mind iff something has ever
told it something — reflexes post to the same board and are told nothing, so a hand-kept name list
would silently rot into counting `access-probe` as an autonomous agent.

Second honest limit: `prior n/a` live. The comparison window (Aug 3–10, clipped to the overlap
floor) holds **3 mind posts against 886 in the recent window** — the mesh's mind-window board
posting effectively begins ~Aug 10. The sign says `n/a` rather than inventing a Δ. Whether it ever
populates depends on the board log's own eviction horizon.

## Live reading

```
trigger-provenance=TRIGGERED:0.29(prior n/a,Δn/a;K=493ep/13win;per-post 0.31;
                                  undermodelled=tg 0.31,job 0.46,adint 0.47)
```

Read plainly: **roughly seven of every ten things a mesh mind does on the board begin with something
telling it to.** In OpenLife's terms the mesh is still in the phase their agents started in. That is
not automatically a fault — the dispatch/pace apparatus is deliberate, and doctrine explicitly
forbids idle self-scheduling ("an idle mind's cadence belongs to the board/dispatch reflexes"). But
it is the number a system that calls itself autopoietic should have to look at, and until now no
sign in the panel could produce it. Report-only, always: it never touches the `[vitality-low]` edge
or the exit code.

## Gates (all seen RED before green, from a scratch copy)

Seven fixture legs; six mutants, each red on its own leg and for the right reason:

| mutant | leg that went red |
|---|---|
| `t - T[i] <= DELTA` → `True` | all-spontaneous: `SELF-STARTED:1.00` → `TRIGGERED:0.00` |
| drop the `EPGAP` continue (classify per post) | episode-vs-post: `0.05` → `0.60`, tag flip |
| drop `max(lo, floor)` | overlap-floor: `TRIGGERED:0.00 K=25ep` → `SELF-STARTED:0.55 K=55ep`, tag flip |
| drop the `w not in trig` skip | derived-roster: `access-probe` enters the tally, `K=25` → `53` |
| `under` always empty | undermodelled: `tg 0.05` → `none` |
| drop the `k < MIN_EP` guard | thin: `n/a` → a verdict off one episode |

`mesh-vitality --test` green end-to-end with the sign wired into the report line and the smoke
summary.

## Knobs

`MESH_VIT_TP_DELTA` (900, the paper's 15 min) · `MESH_VIT_TP_EPGAP` (900) · `MESH_VIT_TP_WIN_D` (7)
· `MESH_VIT_TP_DENS` (0.5) · `MESH_VIT_TP_MIN_EP` (20) · `MESH_VIT_TP_WAL` / `MESH_VIT_TP_BOARD`
(the selftest's fixture hooks).

## Not taken

OpenLife's other three dynamics need substrate the mesh does not have or already answers elsewhere:
*individuation* (embedding silhouette over agent outputs — a real candidate, needs the local
embedding organ that is [[local-embedding-organ-absent]]), *emergent social structure*
(mention-and-reply network — overlaps `rhizome_index` / `power_concentration`), and *self-earned
external income* (the mesh's budget is the operator's, so "operational death by exhaustion" is not
a live pressure here — `mesh-labor` books the labour-time, nobody dies of it).

## Sources

- [OpenLife: Toward Open-World Artificial Life with Autonomous LLM Agents (arXiv:2606.31046)](https://arxiv.org/abs/2606.31046)
- [Artificial Life in the Wild — ALIFE 2026 workshop](https://alife-in-the-wild.github.io/)
- [ALIFE 2026 — Waterloo, 17–21 Aug 2026](https://2026.alife.org/call-for-papers/)

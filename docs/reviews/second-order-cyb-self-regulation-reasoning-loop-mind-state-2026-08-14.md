# Second-order cybernetics live review — the regulator that watches its OWN inference

**Date:** 2026-08-14 · **Lane:** literature (live review) — second-order cybernetics, from the angle of an
OPERATIONAL mechanism · **Landed in:** `scripts/mesh-mind-state` (`--loop`, report-only; uncommitted —
steward lands).

## The source (live, read this session)

**Xinrun Wang, Chang Yang, He Zhao, Zhuoyi Lin, Shuyue Hu — _The Agent Use of Agent Beings: Agent
Cybernetics Is the Missing Science of Foundation Agents_, arXiv:2605.10754v1, submitted 11 May 2026.**
Found by searching the live arXiv listings for 2026 work applying classical cybernetics to agent
systems; the six-law mapping was read from the HTML full text (`/html/2605.10754v1`), not the abstract.

The paper maps six canonical cybernetic laws onto six agent design principles. Five of them the mesh
already embodies in some form (feedback, requisite variety, homeostasis/ultrastability, black-box
probing, channel capacity — see the coverage map). **Principle 5 is second-order cybernetics proper**,
and unlike most writing in this area it is stated as a MECHANISM rather than a stance:

> §2: "The observer cannot be cleanly separated from the observed system… a second-order regulator R′
> acts on the space of first-order regulators: R′:ℋ→𝒦(R)."
>
> §3.1, Agent Design Principle 5: "A sufficiently autonomous agent must monitor and regulate its own
> inferential process, not merely its external actions… detecting looping behavior, declining
> confidence, and reasoning inconsistencies." The engineering mechanism: "detecting **structurally
> identical actions across many steps** (reasoning loop), mis-calibrated confidence estimates, or
> inference drift from task specification."

## The gap it names in this mesh

Every mind watcher we have reads a pane either for MOTION or for a BLOCK:

| watcher | what it catches | why it misses a loop |
|---|---|---|
| `mesh-mind-state` `classify()` | WORKING / NEEDS-INPUT / IDLE / DEAD | a looping mind carries a live spinner → WORKING |
| `mesh-mind-state` `wedge_state()` | an input line stuck ≥2 ticks | nothing is stuck in the input line |
| `mesh-pane-watch` | a DATA pane whose bytes are byte-identical across cycles | a mind pane's bytes churn every second (spinner, timers, token counter) — the hash never repeats, so this check cannot be pointed at mind panes at all |
| `mesh-unit-churn` | a crash-looping systemd unit | the mind never crashes |
| `mesh-criticality` | redispatch max-repeat on the BOARD | the loop never reaches the board |
| `mesh-spend` / `mesh-pace` | cost | bills the loop faithfully, judges nothing |

This file's own header calls NEEDS-INPUT "the blind state: liveness checks see a live pane, work checks
see no progress." A mind grinding the same action for an hour is **the other blind state** — live to
every watcher, progressing to none, paid for by the turn — and nothing in the fleet looked for it.

## Two measured facts that re-shaped the mechanism

The first draft counted repeated actions in the pane's scrollback. Both halves of that turned out to be
impossible on this surface, and both are now documented in the source:

1. **There is no scrollback.** Every mind pane on mesh-home holds tmux's ALTERNATE screen
   (`#{alternate_on}=1`; `#{history_size}=0` on genome/job/senses/witness), so `capture-pane -S -2000`
   returns the ~41-line visible frame — measured on 10/10 windows. A one-shot history read would have
   been a HOLLOW sense: permanently n/a, green by never looking at anything.
2. **The frame is not a faithful tail of the transcript, and repeats cannot be counted from it.** Seven
   identical probes were issued into a live mind pane while a 1.5 s sampler ran; the frame at the end
   contained NONE of them (one older `Update(...)` diff block occupied it). Separately, the
   overlap-merge draft recorded 2 rows for 6 identical calls — because "the same action still on
   screen" and "the same action started again" produce byte-identical frames. Frame sampling cannot
   count events, at any cadence.

So the statistic is the one the surface can actually support: **turnover of the visible action set**,
sampled across ticks.

## What landed — `mesh-mind-state --loop` (report-only)

* **Action extraction.** A `●`/`⏺` bullet counts as an action only if its next non-empty line is the
  `⎿` continuation — that structural pairing is what separates a tool call from assistant PROSE, which
  the renderer bullets identically. `● Tool(arg)` → `Tool(arg)` (identity **includes the argument**);
  `● <description>` → `Bash:<description>` (a Bash call's `$ <cmd>` echo is visible only WHILE it runs,
  so keying on the command would make identity depend on when we sampled). The live render puts a
  **NBSP** between `⎿` and `$`, which glibc does not classify as `[[:space:]]` — parsed explicitly.
* **Sampling.** One row per tick — `ts, digest-of-the-action-SET, lead action` — written **only while
  the window is classified WORKING**. That gate is what makes the axis mean anything: an idle pane's
  action set is unchanging too, and without it every resting mind would read as looping. The sampler
  rides the existing `--watch` cadence (`mesh-liveness-loop:44`, 600 s), so no new cron line and no
  autowire collision.
* **Verdict.** `STATIC` = the action set was identical across ≥4 CONSECUTIVE ticks spanning ≥900 s while
  WORKING · `TURNING-OVER` = it keeps changing · `n/a` = fewer than 6 WORKING samples in the window
  (idle, an unparsed engine dialect — opencode/agy/codex — or too few ticks yet). n/a is never
  TURNING-OVER: "we could not look" must not read as "we looked and it is fine".
* **The span floor is load-bearing, and it exists because the first version was wrong.** A tick count
  alone measures the SAMPLER, not the mind: a 2 s hand-run sampler reached `streak=4` in **six seconds**
  on a perfectly busy pane and reported STATIC. Requiring the streak to also cover 15 minutes of wall
  time makes the verdict a claim about the mind.
* **Consecutive streak, not global share:** an interleaved frame (a big older block co-resident with a
  new call) breaks the streak honestly, where a share statistic would keep accumulating.
* **Nothing alerts, sheds, feeds a state, or posts.** A reflex-driven mind legitimately re-runs one
  command per turn; repetition here is EVIDENCE, not a fault. Wiring an edge-trigger before this is
  calibrated live would be the cry-wolf shape the algedonic/habituation work already paid for once.
  What STATIC cannot separate — a repeat loop from ONE hung tool call — is stated in the verdict's own
  documentation rather than papered over.

## Live reads (mesh-home, 2026-08-14)

```
# after one long-running action, 2s sampler (demo cadence, span floor lowered to 5s):
genome    STATIC        ticks=28 sets=9 streak=4 streak-span=6s  lead=Bash:Sampler during one long action
# the same ring under the SHIPPED 900s floor — the honest answer at that cadence:
genome    TURNING-OVER  ticks=27 sets=9 streak=4 streak-span=6s  lead=Bash:Sampler during one long action
# a real --watch tick across the 12-window set: only the one WORKING window recorded a sample
.mind-loop-genome  →  1786733557  2572768850  Update(scripts/mesh-mind-state)
```

## Gates

`--test` 9.7 s, green. New assertions: tool-call and two-word-tool extraction · the live NBSP `⎿ $ cmd`
dialect → `R` · prose (including a sentence carrying parentheses) yields nothing · WORKING-only
sampling · an action-less frame records nothing · the n/a floor · STATIC at 6 ticks × 50 min ·
alternating sets → TURNING-OVER · a 10-second streak → TURNING-OVER.

**6 mutants, each RED from a scratch copy**, each checked for the RIGHT failure message: (1) drop the
`⎿` confirmation → the R/C dialect assertion fails; (2) drop the WORKING gate → "sampled a non-WORKING
frame"; (3) drop the span floor → "called a 10-second streak STATIC"; (4) streak without reset →
"called an alternating set STATIC"; (5) drop the n/a floor → "gave a verdict on 1 sample"; (6) require a
plain space instead of the NBSP allowance → the live dialect reads `C`. First run of the mutants was red
for the WRONG reason (rc=127 — the scratch copies were not `chmod +x`, and the file's existing CLI test
re-invokes `"$0"`); re-run as executables before any of the above was believed.

## Held (deliberately not done)

* No edge-trigger, no board post, no dispatch/shed effect — see above.
* No engine dialects beyond the Claude-family render. opencode/agy/codex panes yield honest n/a rather
  than a guessed parse.
* No attempt to read the engine's session JSONL (which WOULD give exact tool-call events): doctrine is
  that observation of a node goes through its tmux session, and the JSONL path exists only for the
  local claude engine. Worth revisiting if the axis proves useful.

# THE stream pattern — how minds connect to work (operator, 2026-06-11)

> "This pattern is for EVERYTHING. Minds don't generate work per se — work is a mind's RESPONSE to
>  data fed into its session. Any stream = a tmux window/pane (the SOURCE), reflective PULLING,
>  FILTERING, and CONDITIONALLY feeding the filtered data as a KEYSTROKE prompt into a mind's tmux
>  session (claude/opencode/gemini/codex; claude default). Set up the message flows so tasks flow
>  and get generated from the mesh's goals + the ideas we discussed — autonomous loops via tmux."

## The shape (one primitive, everything is an instance)
    SOURCE (tmux pane) → reflex PULL → FILTER (condition + shaping) → conditional KEYSTROKE-FEED → MIND
- **Cheap reflex always runs** (cron/timer). **Expensive mind engaged only when the filter emits.**
- The mind's job is to RESPOND to the fed prompt. It does not hunt for work; work arrives.

## The primitives
- **`mesh-stream <name> '<pull>' '<filter>' [mind]`** — the MONITOR flavor (idempotent pull). Live
  pane `mon:<name>`; filter reads pull's stdout, emits the prompt to feed (empty = nothing needed);
  edge-deduped. e.g. health: pull=`mesh-doctor --quiet`, filter=`grep -qE '[1-9][0-9]* FAIL' && echo …`.
- **`mesh-generate` → `mesh-feed`** — the QUEUE flavor (consuming pull). mesh-generate pops the next
  `[ ]` idea from `~/.mesh/ideas-queue` → frames a task in `~/.mesh/backlog` → marks it `[~]`;
  mesh-feed keystroke-feeds backlog tasks to idle minds. (Queue needs consumption, not dedup — that's
  why it's a distinct flavor, but it's the SAME pull→filter→conditional-feed shape.)

## Live instances (cron) = the autonomous loop
- monitor: `*/5 mesh-stream health …` → feeds claude ONLY on a real doctor FAIL.
- task-flow: `*/4 mesh-generate` (ideas→backlog) + `mesh-feed` (backlog→idle mind). Proven: an idea
  flowed to gemini's session unattended.
- breath: `mesh-tick` role-streams (plan/check/verify). board: `mesh-chat-sync`.

## Source of work = goals + ideas
`~/.mesh/ideas-queue` (curated from knowledge/fields-to-mine.md, ideas.log, PLAN goals, [idea] posts).
The PLANNER's job shifts: not hand-assign each tick, but keep the ideas-queue FED and curated; the
loop generates + flows tasks from it. Refill the queue when `open` count runs low.

## Why this matters
No single mind is a bottleneck; no loop stalls on one actor. Routine = reflexes (cheap, in panes);
judgment = minds (engaged on demand). Tasks generate from the mesh's own goals/ideas and flow to
whoever's free. Related: [[tmux-native-principle]], [[quiet-is-not-done]], reflex-doctrine.

# Survey: OSS tmux-send-keys agent orchestration vs our mesh — and what we adopted

Date: 2026-06-12
Operator task: "look at existing repos where agents communicate via tmux send-keys,
pick/adopt the best solution for us — maybe it's ours already, need to check."

## Repos surveyed

| Project | Core idea | Coordination | State detection |
|---|---|---|---|
| **Jedward23/absmartly Tmux-Orchestrator** | `send-claude-message.sh session:window "msg"` + `schedule_with_note.sh N "note"` (agents self-schedule check-ins) | none structured (PM-agent assigns verbally) | none documented |
| **mixpeek/amux** | REST API → tmux send-keys; web dashboard | SQLite task board, atomic claim, @mention channels, peek API | **parses ANSI-stripped scrollback**: Working / Needs-input / Idle; auto-answers rate-limit + permission prompts |
| **primeline-ai/claude-tmux-orchestration** | idle→send `/orchestrate-cycle`; bash heartbeat | file-based (`_orchestrator/` dir) | heartbeat files |
| **Dicklesworthstone/claude_code_agent_farm** | 20+ panes, prompt-file launch | **lock files** (`active_work_registry.json`, `agent_locks/`) | heartbeat files (>2min=stuck), context-% in pane title, error-pattern detection (auth/parse/login) |
| **Claude Code agent teams** (official, experimental, v2.1.32+) | lead spawns teammates, **mailbox** msg delivery + shared task list w/ file-lock claim | shared task list, dependency unblocking, TeammateIdle/TaskCreated/TaskCompleted hooks | automatic idle notification (built into the agent, not pane-scraped) |

## Verdict: our mesh already has the architecture; we were missing ONE primitive

What we already do **as well as or better than** the field:
- send-keys mechanics: `mesh-tell` already uses the exact best-practice sequence the
  field converged on — `C-u` clear, `send-keys -l` literal (base64-wrapped, beats the
  multiline-newline bug every repo warns about), separate `C-m` submit. Plus a thing
  none of them do: **drives the bottom (MIND) pane by pane_top**, not the active/data pane.
- waiting: `mesh-watch --until/--change` = amux's peek, tmux-native.
- coordination: `mesh-chat` board ([task]/[taking]/[done]) + `mesh-trace` = their task
  board; we're file/tmux-native instead of SQLite/REST (matches our no-DB doctrine).
- self-scheduling: `mesh-tick` cron + ScheduleWakeup = Tmux-Orchestrator's
  `schedule_with_note`, but reflexive and always-on.
- remote: `--node user@ip` over Tailscale SSH — most repos are single-host only.

The **one genuinely good idea we lacked**: amux + agent-farm both **classify pane STATE
from scrollback** (Working / Needs-input / Idle / rate-limited / error). Our liveness
stack (`mesh-supervise` process+beat, `mesh-phi` accrual, `mesh-mind-watch`) detects
DEAD/WEDGED but is **blind to alive-but-blocked** — exactly the failure that bit ds today
(mind sat HOURS on a permission prompt: UP for supervise, DEAD for work; see
[[ds-doctor-triage-2026-06-12]]).

## Adopted → `mesh-mind-state` (new genome tool)

Brings amux's idea in tmux-native, no REST/SQLite, no agent patching:
- `classify()` on the **bottom 8 pane lines** (status bar lives there; scanning deeper
  matched quoted dialogs in agent output — caught misclassifying its own author's pane).
- States: WORKING (live spinner w/ running timer / "esc to interrupt") · NEEDS-INPUT
  (permission/confirm dialog) · RATE-LIMITED (quota/usage-limit — codex was live in this
  state during testing) · IDLE (empty prompt) · DEAD (empty/bare-shell) · UNKNOWN.
- `--watch` edge-triggers `[mind-blocked]`/`[mind-limited]`/`[mind-unblocked]` to the
  board (body-power/therm pattern, MESH_ALERT_DRYRUN gated). Cron */10 both nodes.
- Complements, not replaces, supervise: supervise sees the *process*, mind-state sees the
  *TUI*. Blocked-on-prompt = the gap between them.

NOT adopted (rejected with reason): amux's **auto-answering** of permission prompts —
that defeats the consent gate on purpose; we ALERT a human/peer to choose, never
auto-press Yes. SQLite/REST task board — our mesh-chat is deliberately fileless-tmux.
Official agent-teams mailbox — heavier, single-host, experimental, and lead-fixed; our
flat stigmergic model is the explicit design (no fixed mind).

## Verification

- `--test` golden-pane classifier: dialog→NEEDS-INPUT, spinner→WORKING, prompt→IDLE,
  empty→DEAD, quota→RATE-LIMITED — all pass.
- Live against all 4 local minds: claude=WORKING (correctly, after the bottom-8 fix
  stopped it self-matching a fixture in its own diff), codex=RATE-LIMITED (real, genuine
  quota stop), gemini/opencode=WORKING. ds `--test` ok, cron wired.

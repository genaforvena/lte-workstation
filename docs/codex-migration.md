# Codex migration

`lte-workstation` used Claude Code as its primary mind engine. Codex is now a supported primary
engine while the existing Claude integration remains available as an explicit fallback during the
transition.

## Instruction loading

Codex reads the repository root [`AGENTS.md`](../AGENTS.md) automatically. That file is intentionally
short enough to survive Codex’s default project instruction limit. It points to [`CLAUDE.md`](../CLAUDE.md),
which remains the mesh’s canonical doctrine because mesh tools parse its tooling and on-demand canon
sections. The name is historical and does not restrict the doctrine to Claude.

## Durable context

Both engines support SessionStart JSON. [`.codex/hooks.json`](../.codex/hooks.json) invokes
[`mesh-codex-lifecycle --start`](../scripts/mesh-codex-lifecycle), which returns the existing
`mesh-handoff --restore` output. Creation, resume, clear, and compaction use the same external text.
[`mesh-codex-context`](../scripts/mesh-codex-context) is the manual plain-text recovery adapter.
Write a handoff before leaving a session or handing work to another mind:

```bash
mesh-handoff <window> "<done> + <next> + <key paths/files/vars>"
```

Codex compaction may preserve conversation context, but it does not replace the mesh’s durable
handoff. The existing five-minute snapshot remains the crash recovery path.

## The autonomous turn loop

The prior design is `docs/superpowers/specs/2026-07-18-mind-recycle-design.md`:
fresh context after each work turn, durable memory outside the engine. Its old polling driver remained
in shadow mode and depended on Claude breadcrumbs and a model to propose continuation.

The existing `mesh-pane-consume` watches the algorithmic top pane, strips display clocks, and wakes
the mind only for meaningful change. `mesh-consume-all` supervises it. Board writes separately wake
`mesh-dispatch` through `mesh-fsnotify`. The source renderer and these gates do not need an LLM.
The mind owns interpretation, bounded action, and artifact verification.

For Codex, configure the user-level `notify` array with the absolute deployed path to
`mesh-codex-lifecycle`. Its `agent-turn-complete` callback accepts only the root thread registered
by SessionStart. Auxiliary title-generation notifications and subagent threads must not reset a pane.
The callback saves a JSON receipt and the literal final response under
`~/.mesh/codex-lifecycle/<window>/`, preserves the previous handoff, posts a handoff pointing to the
result, and appends one deduplicated TURN to `spend.log`. `mesh-labor` materializes that tape in hledger;
native windows are excluded from the older activity sampler to avoid counting twice. A TURN here is
one root work turn, potentially containing many model/tool calls, not a token bill.

The worker calls `mesh-clear` after the mind is idle and checks that a fresh empty composer appeared.
It never injects a restore-only prompt. SessionStart delivers the texts on the next real turn.
Pending resets remain on disk; `mesh-codex-lifecycle --drain` runs every minute as a retry.
`mesh-tell` refuses a new delivery while a reset is pending so dispatch/consumer callers can retry.
Detached undelivered work still blocks clearing through `mesh-clear --gate`.

## Verification on mesh-home, 2026-09-06

The test rollout remains `senses`, `health`, and `witness`. All three ran native SessionStart probes,
reported their own charter/handoff, produced completion receipts, and returned to empty Codex chats.
Their diff-check intervals are now 60 seconds; existing wake budgets and refractory controls remain.
Witness also consumed its real live pane, handed off the open mind-count defect, and genome took the
existing task `{#28a1b8d2}`. That is a live observation → action → external handoff → follow-up example.

The probe caught three migration defects: the Codex placeholder was misread as stuck input, title
generation was initially mistaken for a root turn, and minute-only labor timestamps could lose a
completion near a feed watermark. Root identity binding, placeholder handling, and second-resolution
completion timestamps/parser fix those paths. Initial title receipts remain annotated as excluded;
their spend rows are classified as auxiliary and the local hledger has an explicit correcting entry.

The already-running operator `tg` session needs a one-time restart to load the new notify setting.
Its node-local `~/.mesh/codex-lifecycle/adopt-operator.py` bridge waits for the exact current root's
JSONL completion, saves the normal receipt/handoff, clears, and gracefully restarts Codex. It fences
new deliveries during restart and preserves the current turn's existing legacy sampler count.
`adopt-operator.json` records whether that post-response transition actually finished; an armed bridge
is not evidence of a completed restart.

Native hooks require review on first use; the test node has trusted this repository's hook. Other
nodes need the deployed helper, user notify configuration, and a restarted/trusted Codex session before
this lifecycle is active. A repository change alone is not proof of fleet-wide rollout.

## Skills

The existing planting skill is discoverable to Codex at
`.agents/skills/mishe-mishe-to-tauftauf/SKILL.md`. Its source remains in `skills/` so Claude and
other engines can continue to use it. A planted Codex home should install the skill under
`$CODEX_HOME/skills/mishe-mishe-to-tauftauf/`.

## Engine selection

`mesh-restore` now selects Codex for the operator-facing mind channels when Codex is available. Set
`MESH_PRIMARY_MIND_TYPE=claude` or the existing per-channel `MESH_*_CMD` variables in
`~/.mesh/restore.env` to retain or override Claude for a node. `MESH_CODEX_CMD` is the Codex command
override and is kept node-local. The restore path launches Codex with
`--sandbox danger-full-access --ask-for-approval never`.

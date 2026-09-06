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

Claude’s SessionStart hook returned JSON. Codex uses [`scripts/mesh-codex-context`](../scripts/mesh-codex-context)
to print the same charter and handoff as plain text. Run it when entering a tmux window, then resume
from the restored handoff. Write a handoff before leaving a session or handing work to another mind:

```bash
mesh-handoff <window> "<done> + <next> + <key paths/files/vars>"
```

Codex compaction may preserve conversation context, but it does not replace the mesh’s durable
handoff. The existing five-minute snapshot remains the crash recovery path.

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

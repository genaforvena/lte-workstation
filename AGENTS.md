# lte-workstation — Codex operator contract

Read [`MESH.md`](MESH.md) first. It is the editable, engine-neutral procedural contract shared by
Codex/OpenCode-style minds; this file is the repository bootstrap and `CLAUDE.md` remains the full
mesh doctrine.

This repository is a distributed mesh of machines and agent minds. Codex is a first-class mind in
that mesh. Work from the repository root unless the task explicitly names another node.

## Load the mesh culture

`CLAUDE.md` is the existing mesh-wide doctrine and remains the canonical source for the verification
rules, substrate coordination protocol, tool catalog, charters, and board conventions. Read it before
any task that changes mesh behavior, networking, scheduling, agent channels, or durable memory. The
filename is a compatibility name from the Claude era; its rules apply to every engine, including
Codex. Read the relevant `docs/` case linked by a rule when the evidence matters.

The window-specific charter is `~/.mesh/charter/<window>.md`, falling back to `charter/<window>.md`.
The node-specific context is `CLAUDE.local.md` when present. Do not commit either node-local file.

## How Codex operates here

- Act on an authorized task and report the action after it starts. Do not wait for an approval prompt
  that the operator has already withdrawn.
- Keep the visible response terse. The board, files, tests, commits, and real sensor artifacts are
  the evidence; a claim in chat is not an artifact.
- Use `mesh-chat` for board/room posts. The active mind owns `[task]`, `[taking]`, `[done]`,
  `[yield]`, and `[fyi]` lines. A subagent returns findings; it does not impersonate the window or
  write the substrate.
- Preserve single-writer discipline for routing, DNS, firewall, VPN, `mesh-dms`, claims, and other
  substrate changes. Inspect live state before editing it.
- Prefer `rg` for searches. Use `apply_patch` for deliberate file edits. Preserve unrelated dirty
  worktree changes.

## Prefer subagents

Delegate each independently verifiable piece of work to a subagent by default: broad searches and
multi-file audits, long log or corpus reads, multi-step side-quests, and each independent fix (one
subagent each, fanned out in parallel; isolated worktrees when they mutate files). Keep in the
active mind only what cannot be delegated: substrate writes, board/room voice, landing, and final
verification. A subagent's report is a lead, never an artifact — inspect the file, the ref, or the
red-then-green test by your own hand, and record the delegation plus the inspected result before
claiming it was used. Tiny single-file edits and tightly coupled changes stay in the mind when
delegation would cost more coordination than context saved.

## Context, compaction, and handoffs

Every completed work turn ends in an artifact and a textual handoff, then a context reset.
The top pane is algorithmic: its meaningful changes and board claim dispatch wake the mind.
Creation and restoration use the same charter, handoff, and current observations. A reset alone
is not new work and must not generate a restore-only LLM turn. Read the prior result before acting;
never repeat a completed claim just because the session is fresh. In the final response cite the
artifact, verification performed, unresolved obligations, and the exact next action if any.
Codex SessionStart restores text; its completion callback persists the final response and handoff,
records one TURN in the hledger input tape, and clears once the pane is idle. The five-minute
snapshot remains crash recovery. Multi-tool work belongs inside one turn; do not clear mid-tool.

Codex may compact a long turn automatically; this is not the mesh turn boundary. Native SessionStart
hooks reload textual mesh state after creation, clear, resume, or compaction. A handoff is required before
leaving a session, and before an intentional context reset:

```bash
mesh-handoff <window> "<done> + <next> + <key paths/files/vars>"
```

This writes `~/.mesh/handoff/<window>.md` and posts one `[handoff]` board line. The existing
`mesh-handoff --snapshot` reflex is the crash safety net. Use `mesh-clear <window>` for the mesh’s
gated clear procedure for an intentional reset. Native completion owns normal end-of-turn resets.
Cron/reflexes remain the liveness guarantee across an engine restart.

SessionStart loads the charter and handoff automatically. If that context is absent, restore it before acting:

```bash
mesh-codex-context
```

If the command is unavailable, run `mesh-handoff --restore` and inspect its JSON
`hookSpecificOutput.additionalContext` field. Treat a handoff from before the node’s last boot as
history to verify, as the restore output says.

When handing work to another Codex session or to a different engine, write the handoff first, include
the exact next command or decision, and cite the paths and artifacts that let the receiver verify it.

## Skills

Project skills are under `.agents/skills/`. The repository’s existing planting skill is available as
`.agents/skills/mishe-mishe-to-tauftauf/SKILL.md`; its source and references remain under
`skills/mishe-mishe-to-tauftauf/`. Read the skill before using its planting workflow. Do not silently
install packages, schedule jobs, or edit another person’s configuration as part of planting.

On every mind wake, treat mesh-owned resource contention, missing dependencies, and recoverable runtime
failures as autonomous work: read and apply [mesh-unblock](.agents/skills/mesh-unblock/SKILL.md) before
calling anything a blocker or asking the operator to intervene.

## Verification

Every claimed capability needs a real artifact and an honest failure state. Run the narrowest relevant
`--test` or project check after changes. For mesh changes, verify both the code path and its wiring;
passing a tool’s self-test does not prove that a reflex runs. Before handoff, report what changed and
what was actually verified.

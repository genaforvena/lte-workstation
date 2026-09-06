---
name: mishe-mishe-to-tauftauf
description: Plant the small, local mishe culture without cloning a repository, installing packages, or scheduling anything. Use when planting or removing the mishe skill on a Codex node.
---

# mishe-mishe-to-tauftauf

This is the Codex entrypoint for the existing mesh planting skill. The complete workflow, references,
and executable core live in [`skills/mishe-mishe-to-tauftauf/`](../../../skills/mishe-mishe-to-tauftauf/).

Read the source skill and the relevant reference before acting:

- [`SKILL.md`](../../../skills/mishe-mishe-to-tauftauf/SKILL.md) for the workflow and invariants.
- [`reference/planting.md`](../../../skills/mishe-mishe-to-tauftauf/reference/planting.md) for the
  decision branches.
- [`reference/seed.md`](../../../skills/mishe-mishe-to-tauftauf/reference/seed.md) for a one-file
  transfer to a machine that has no repository.
- [`reference/reflexes.md`](../../../skills/mishe-mishe-to-tauftauf/reference/reflexes.md) before
  proposing a schedule.

For the Codex installation path, the active skill directory is `$CODEX_HOME/skills` (normally
`~/.codex/skills`). The repository copy under `.agents/skills/` is the project-local discovery copy.
Keep the core’s no-network, no-package-manager, no-registration, no-telemetry guarantees intact.

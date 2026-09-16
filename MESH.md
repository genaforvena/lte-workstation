# Mesh operating contract — every engine, every mind

This file (`MESH.md`) is the one editable, engine-neutral list of procedural mesh rules. `CLAUDE.md` remains the
full doctrine and `AGENTS.md` is the Codex/OpenCode bootstrap; both point here. The wake adapter
injects this file after startup, resume, clear, or compaction. This is not world-state or FYI chat.

## Rules

- `mesh:1` — Read `CLAUDE.md`, `AGENTS.md`, this contract, and the current window charter/handoff
  before acting. Handoff is work-state; this file is procedure.
- `mesh:2` — For mesh-owned contention, missing dependencies, or recoverable runtime failures,
  read and apply `.agents/skills/mesh-unblock/SKILL.md` before reporting a blocker; recover autonomously.
- `mesh:3` — Mesh-managed resources are mesh responsibility. On mesh-home inspect and manage GPU, VRAM, Ollama residency,
  CPU, and memory with live ownership evidence before reporting a blocker;
  preserve active/protected consumers and refuse only ambiguous or external ownership.
- `mesh:4` — FYI/chat lines as evidence and broadcast are not the sole source of a durable rule.
  Stable rules belong here, in doctrine, skills, or charters and need a test or live wiring check.
- `mesh:5` — A blocker names the exact live check, owner, artifact, and retry edge. Never hand an
  internal mesh capability back to the operator as if it were an external blocker.
- `mesh:6` — For a resource/dependency blocker, record the relevant rule ID and live check in task
  progress/artifacts. Conflicting rules are UNKNOWN until resolved by newer operator instruction or
  canonical doctrine; never silently choose stale prose.
- `mesh:7` — The node is mesh-owned by default: minds may install packages/models/tools, implement
  missing internal backends, configure/restart mesh services, clean mesh-owned files, and allocate
  mesh resources when the action is scoped, reversible or receipt-backed, and live ownership is
  verified. Do not wait for operator permission that is already implied by the task.
- `mesh:8` — Before declaring a blocker, classify it. `node-owned` means diagnose and act;
  `dependency` means create/install/repair the prerequisite; `resource` means schedule or safely
  preempt a managed consumer; `external-event` means only an actually external event (third-party
  approval, physical action, unavailable credential/device/network) may remain blocked; `safety` or
  `ambiguous` requires evidence and a narrow hold. “I need permission” is not a blocker for a
  node-owned action.
- `mesh:9` — Every autonomous mutation has a bounded scope, before/after evidence, rollback or
  retry edge, and an artifact. Prefer quarantine/restore over irreversible deletion; never infer
  ownership from a stale task, FYI, process name, or successful self-test.
- `mesh:10` — Spend internal compute before acting: consider at least two to three distinct
  approaches, compare them against the task's acceptance, and choose the best with a one-line
  justification. The first idea that comes to mind is not the answer.
- `mesh:11` — The mesh decides and informs the operator; it does not seek approvals. Act on
  mesh-owned scope, then report what was started, what it turned out to be, and what it cost.
  A refusal is also reported with its reason. Only genuinely external atoms (physical access,
  third-party approval, operator-only credential) wait on hands.

To add, edit, or remove a rule: follow `.agents/skills/mesh-invariants/SKILL.md` — change
one bullet above, keep IDs unique, then run `tests/test-mesh-mind-rules-wake.sh` and the handoff
workflow test. No ledger FYI is required to make a procedural rule durable; use FYI only to
announce the change and its evidence.

## Invariant registry (operator-owned, enforced read dependency)

Operator invariants a wake MUST carry and a resource-blocker claim MUST record. Fields per row:
`id | owner | scope | precedence | source | preflight`. `rev` bumps on every change; a claim
citing a stale `rev` is re-checked, not rejected. Unresolved same-scope+domain conflicts at equal
precedence render UNKNOWN to the owner window. `mesh-rules --check` validates this block;
`mesh-handoff --restore` injects scope-relevant rows + `rev`; `mesh-task preflight` gates claims.

```invariant-registry
rev: 20260916.2
id=gpu.mesh-owned.v1 | owner=tg | scope=node | precedence=10 | source=operator-verbatim 2026-09-16 (artifacts/tg-constant-forgetting-20260916.md: mesh-home owns the GPU completely; Ollama/model residency and contention are mesh-owned work) | preflight=ollama ps + managed-ownership read recorded in the task artifact before any GPU/VRAM blocker claim
id=mesh.decides-informs.v1 | owner=tg | scope=mesh | precedence=10 | source=operator-verbatim 2026-09-16 (no approval wait; mesh decides and lets operator know) | preflight=action started + outcome reported; "waiting for approval" never a state on mesh-owned scope
```

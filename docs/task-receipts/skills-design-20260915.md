# Mesh skills taxonomy design — 2026-09-15

Task: `mesh-skills-20260915/design-skills-taxonomy`  
Owner: `pub`  
Status: proposal only; no `SKILL.md` implementation or loader wiring was made.

## Evidence and scope

The prerequisite audit is complete at [`skills-audit-20260915.md`](skills-audit-20260915.md).
It measured 11 manifests across the installed tree, repository source, and repository shim; found
the installed Codex tree at `/home/mesh-home/.codex/skills/`; found no `/skills` mount; and found
that repository-local skills are visible by path but not proven discoverable by the engine catalog.
The audit also ranked the large recurring doctrine and node context as the strongest extraction
opportunities, with board/task-ledger protocol a smaller but high-value coordination candidate.

The live repository corroborates the path model: `skills/mishe-mishe-to-tauftauf/` is the canonical
source, `.agents/skills/mishe-mishe-to-tauftauf/` is a short discovery shim, and `opencode.json`
currently declares `skills` and `~/.claude/plugins/cache/superpowers-marketplace` as skill paths.
Existing planting scripts and the shim identify `~/.claude/skills/` as Claude's install path.

## Proposed skill set

Each skill has a narrow trigger and should contain reusable procedure plus links to measured cases;
it must not duplicate the whole charter or `CLAUDE.md`.

| Name | Description / trigger phrases |
|---|---|
| `mesh-board-ledger-protocol` | Coordinate board posts, task claims, progress, typed blocks, structured close, and hledger evidence. Trigger: “post/claim/dispatch/settle a mesh task”, “what do I owe the board?”, “close this task”. **Pilot.** |
| `mesh-evidence-verification` | Choose an artifact-backed gate, exercise the real path, and report red-then-green evidence and wiring separately. Trigger: “verify this capability”, “run the real test”, “is this wired?”. |
| `mesh-handoff-lifecycle` | Preserve work state through handoff, clear, restore, and completion; identify the exact next action and artifact. Trigger: “handoff”, “clear/reset”, “resume this work”, “what survived the reset?”. |
| `mesh-substrate-coordination` | Apply single-writer discipline for routing, DNS, firewall, VPN, claims, DMS, and shared substrate; inspect live state before edits. Trigger: “change mesh routing/network/substrate”, “who owns this writer?”. |
| `mesh-tool-enumerator` | Maintain the source/deployed inventory and teach every reader its complete candidate set, including skill payloads and tool directories. Trigger: “enumerate/install/sync mesh tools”, “why is this directory silent?”, “is this wired?”. |
| `mesh-context-extraction` | Extract high-cost recurring doctrine or node facts into triggered skills while preserving authority, links, and measurable behavior. Trigger: “reduce per-turn context”, “extract a skill”, “what belongs in a skill?”. |
| `mesh-node-senses` | Operate sensor reads with freshness, coverage, contention, unknown-state, and real-hardware artifact rules. Trigger: “read a sensor”, “is the node healthy/live?”, “probe hardware”. |
| `mesh-publishing-case` | Turn a measured failure and artifact into an outward-facing draft or publication with dates, commits, and honest uncertainty. Trigger: “write/publish a case”, “draft a dev.to post”, “reply to a reaction”. |

The set is intentionally concern-oriented: topology and universal doctrine are extraction parents,
not one giant always-loaded skill. A skill description is a routing hint, not authority.

## Storage and mirrors

For every mesh skill, keep one canonical tree under `skills/<name>/`, with `SKILL.md` frontmatter
(`name`, `description`), concise workflow text, and optional `reference/`, `assets/`, or `core/`
payloads. The repository-local engine shim lives at `.agents/skills/<name>/SKILL.md` and points back
to the canonical source, as the existing `mishe-mishe-to-tauftauf` precedent does. Do not maintain
two independent implementations. Any generated/install copy must be traceable to the canonical
source and checked for source/deployed parity.

Proposed layout:

```text
skills/
  mesh-board-ledger-protocol/
    SKILL.md
    reference/
.agents/skills/
  mesh-board-ledger-protocol/
    SKILL.md                 # discovery shim; links to ../../../skills/...
```

`docs/task-receipts/` remains evidence and design output, not a skill loader directory.

## Per-engine loader wiring (future implementation proposal)

No wiring was changed in this task. The implementation task should make and verify the following
explicit mappings:

| Engine | Loader path / current fact | Proposed wiring |
|---|---|---|
| Codex | `$CODEX_HOME/skills` (normally `~/.codex/skills`); audit measured this as the installed tree | Install/sync the canonical skill directories there, or establish a verified supported link from the repo shim. Prove discovery with the engine's `/skills` listing and source/deployed parity. |
| Claude | `~/.claude/skills/`, as used by existing planting/install scripts | Install/sync the same canonical directories there. Verify Claude discovers frontmatter and does not receive a divergent copy. |
| opencode | `opencode.json` has `skills.paths: ["skills", "~/.claude/plugins/cache/superpowers-marketplace"]` | Keep repo `skills` as the source path; add `.agents/skills` only if an actual reader requires it, then test precedence and duplicate-name behavior. Do not assume the Codex/Claude paths are read by opencode. |

The loader work must also define precedence, duplicate-name rejection, absent-directory behavior,
and a fresh-catalog test for each engine. A path being readable is not evidence that the engine
enumerates it.

## Enumerator-teaching requirement

Every reader or installer that enumerates mesh content must explicitly include the skill tree and
the following existing tool directories/files in its candidate set:

`mesh-land`, `mesh-sync-tools`, `mesh-doctor`, `mesh-autowire`, and `mesh-vitality`.

This is a required reader census for `mesh-land`, `mesh-sync-tools`, `mesh-doctor`,
`mesh-autowire`, and `mesh-vitality` themselves, plus bootstrap/setup/install and any future skill
loader. A directory that no reader glob/pathspec includes is silent: it may exist on disk while
never being landed, synced, diagnosed, autowired, or kept alive. The implementation must show the
candidate path in each reader and a fixture proving a newly added skill/tool is observed.

## Authority rule

Skills are subordinate instructions. A skill never overrides the active window charter,
`CLAUDE.md`, `CLAUDE.local.md`, safety gates, or operator instruction. On conflict, resolve to the
charter first, then mesh-wide doctrine, then node-local context, then the skill; record the conflict
and stop or escalate when the higher-authority rule makes the requested action unsafe. Skill text
must link to cases rather than silently restating or weakening those authorities.

## Pilot decision

Implement `mesh-board-ledger-protocol` first. It is the smallest high-fan-in extraction with an
objective contract: exact `[task]`, `[taking]`, `[progress]`, `[block]`, `[done]`, `[yield]`, and
`[fyi]` markers; owner and lease discipline; `mesh-task` structured transitions; artifact and
SHA-256 closure; hledger/accounting agreement; and handoff obligations. It exercises all three
engine loaders without coupling the first pilot to hardware or external publishing.

## Genome-ready implementation task spec — explicit next step

Create and dispatch a genome-owned implementation task for
`mesh-board-ledger-protocol`. It must: (1) add the canonical `skills/mesh-board-ledger-protocol/`
manifest and references; (2) add the `.agents/skills/` discovery shim; (3) wire the verified
Codex, Claude, and opencode paths without changing charter authority; (4) update the enumerator
census for `mesh-land`, `mesh-sync-tools`, `mesh-doctor`, `mesh-autowire`, and `mesh-vitality`;
(5) add red-then-green discovery, duplicate-name, source/deployed-parity, and ledger-close
fixtures; and (6) produce an implementation receipt with exact commands, outputs, and unresolved
engine limitations. The implementation task must remain separate from this proposal and must not
land any broad `CLAUDE.md` or charter rewrite as a shortcut.

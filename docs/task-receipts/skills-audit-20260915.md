# Skills landscape audit — 2026-09-15

Task: `mesh-skills-20260915/audit-skills-landscape`  
Actor: `discover`  
Scope: read-only inspection of this node's Codex skill paths and per-turn context cost.

## Executive result

The engine-installed skill tree is `/home/mesh-home/.codex/skills/`; it contains nine
`SKILL.md` manifests (three directly under the tree and six under `.system/`). The repository
contains one `.agents/skills` shim and one canonical `skills/` source, but neither is copied into
the engine tree. `/skills` does not exist. The runtime skill catalog exposed the installed/system
skills and did not expose the repository-local shim as a separate discoverable entry; therefore
repo-local skills are visible by filesystem path, but are not proven engine-discoverable without
explicit loading. Every one of the 11 manifests found across the three existing trees has non-empty
`name` and `description` frontmatter.

## Engine/path matrix

| Candidate path | Exists | `SKILL.md` count | Observed role / visibility |
|---|---:|---:|---|
| `/skills` | no | 0 | No global mount on this node |
| `/home/mesh-home/.codex/skills/` | yes | 9 | Engine-installed tree; runtime catalog source |
| `.agents/skills/` | yes | 1 | Repo shim for `mishe-mishe-to-tauftauf`; not in installed tree |
| `skills/` | yes | 1 | Repo canonical source plus `core/` and `reference/` payloads |

Installed manifests and measured bytes: `brainstorming` 1,486; `driving-coding-agent-sessions`
2,328; `using-superpowers` 1,506; `.system/imagegen` 19,201; `.system/openai-docs` 5,437;
`.system/plugin-creator` 11,467; `.system/review-agent` 2,661; `.system/skill-creator`
15,311; `.system/skill-installer` 3,367. The repo shim is 1,310 bytes and its canonical source
is 17,100 bytes. The frontmatter check over all 11 manifests returned `frontmatter_check_rc=0`.

## Repeated context cost

The following are measured file/section sizes from this checkout. Approximate tokens are a rough
`ceil(bytes / 4)`, included only as a comparable budget proxy; they are not tokenizer output.

| Loaded or recurring material | Bytes | Words | Approx. tokens | Frequency evidence |
|---|---:|---:|---:|---|
| `CLAUDE.local.md` | 93,100 | 13,826 | 23,275 | node context, loaded per turn |
| `CLAUDE.md` | 67,548 | 9,710 | 16,887 | mesh doctrine, loaded per turn |
| `AGENTS.md` | 4,700 | 688 | 1,175 | repository contract, loaded per task |
| `~/.codex/RTK.md` | 482 | 77 | 121 | injected repository instruction |
| `~/.mesh/charter/discover.md` | 2,088 | 312 | 522 | discover charter, loaded per discover turn |
| Verification principle section (`CLAUDE.md:98–294`) | 17,056 | 2,459 | 4,264 | embedded in every `CLAUDE.md` load |
| Substrate coordination (`CLAUDE.md:295–339`) | 3,399 | 527 | 850 | embedded in every `CLAUDE.md` load |
| End-of-session/handoff (`CLAUDE.md:340–406`) | 5,439 | 801 | 1,360 | embedded in every `CLAUDE.md` load |
| Chat/board/task-ledger rules (`CLAUDE.md:512–573`) | 5,675 | 826 | 1,419 | embedded in every `CLAUDE.md` load |

The literal `task-ledger` count is zero in the four injected context files because the doctrine
uses prose such as “task ledger”; the board marker is defined in `CLAUDE.md:550–557`. Literal
marker counts in the files were: `CLAUDE.md` board 17, handoff 28, substrate 11, verification 4;
`CLAUDE.local.md` board 10, substrate 5, verification 1; `AGENTS.md` board 5, handoff 14,
substrate 3, verification 3; discover charter board 2.

## Extraction candidates, ranked

Ranking uses measured bytes as the size term and the documented per-turn load as the frequency
term. All candidates below are high-frequency (`1/turn` when their parent context is loaded), so
the ranking is size-dominated and intentionally avoids double-counting embedded sections in the
total context figures.

| Rank | Candidate | Measured size | Draft trigger phrase |
|---:|---|---:|---|
| 1 | Node-local hardware/topology facts in `CLAUDE.local.md` | 93,100 B | “Need node-local topology or hardware” |
| 2 | Universal doctrine in `CLAUDE.md` | 67,548 B | “Need mesh-wide operating rules” |
| 3 | Verification-principle cases/rules | 17,056 B | “Need evidence or a verification gate” |
| 4 | Tooling catalog and capability wiring | 12,739 B | “Need to choose or wire a mesh tool” |
| 5 | Handoff/session lifecycle rules | 5,439 B | “Need clear, restore, or handoff state” |
| 6 | Board/chat/task-ledger protocol | 5,675 B | “Need post, dispatch, claim, or settle work” |
| 7 | Repository operator contract (`AGENTS.md`) | 4,700 B | “Need repository-local operating constraints” |

The first two candidates are the clear extraction wins by raw cost. They should be split by
triggered concern (hardware, networking, voice, Gmail, etc.) rather than copied wholesale. The
board and handoff sections are smaller but recur on coordination turns and are good candidates for
one compact protocol skill. No wiring or configuration change was made by this audit.

## Verification record

- `mesh-dash --once discover` completed at `2026-09-15T21:17:24Z`.
- `mesh-task check dispatch mesh-skills-20260915/audit-skills-landscape discover` exited 0.
- `MESH_TASK_ACTOR=discover mesh-task take mesh-skills-20260915 audit-skills-landscape` claimed the row.
- `find ... -name SKILL.md` enumerated 11 manifests; all passed the non-empty frontmatter check.
- `/skills` existence and all three candidate trees were checked directly with `find`.
- No files outside this receipt were written.

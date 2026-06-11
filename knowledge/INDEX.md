# Knowledge Index — lte-workstation mesh

Last updated: 2026-06-11T18:40Z

## How to read

For a planted mesh: start with **Protocol** and **Architecture**, then your specific interests.
For the operator: start with **WHERE-TO-READ** (in `.mesh/knowledge/`), then **Philosophy**.

---

## Doc types

| Location | Visibility | Purpose |
|----------|-----------|---------|
| `knowledge/` (repo) | Git-tracked, inherited by every clone | Verdicts, audits, security, canonical patterns |
| `~/.mesh/knowledge/` | Gossiped node-to-node, gitignored | Living doctrine, operator directives, node-specific affordances |

---

## Repo `knowledge/` — indexed by theme

### Genome & tool audits
| Doc | Hook |
|-----|------|
| `genome-lean-A-verdict.md` | 8 unwired scripts classified: 7 KEEP, 1 SUPERSEDED (health-watch) |
| `genome-lean-B-verdict.md` | Second batch of 8 unwired scripts verdicts |
| `deployed-side-audit-2026-06-11.md` | Deployed-binary ↔ genome parity audit |
| `deployed-side-cleanup-2026-06-11.md` | Removed stale deployed-only helpers from ~/.local/bin |
| `router-collision-live-check-2026-06-11.md` | GL-MT3000 old vs new IP collision verification |

### Security
| Doc | Hook |
|-----|------|
| `secrets-at-rest-audit-20260611.md` | Full inventory of mesh secret files, perms, git leaks, remediation plan |
| `ssh-least-privilege.md` | Audit + design: per-purpose SSH keys with forced-commands (blast radius analysis) |

### Theory & patterns
| Doc | Hook |
|-----|------|
| `stream-pattern.md` | THE universal pattern: source→reflex-pull→filter→conditional-keystroke-feed |
| `control-theory-application.md` | Bang-bang→I-controller for mesh-revive escalation; P-controller for adaptive tick cadence |
| `chaos-drill-runbook.md` | First supervised-reflex chaos drill procedure |

### Operations & verification
| Doc | Hook |
|-----|------|
| `board-timerepair-verification-2026-06-11.md` | Verifier-mission artifact for the timerepair board check |
| `capability-sweep-ideapad-lid-2026-06-11.md` | IdeaPad ACPI lid switch sensor capability sweep |

### Superseded / attic
| Doc | Status |
|-----|--------|
| (none yet) | — |

---

## `.mesh/knowledge/` — gossiped themes (selective, for reference)

### Philosophy & architecture (operator directives)
`autonomy-architecture` · `capabilities-are-text` · `capability-live-contract` ·
`divisible-self-and-roles` · `fungible-remote-inference` · `intrinsic-telos-and-no-self` ·
`no-fixed-mind-stigmergic-skeleton` · `orchestra-and-dance` · `project-mission-and-stewardship` ·
`reflex-doctrine` · `steward-as-role` · `threads-mortal-resurrection-always` ·
`trust-in-the-mesh` · `commit-to-main-no-prs` · `text-over-any-channel` ·
`text-streams-self-organize` · `single-write-fanout` · `smooth-onboarding-and-clocks`

### Operations & resilience
`how-nodes-breathe` · `node-self-care` · `reboot-survival-breathing` ·
`reflex-checks-reflex` · `resilience-exit-node-spof` · `resilience-map` ·
`runbook` · `survival-without-brains` · `mind-failover-borrowed-brain` ·
`fluid-egress` · `mycelium-resilience-and-topology` · `mesh-delegation` ·
`agent-load-accounting` · `ONBOARDING`

### Nodes & topology
`mesh-capability-map` · `mesh-inventory-and-compositions` ·
`discovered-affordances-2026-06-09` · `ilya-affordances` ·
`router-node-and-vpn-egress` · `blocker-ilya-egress`

### Organs & capabilities
`browser-as-organ` · `organ-research-program` · `organ-status-2026-06-09` ·
`organism-roadmap` · `capability-sweep-ideapad-screen-2026-06-11` ·
`mic-default-device-broken` · `presence-zone-inference`

### Theory & research
`control-theory-application` · `fields-to-mine` · `free-inference-pools` ·
`idle-is-capability-discovery` · `informed-consent-by-owner` ·
`persistence-code-git-text-gossip` · `prefer-free-model-for-runtime-loops` ·
`self-maintenance-and-development`

### Security
`ssh-least-privilege-design` · `mesh-secrets-scheme` · `threat-model`

### TMux
`tmux-append-only` · `tmux-is-the-only-window` · `tmux-native` ·
`channels-and-context-routing`

### Reports
`chaos-drill-report-2026-06-11` · `postmortem-2026-06-09-egress-outage`

### Navigation
`WHERE-TO-READ.md` · `MEMORY.md`

---

## Duplicate / overlap notes

| Name | Locations | Verdict |
|------|-----------|---------|
| `capability-sweep-ideapad-lid-2026-06-11.md` | `knowledge/` + `.mesh/knowledge/` | Same file; repo copy is the canonical artifact, .mesh copy is gossiped |
| `control-theory-application.md` | `knowledge/` + `.mesh/knowledge/` | Different authors: repo has ilya-mind field investigation, .mesh has steward application design. Keep both — complementary |
| `ssh-least-privilege.md` vs `ssh-least-privilege-design.md` | `knowledge/` vs `.mesh/knowledge/` | Different: audit summary vs design document. Keep both |
| `ONBOARDING.md` vs `node-onboarding.md` | `.mesh/knowledge/` | Possible overlap: ONBOARDING is the protocol, node-onboarding is the operator design. Verify |

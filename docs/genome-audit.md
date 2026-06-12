# Genome audit — what blocks planting an INDEPENDENT mesh (steward, 2026-06-09)

Operator's observation (read the repo before sleep): the "genome" hardcodes OUR specifics, so a
stranger can't cleanly plant their **own autonomous mesh** from it. This audit (grep-based) confirms
it and proposes the split. Goal: anyone clones → plants a working, independent mesh with **zero code
edits**; our specifics live in a node-local config, never in the genome.

## Findings (tracked files)
- **~38 hardcoded IPs** (our Tailscale `100.x` + LAN `192.168.8.x`) across `*.sh`, `*.md`, `scripts/*`.
- **Our hostnames / usernames** (`imozerov-*`, `Default-string`, `Redmi`, `imozerov@`, `u0_a380` live; `u0_a386` legacy) in:
  CLAUDE.md, README.md, PROGRESS.md, docs/*, and scripts: mesh-conn, mesh-morning, mesh-fix-egress,
  mesh-health, mesh-minds, mesh-census, mesh-converse, mesh-ear, mesh-blessyou, genius-loci, …
- **bootstrap.sh**: parameterized (`PEER=${1:-${MESH_PEER:-100.125.157.75}}`) but the *default* is our IP.

## The split (generic SKELETON vs node-local CONFIG)
1. **Node registry → config, not code.** Introduce `~/.mesh/nodes` (gitignored) + `nodes.example`:
   the peer IP(s), node labels, output targets. Scripts that hardcode peers/node-lists (mesh-conn
   `MESH_PEER`, mesh-morning `NODES`, mesh-voice-tx `BOSE_NODE`, mesh-verify `NODES`, mesh-organs,
   mesh-fix-egress, heartbeat `HB_PEER`) read from it OR derive from `tailscale status` at runtime.
   Many already honor an env var — just remove the *our-IP defaults* and source the config.
2. **CLAUDE.md = generic doctrine + node-local context.** Today it's 100% our topology. Split into:
   a generic `CLAUDE.md` (the kernel doctrine, conventions, mesh-* tool contracts — plantable) and a
   `~/.mesh/operator-context.md` (or `CLAUDE.local.md`, gitignored) holding our nodes/services/IPs.
3. **bootstrap.sh**: default `PEER` empty → first node needs no peer; a joiner passes their own.
4. **README/docs**: replace our concrete IPs/hostnames with `<your-peer>` placeholders + a "plant your
   own mesh" quickstart.
5. **Keep nothing of ours lost** — everything specific moves into the gitignored node-local config
   (with an `.example`), not deleted.

## Verification (the slime-mold test for the genome)
Clone the repo on a FRESH machine with NO knowledge of our nodes → `bootstrap.sh` → a working,
independent single-node mesh that can grow, never touching our IPs. (Do as a careful, part-by-part
PR; steward reviews + commits — agents don't commit.)

Status: AUDIT done (this file). Refactor = the dispatched gh-agent task, landed via steward review.

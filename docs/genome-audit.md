# Genome audit — historical record of the genome de-personalization (2026-06-09 → resolved)

Operator's observation (read the repo before sleep): the "genome" hardcodes OUR specifics, so a
stranger can't cleanly plant their **own autonomous mesh** from it. This audit (grep-based) confirms
it and proposes the split. Goal: anyone clones → plants a working, independent mesh with **zero code
edits**; our specifics live in a node-local config, never in the genome.

All findings below are **historical** — resolved via the refactor that followed. Verified clean:

## Findings (tracked files — all resolved as of 2026-06-16)
- ~~**~38 hardcoded IPs** (our Tailscale `100.x` + LAN `192.168.8.x`) across `*.sh`, `*.md`, `scripts/*`.~~
  → **RESOLVED: zero hardcoded IPs remain.** All scripts use `~/.mesh/nodes` + `mesh-peer-addr` for
  dynamic resolution at runtime.
- ~~**Our hostnames / usernames** (`imozerov-*`, `Default-string`, `Redmi`, `imozerov@`, `<phone-user>`)
  in CLAUDE.md, README.md, PROGRESS.md, docs/*, and scripts.~~
  → **RESOLVED: zero occurrences in code/scripts.** `CLAUDE.md` is now a generic skeleton;
  node-specific topology lives in `CLAUDE.local.md` (gitignored). PROGRESS.md changelog entries
  retain hostnames (historical record — acceptable).
- ~~**bootstrap.sh**: default `PEER` defaults to our IP.~~
   → **RESOLVED: `bootstrap.sh` (repo root) no longer contains a hardcoded default.** Parameterized via
   `MESH_PEER` env / explicit argument.

## The split (generic SKELETON vs node-local CONFIG — implemented)
1. **Node registry → config, not code.** `~/.mesh/nodes` (gitignored) + `nodes.example` exist.
   Scripts read peers from `~/.mesh/nodes` at runtime or derive from `tailscale status`.
2. **CLAUDE.md = generic doctrine + CLAUDE.local.md (node-local).** `CLAUDE.md` is the committed
   skeleton; node-specific topology, IPs, and credentials live in `CLAUDE.local.md` (gitignored).
3. **bootstrap.sh**: parameterized, no hardcoded default.
4. **README/docs**: no hardcoded IPs/hostnames remain. Placeholders used where needed.
5. **Nothing of ours lost** — everything specific moved into gitignored node-local config with
   `.example` templates.

## Verification (the slime-mold test for the genome)
Clone the repo on a FRESH machine with NO knowledge of our nodes → `bootstrap.sh` → a working,
independent single-node mesh that can grow, never touching our IPs. (Do as a careful, part-by-part
PR; steward reviews + commits — agents don't commit.)

## Periodic drift check
Re-run `rg -c '100\.(7[0-9]|[89][0-9]|1[01][0-9]|12[0-5])\.[0-9]{1,3}\.[0-9]{1,3}' scripts/` and
`rg -c 'imozerov|Default-string|Redmi' scripts/` to detect back-sliding. Zero hits = clean.

Status: AUDIT findings resolved. Verified zero hardcoded IPs/usernames in scripts (2026-06-16).
Re-check if new scripts are added.

## Post-audit drift (2026-06-18 re-check)

- **`scripts/mesh-say`**: `MAC_HOST` and `MAC_CHAIN` had hardcoded IPs (`192.168.8.214`, `100.73.170.56`).
  → **FIXED**: resolved via `mesh-peer-addr mac` + `tailscale status --self` dynamically.
- **`scripts/mesh-breath`**: `--test` fixture used our real IPs as test data (`100.73.170.56`,
  `38.49.216.141`, `192.168.8.146`).
  → **FIXED**: replaced with RFC 5735 documentation IPs (`203.0.113.0/24`, `198.51.100.0/24`).
  Test assertions updated accordingly.

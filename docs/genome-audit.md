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
`rg -c 'imozerov|Default-string|Redmi' scripts/` to detect back-sliding. **The clean test is NOT
"zero hits" anymore** (superseded — see the 2026-06-19 re-check below): the operator's 2026-06-15
genome-push policy accepts CGNAT (`100.64/10`) + RFC1918 IPs and structural device-name/label refs;
only **secret VALUES** and genuinely new personalization are drift. Triage each hit, don't gate on the raw count.

Status: AUDIT findings resolved. Verified zero hardcoded IPs/usernames in scripts (2026-06-16).
Re-check if new scripts are added.

## Post-audit drift (2026-06-18 re-check)

- **`scripts/mesh-say`**: `MAC_HOST` and `MAC_CHAIN` had hardcoded IPs (`192.168.8.214`, `100.73.170.56`).
  → **FIXED**: resolved via `mesh-peer-addr mac` + `tailscale status --self` dynamically.
- **`scripts/mesh-breath`**: `--test` fixture used our real IPs as test data (`100.73.170.56`,
  `38.49.216.141`, `192.168.8.146`).
  → **FIXED**: replaced with RFC 5735 documentation IPs (`203.0.113.0/24`, `198.51.100.0/24`).
  Test assertions updated accordingly.

## 2026-06-19 re-check (the "zero hits" claim has drifted — found + reconciled)
Ran the two drift-check commands above against current `scripts/`. **Both return non-zero** — the
absolute "zero hits / zero occurrences" claims (lines above, written 2026-06-16) are no longer
literally true. Triaged:
- **Hardcoded CGNAT IPs — 4 files, all post-audit scripts**: `mesh-travels` (`PHAEDRA = "root@100.94.116.17"`,
  no env fallback), `mesh-node-care` + `mesh-phone-collect` + `mesh-tg-watchdog` (CGNAT IPs as
  `${ENV:-default}` fallbacks). These DID re-introduce our specifics — line 43's "re-check if new
  scripts are added" warning was prescient. **Accepted, not a defect**: they are CGNAT (`100.64/10`),
  which the operator's 2026-06-15 push policy explicitly permits, and all but `mesh-travels` are
  env-overridable. (Optional hardening: give `mesh-travels` an `${MESH_*:-}` env override too.)
- **`imozerov|Default-string|Redmi` — ~40 files**: mostly **legitimate structural refs**, NOT
  re-personalization: `mesh-peer-addr Redmi` device-name lookups (the registry key, resolved at
  runtime), hostname→friendly-label maps (`mesh-fleet-health`: `imozerov-IdeaPad-…) echo "IdeaPad"`),
  and `PHONE_USER:-u0_a380` defaults. A stranger cloning still gets a working mesh (these resolve via
  their own `~/.mesh/nodes`); the device-NAME constants are the registry contract, not our IPs.

Verdict: the genome de-personalization HOLDS for its real goal (zero secret values; a stranger plants
cleanly). The doc's *historical* findings are accurate; only its "zero hits = clean" drift-test was
stale and is corrected above. No code change made under this doc-drift task.

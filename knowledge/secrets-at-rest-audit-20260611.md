# SECURITY: secrets-at-rest audit — 2026-06-11T14:30Z

**Node:** imozerov-IdeaPad-3-15IIL05

## CLEAN (permissions 0600, not git-tracked)

| # | File | Contents | Perms | Git |
|---|------|----------|-------|-----|
| 1 | `~/.mesh/secrets/tailscale.env` | TS_API_KEY, TS_AUTHKEY | 0600 | no |
| 2 | `~/.config/remote-access/env` | BOT_TOKEN, CHAT_ID, MTG_SECRET | 0600 | no |
| 3 | `~/.ssh/id_ed25519` | SSH private key | 0600 | no |
| 4 | `~/.config/foxible/changelog.env` | TELEGRAM_BOT_TOKEN | 0600 | no |
| 5 | `~/.wg-mesh-nodes.json` | WG mesh config | 0600 | no |
| 6 | `~/.config/sops/age/keys.txt` | age node private key | 0600 | no |
| 7 | `~/.config/yandex-cloud/logs/*` (25 files) | yc IAM create-token logs | 0600 (dir 0700) | no |
| 8 | `~/.ssh/authorized_keys` | SSH pub keys | 0600 | no |

## FAIL: PERMISSIONS (not 0600)

| # | File | Current | Should | Risk |
|---|------|---------|--------|------|
| 9 | `~/.gemini/` (dir) | **0775** | 0700 | group can list + read OAuth state |
| 10 | `~/.gemini/google_accounts.json` | **0664** | 0600 | group-readable OAuth account data |
| 11 | `~/.gemini/state.json` | **0664** | 0600 | session state tokens |
| 12 | `~/.gemini/settings.json` | **0664** | 0600 | OAuth config |
| 13 | `~/.gemini/projects.json` | **0664** | 0600 | project metadata |
| 14 | `~/.gemini/installation_id` | **0664** | 0600 | install fingerprint |
| 15 | `~/.mesh/` (dir) | **0775** | 0700 | group can read ALL logs below |
| 16 | `~/.mesh/nodes` | **0664** | 0600 | peer topology (perimeter) |

## FAIL: SECRETS IN LOGS (cleartext, group-readable)

All `~/.mesh/*.log` files are **0664** and contain cleartext secrets:

| # | File | What leaked |
|---|------|-------------|
| 17 | `~/.mesh/chat.log` | BOT_TOKEN fragments, OAuth codes |
| 18 | `~/.mesh/traces.log` | OAuth callback URLs with codes |
| 19 | `~/.mesh/voice-in.log` | sudo passwords in plaintext, OAuth URLs with tokens |
| 20 | `~/.mesh/textin.log` | OAuth auth codes (`code=ac_...`) |

Root cause: `mesh-voice-rx`, `mesh-tg-recv`, `mesh-textin` echo raw input (including
secrets the operator typed/pasted) into shared log files. Log files are 0664 → anyone
in the `imozerov` group can read them.

## FAIL: RECOVERY KEY STILL ON DISK

| # | File | Risk |
|---|------|------|
| 21 | `~/RECOVERY-age-key-MOVE-OFFMESH.txt` | **Root-of-trust offline recovery age key STILL on IdeaPad disk** (0600, but the entire point of this key is it should be OFF-MESH — password manager, printed, or encrypted Telegram Saved Messages) |

## GIT: INTENTIONAL (no actual secrets, confirmed)

| # | File | Contents |
|---|------|----------|
| — | `.sops.yaml` | age **public** keys (safe for public repo per its own doc) |
| — | `docs/secrets.md` | documentation — no secrets |
| — | `knowledge/mesh-secrets-scheme.md` | documentation — no secrets |

## .gitignore coverage

Patterns: `.env`, `*.env`, `env`, `secrets/`, `CLAUDE.local.md`, `nodes.local`
→ Adequate for the repo. `~/.mesh/secrets/` is outside the repo tree (HOME-level) — correct, no risk of accidental commit.

---

## DESIGN: remediation plan (operator-gated, no changes by auditor)

### Phase 1 — immediate perms fix (one-liner, idempotent)

```bash
chmod 700 ~/.gemini/ ~/.mesh/
chmod 600 ~/.gemini/{google_accounts.json,state.json,settings.json,projects.json,installation_id}
chmod 600 ~/.mesh/nodes ~/.mesh/*.log
```

### Phase 2 — move recovery key off-mesh

```bash
# Operator moves the content to password manager / printed / encrypted Telegram
cat ~/RECOVERY-age-key-MOVE-OFFMESH.txt
# Then shred:
shred -u ~/RECOVERY-age-key-MOVE-OFFMESH.txt
```

### Phase 3 — log sanitization (tooling changes, steward lands in genome)

Add a sanitizer pass to every secret-ingesting reflex (`mesh-voice-rx`, `mesh-tg-recv`,
`mesh-textin`, `mesh-chat`, `mesh-trace`):

- Strip `BOT_TOKEN=` values before logging
- Strip OAuth `code=`, `state=` parameters from URLs
- Strip anything matching `\b[a-zA-Z0-9_-]{35,}\b` that looks like a token
- Consider a shared `mesh-sanitize` helper sourced by all ingest scripts

Alternatively: pipe all incoming text through a sanitizer regex before logging:

```
| sed -E 's/(BOT_TOKEN|code|state|password)=[^ &]+/\1=REDACTED/gi'
```

### Phase 4 — log rotation + retention

```
# Rotate logs daily, keep 7 days
logrotate ~/.mesh/*.log with daily + rotate 7
```

Combined with perms fix (0600), this limits the blast radius of any future secret leak
into logs.

### Phase 5 — shared secrets hydration audit (cross-node)

Run the same audit on `imozerov-default-string` (100.125.157.75) and `ilya`
(100.107.198.111) — they also hold `~/.config/remote-access/env` (or equivalent),
age keys, and log files.

## Status

| Category | Count |
|----------|-------|
| CLEAN | 8 files |
| PERM VIOLATION (0664/0775) | 8 items |
| SECRETS IN LOGS | 4 log files |
| RECOVERY KEY ON DISK | 1 file |
| GIT LEAK | 0 |

**Verdict:** No git leaks. Core secret files are 0600. Blast radius: 8 permission
violations (Gemini dir + files, .mesh/ dir + nodes + logs), 4 log files with
cleartext secrets, and the off-mesh recovery key not yet moved.

# Hire submission test receipt — 2026-09-08 17:02Z

- Trigger: board message `d7266aca9e009c19`; terminal acknowledgement sent.
- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`); author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`.
- Acceptance: `ACCEPT` on `trovu/trovu`; required rule files `AGENTS.md`, `README.md`.
- Credential check: `ABSENT` — `/home/mesh-home/.mesh/secrets/github-hire.env` is absent.
- Test command: `./scripts/mesh-hire-submit --test`.
- Result: exit `2`, the documented credential-organ absent state.
- Outward action: none; `--send` was not run.
- Funnel position: blocked pending a replacement classic PAT for `ghIsPureTrash` with exactly
  `public_repo`, stored mode `600` as `GH_HIRE_TOKEN` in the credential file.

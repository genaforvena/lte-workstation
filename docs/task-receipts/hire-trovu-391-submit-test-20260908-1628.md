# Hire submission test receipt — 2026-09-08 16:28Z

- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`); author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`.
- Acceptance: `ACCEPT` on `trovu/trovu`; fresh rule files read: `AGENTS.md`, `README.md`.
- Credential: `ABSENT` — `/home/mesh-home/.mesh/secrets/github-hire.env` does not exist; no lane token was available in `GH_HIRE_TOKEN`.
- Test command: `rtk ./scripts/mesh-hire-submit --test`
- Result: exit `2`, the documented credential-organ absence state.
- Identity/scope: not inspected because no dedicated token exists. The available `gh` login is `genaforvena` with broader scopes and was not used.
- Outward action: none; `--send` was not run.
- Funnel position: ready-to-send, blocked only on operator provisioning a dedicated classic PAT for `ghIsPureTrash` with `public_repo` only, stored mode `600` as `GH_HIRE_TOKEN` in the credential file.

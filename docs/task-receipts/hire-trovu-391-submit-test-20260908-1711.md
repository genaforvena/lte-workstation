# Hire submission test — 2026-09-08 17:11Z

- Trigger: board message `c4a241afc3259c60`; terminal acknowledgement sent.
- Command: `rtk ./scripts/mesh-hire-submit --test msg:c4a241afc3259c60`
- Package: `OK`; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`.
- Acceptance: `ACCEPT` on `trovu/trovu`; rule files `AGENTS.md README.md`.
- Credential: `ABSENT` at `/home/mesh-home/.mesh/secrets/github-hire.env`.
- Result: exit `2` (expected credential-gate failure).
- Outward action: none; `--send` was not run.
- Funnel position: still blocked at dedicated `GH_HIRE_TOKEN` provisioning.

# Hire submission gate receipt — trovu/trovu#391

- Timestamp: 2026-09-08T16:11Z
- Command: `rtk ./scripts/mesh-hire-submit --test`
- Exit: `2`
- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`)
- Acceptance: `ACCEPT` on `trovu/trovu` (`AGENTS.md`, `README.md`)
- Credential: `ABSENT` — `/home/mesh-home/.mesh/secrets/github-hire.env` is not present
- Credential inventory: `/home/mesh-home/.mesh/secrets` contains only `tailscale.env`; no `GH_HIRE_TOKEN` environment variable was present
- Outward action: none; `--send` was not run

The funnel remains blocked only on the operator provisioning the dedicated `ghIsPureTrash`
classic PAT with `public_repo` scope and mode `600`. No other credential was reused.

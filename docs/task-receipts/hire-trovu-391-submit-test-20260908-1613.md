# Hire submission gate receipt — trovu/trovu#391

- Timestamp: 2026-09-08T16:13:07Z
- Command: `rtk ./scripts/mesh-hire-submit --test`
- Exit: `2`
- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`)
- Acceptance: `ACCEPT` on `trovu/trovu` (`AGENTS.md`, `README.md`)
- Credential: `ABSENT` — `/home/mesh-home/.mesh/secrets/github-hire.env` is not present
- Credential mode check: not applicable; no file exists
- Outward action: none; `--send` was not run

The funnel remains blocked on operator provisioning of the dedicated `ghIsPureTrash`
classic PAT with `public_repo` scope and mode `600`. The separate operator GitHub identity
was not reused.

# Hire submit test receipt — 2026-09-08 16:24 UTC

- Command: `rtk ./scripts/mesh-hire-submit --test`
- Exit: `2`
- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`)
- Acceptance: `ACCEPT` on `trovu/trovu` (`2` target files: `AGENTS.md`, `README.md`)
- Credential: `ABSENT` (`/home/mesh-home/.mesh/secrets/github-hire.env`)
- Outward action: none; `--send` was not run.

The funnel remains blocked on operator provisioning of the dedicated `ghIsPureTrash`
classic PAT with `public_repo` only, stored mode `600`. After provisioning, rerun the
test and inspect identity/scope before any send.

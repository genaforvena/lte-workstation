# Hire credential re-check — 2026-09-08 17:05Z

- Trigger: board message `6a7454082dc47b2a`; terminal acknowledgement sent.
- Requested action: provision a dedicated classic PAT for `ghIsPureTrash` with exactly `public_repo` at `/home/mesh-home/.mesh/secrets/github-hire.env`, mode `600`, then rerun the submit test.
- Credential state: `ABSENT`; the secrets directory contains only `tailscale.env`.
- Identity safety check: the only configured GitHub login is `genaforvena` with scopes `gist`, `read:org`, `repo`, `workflow`; it was not used or copied because it is the operator's identity and exceeds the hire lane's scope.
- Test command: `./scripts/mesh-hire-submit --test`.
- Result: package `OK`, acceptance `ACCEPT`, credential `ABSENT`; exit `2`.
- Outward action: none; `--send` was not run.
- Funnel position: blocked at the dedicated `ghIsPureTrash` credential gate.

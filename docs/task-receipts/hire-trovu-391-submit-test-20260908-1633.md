# Hire submission gate receipt — trovu/trovu#391

- Timestamp: 2026-09-08T16:33:54Z
- Command: `rtk ./scripts/mesh-hire-submit --test`
- Exit: `2` (credential organ absent; package and acceptance gates passed)
- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`)
- Acceptance: `ACCEPT` on `trovu/trovu` (`AGENTS.md`, `README.md`)
- Credential: `ABSENT` — `/home/mesh-home/.mesh/secrets/github-hire.env` is not present
- Outward action: none; `--send` was not run
- Board acknowledgement: `ack:b4c2d2dc9d909876` posted to `hire`

The funnel remains blocked on operator provisioning of the dedicated `ghIsPureTrash`
classic PAT with `public_repo` scope and mode `600`.

Next exact action after provisioning:

```bash
rtk ./scripts/mesh-hire-submit --test
```

Run `--send` only if that test reports credential identity and scope `OK`.

# Hire submission gate receipt — trovu/trovu#391

- Timestamp: 2026-09-08T15:56Z
- Command: `scripts/mesh-hire-submit --test`
- Exit: `2`
- Package: `OK` (`/home/mesh-home/.mesh/hire/trovu-391`; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`)
- Acceptance: `ACCEPT` on `trovu/trovu` (`2` required files: `AGENTS.md`, `README.md`)
- Credential: `ABSENT` — `/home/mesh-home/.mesh/secrets/github-hire.env` is not present
- Outward action: none; `--send` was not run

Next action: provision the dedicated mode-600 credential containing `GH_HIRE_TOKEN`, rerun
`scripts/mesh-hire-submit --test`, and run `--send` only if the fresh identity and scope gates pass.

## Terminal receipt — 2026-09-08T16:06Z

- Receipt `29b43fa7caf5d02c` acknowledged on the hire board as `ack:29b43fa7caf5d02c`.
- Fresh `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`
  (`AGENTS.md`, `README.md`); exit `2`.
- Credential remains `ABSENT` at `/home/mesh-home/.mesh/secrets/github-hire.env`; no outward
  action occurred. Funnel remains ready-to-send and idle pending operator provisioning of the
  dedicated mode-600 `GH_HIRE_TOKEN` file.

## Recheck — 2026-09-08T15:58Z

- Operator receipt `ed5a2c4577251f43` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`
  (`AGENTS.md`, `README.md`).
- Credential gate: `ABSENT` at `/home/mesh-home/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none; `--send` was not run. Funnel position: ready-to-send, blocked only on
  provisioning the dedicated mode-600 `GH_HIRE_TOKEN` file, then rerunning `--test`.

## Recheck — 2026-09-08T15:59Z

- Fresh `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`
  (`AGENTS.md`, `README.md`).
- Credential gate: `ABSENT` at `/home/mesh-home/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none; `--send` was not run. Funnel remains ready-to-send and blocked only on
  provisioning the dedicated mode-600 file containing the lane identity's `GH_HIRE_TOKEN`.

## Recheck — 2026-09-08T16:09Z

- Terminal receipt `ea582a4bb106341d` acknowledged on the hire board.
- Fresh `rtk ./scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`
  (`AGENTS.md`, `README.md`).
- Credential gate: `ABSENT` at `/home/mesh-home/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none; `--send` was not run. Funnel remains ready-to-send and idle pending
  operator provisioning of the dedicated mode-600 `GH_HIRE_TOKEN` file.

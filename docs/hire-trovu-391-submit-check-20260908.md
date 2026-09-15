# Hire funnel check — trovu/trovu#391

- Checked: 2026-09-08T14:00:44Z
- Package: `~/.mesh/hire/trovu-391` — OK; author `ghIsPureTrash`; branch `warn-on-dot-in-keyword`
- Acceptance: `ACCEPT` on `trovu/trovu`; rule files read: `AGENTS.md`, `README.md`
- Credential: absent at `~/.mesh/secrets/github-hire.env`
- Command: `scripts/mesh-hire-submit --test`
- Exit: `2` (credential organ absent)
- Outward action: none; no disclosure comment, fork, push, or PR was made

Next action after the operator provisions the credential: rerun `scripts/mesh-hire-submit --test`,
then run `scripts/mesh-hire-submit --send` only if the fresh acceptance and identity/scope checks
remain green.

## Recheck — 2026-09-08T14:03Z

- `scripts/mesh-hire-submit --test` re-run: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential still `ABSENT`; exit `2`.
- Outward action: none. `--send` was not run because the dedicated credential is not present.

## Recheck — 2026-09-08T14:05Z

- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential file absent at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Receipt for operator message `3ba8ce0bb50f8dcc` acknowledged on the hire board.
- Outward action: none. `--send` remains blocked until the operator provisions the dedicated
  mode-600 credential containing `GH_HIRE_TOKEN`.

## Recheck — 2026-09-08T14:08Z

- Receipt `ac0e20ce06ffb364` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` was not run because the dedicated credential is still absent.
- Next action: operator provisions mode-600 `~/.mesh/secrets/github-hire.env` containing the
  dedicated `GH_HIRE_TOKEN`; then rerun `scripts/mesh-hire-submit --test` and send only if the
  fresh identity and scope checks pass.

## Recheck — 2026-09-08T14:09Z

- Receipt `11bcefd110328933` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` remains blocked because the operator has not provisioned the
  dedicated credential.

## Recheck — 2026-09-08T14:11Z

- Receipt `561184d073098f8f` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` remains blocked because the dedicated credential is still absent.
- Funnel position: ready-to-send package, waiting for the operator to provision the dedicated
  mode-600 `~/.mesh/secrets/github-hire.env` containing `GH_HIRE_TOKEN`.

## Recheck — 2026-09-08T14:14Z

- Receipt `44ba8a53143a7b37` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` remains blocked because
  `~/.mesh/secrets/github-hire.env` is still absent.
- Funnel position: ready-to-send; next action is to rerun `scripts/mesh-hire-submit --test`
  after the operator provisions mode-600 `GH_HIRE_TOKEN`, then run `--send` only if identity
  and scope checks pass.

## Recheck — 2026-09-08T14:18Z

- Receipt `b903ad05f736870b` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` remains blocked because the dedicated credential is still absent.
- Funnel position: ready-to-send; operator must provision mode-600
  `~/.mesh/secrets/github-hire.env` containing `GH_HIRE_TOKEN`, then rerun `--test` before any
  outward submission.

## Recheck — 2026-09-08T14:19Z

- Receipt `0c5071b4203c5ea9` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test` completed within a bounded 20-second run: package `OK`;
  acceptance `ACCEPT` on `trovu/trovu`; credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` remains blocked because
  `~/.mesh/secrets/github-hire.env` is absent; no token was created or read.
- Funnel position: ready-to-send; operator must provision mode-600 `GH_HIRE_TOKEN`, then rerun
  `--test` and send only if fresh identity and scope checks pass.

## Recheck — 2026-09-08T14:21Z

- Receipt `545fdd39d5c7096b` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT`; exit `2`.
- Outward action: none. `--send` was not run because
  `~/.mesh/secrets/github-hire.env` is absent; no token was created or read.
- Funnel position: ready-to-send, blocked only on the operator provisioning mode-600
  `GH_HIRE_TOKEN`; next action is rerun `--test`, then `--send` only if fresh identity and
  scope checks pass.

## Recheck — 2026-09-08T14:27Z

- Receipt `9f3385374bd80bfe` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none. `--send` remains blocked because the dedicated `GH_HIRE_TOKEN` is not
  provisioned; no token was created or read.
- Funnel position: ready-to-send; operator provisioning of the dedicated mode-600 credential is
  the sole open gate, after which rerun `--test` before any outward submission.

## Recheck — 2026-09-08T14:31Z

- Receipt `a1d8ff2c078c7dc5` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none. `--send` was not run because the dedicated `GH_HIRE_TOKEN` is not
  provisioned; no token was created or read.
- Funnel position: ready-to-send; operator provisioning of the mode-600 credential is the sole
  open gate, after which rerun `--test` and send only if fresh identity/scope checks pass.

## Recheck — 2026-09-08T14:33Z

- Receipt `d34709ea57793d52` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none. `--send` was not run because the dedicated `GH_HIRE_TOKEN` is not
  provisioned.
- Funnel position: ready-to-send; the sole open gate is the operator provisioning the mode-600
  credential, after which rerun `--test` and send only if fresh identity/scope checks pass.

## Recheck — 2026-09-08T14:39Z

- Receipt `819d4a2d1513d84d` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`); credential file remains absent at `~/.mesh/secrets/github-hire.env`.
- Exit: `2` (credential organ absent). No `GH_HIRE_TOKEN` was present and no credential was
  created or read.
- Outward action: none. `--send` remains blocked until the operator provisions the dedicated
  mode-600 credential; then rerun `--test` and send only if identity and scope checks pass.

## Recheck — 2026-09-08T14:36Z

- Receipt `2dd31f7404c82b12` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`); credential file remains absent at `~/.mesh/secrets/github-hire.env`.
- Exit: `2` (credential organ absent). No `GH_HIRE_TOKEN` was present in the environment and no
  credential was created or read.
- Outward action: none. `--send` remains blocked until the operator provisions the dedicated
  mode-600 credential; then rerun `--test` and send only if identity/scope checks remain green.

## Recheck — 2026-09-08T15:05Z

- Receipt `a8905cc7cb04b70f` acknowledged on the hire board.
- Exact command `scripts/mesh-hire-submit --test msg:a8905cc7cb04b70f`: package `OK`; acceptance
  `ACCEPT` on `trovu/trovu`; credential `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none. `--send` was not run; the operator must provision the dedicated mode-600
  credential containing `GH_HIRE_TOKEN` before the next test.

## Recheck — 2026-09-08T14:48Z

- Receipt `3c1ac8db0dadbe22` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Exit: `2` (credential organ absent). `~/.mesh/secrets/github-hire.env` is missing; no
  `GH_HIRE_TOKEN` was created or read.
- Outward action: none. `--send` remains blocked until the operator provisions the dedicated
  mode-600 credential; then rerun `--test` and send only if identity/scope checks remain green.

## Recheck — 2026-09-08T15:07Z

- Receipt `3bfdb5c4c2dd0565` acknowledged on the hire board.
- Package remains ready: `trovu/trovu#391` package `OK`; acceptance `ACCEPT`.
- Credential file remains absent at `~/.mesh/secrets/github-hire.env`; no token was created or read.
- Outward action: none. `--send` remains blocked until the operator provisions the dedicated
  mode-600 credential containing `GH_HIRE_TOKEN`, then reruns `--test`.

## Recheck — 2026-09-08T15:08Z

- Receipt `b1443cf55d310e03` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read, and no outward action occurred.
- Funnel remains ready-to-send and blocked only on the operator provisioning the dedicated mode-600
  credential containing `GH_HIRE_TOKEN`; rerun `--test` before any `--send`.

## Recheck — 2026-09-08T15:53Z

- Receipt `2f92cc40c17e0bca` acknowledged on the hire board.
- Fresh bounded `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read.
- Outward action: none; `--send` was not run. Funnel remains ready-to-send and blocked only on
  the operator provisioning the dedicated mode-600 credential containing `GH_HIRE_TOKEN`, then
  rerunning `--test` before any outward submission.

## Recheck — 2026-09-08T15:48:33Z

- Receipt `3f0790cbecdf91eb` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read.
- Outward action: none; `--send` was not run. Funnel remains ready-to-send and blocked only on
  the operator provisioning the dedicated mode-600 credential containing `GH_HIRE_TOKEN`, then
  rerunning `--test` before any outward submission.

## Recheck — 2026-09-08T15:50Z

- Operator granted general approval to proceed.
- Fresh `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains absent at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Approval does not supply the dedicated GitHub credential. `--send` was skipped; no outward
  action occurred. The next action remains provisioning the mode-600 credential, then rerunning
  `--test` before `--send`.

## Recheck — 2026-09-08T15:50:22Z

- Receipt `b2c49bd91f86b73c` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains absent at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none; `--send` remains gated until the dedicated mode-600 credential containing
  `GH_HIRE_TOKEN` is provisioned.

## Recheck — 2026-09-08T15:51:12Z

- Receipt `6aa8b8d2dba478cd` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK`; acceptance `ACCEPT` on `trovu/trovu`;
  credential remains absent at `~/.mesh/secrets/github-hire.env`; exit `2`.
- Outward action: none; `--send` remains gated until the dedicated mode-600 credential containing
  `GH_HIRE_TOKEN` is provisioned.

## Recheck — 2026-09-08T15:39:38Z

- Receipt `3c1c8b685bbca1ce` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read, and no outward action occurred.
- Funnel remains ready-to-send and blocked only on the operator provisioning the dedicated mode-600
  credential containing `GH_HIRE_TOKEN`; rerun `--test` before any `--send`.

## Recheck — 2026-09-08T15:25Z

- Receipt `f6f1662a5043bd9e` acknowledged on the hire board.
- Exact command `scripts/mesh-hire-submit --test`: package `OK` (author `ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); fresh acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read, and no outward action occurred.
- Funnel remains ready-to-send and blocked only on the operator provisioning the dedicated mode-600
  credential containing `GH_HIRE_TOKEN`; rerun `--test`, then `--send` only if fresh identity and
  scope checks pass.

## Recheck — 2026-09-08T15:42Z

- Receipt `fe4b66d15c7798e` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read, and no outward action occurred.
- Funnel remains ready-to-send; the sole open gate is operator provisioning of the dedicated mode-600
  credential containing `GH_HIRE_TOKEN`, followed by another `--test` before any `--send`.

## Recheck — 2026-09-08T15:47:21Z

- Receipt `1de803e4fde0e734` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; no token was created or read.
- Outward action: none; `--send` remains blocked until the operator provisions the dedicated
  mode-600 credential containing `GH_HIRE_TOKEN`.
- Funnel position: ready-to-send and idle; next action is rerun `--test`, then run `--send` only
  if fresh identity and scope checks pass.

## Recheck — 2026-09-08T15:30Z

- Receipt `b35fdeb01d9d81c0` acknowledged on the hire board.
- Exact command `scripts/mesh-hire-submit --test`: package `OK` (author `ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); fresh acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read.
- Outward action: none; `--send` was not run. Funnel remains ready-to-send and blocked only on
  the operator provisioning the dedicated mode-600 credential containing `GH_HIRE_TOKEN`, then
  rerunning `--test` before any outward submission.

## Recheck — 2026-09-08T15:44:37Z

- Receipt `fe4be66d15c7798e` acknowledged on the hire board.
- Fresh `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); acceptance `ACCEPT` on `trovu/trovu` (rule files `AGENTS.md`,
  `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read.
- Outward action: none; `--send` was not run. Funnel remains ready-to-send and blocked only on
  the operator provisioning the dedicated mode-600 credential containing `GH_HIRE_TOKEN`, then
  rerunning `--test` before any outward submission.

## Recheck — 2026-09-08T15:20Z

- Receipt `1dd724973b1767e8` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); fresh acceptance `ACCEPT` on `trovu/trovu` (rule files
  `AGENTS.md`, `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read, and no outward action occurred.
- Funnel remains ready-to-send and blocked only on the operator provisioning the dedicated mode-600
  credential containing `GH_HIRE_TOKEN`; rerun `--test`, then `--send` only if fresh identity and
  scope checks pass.

## Recheck — 2026-09-08T15:13Z

- Receipt `344cda7e67c60921` acknowledged on the hire board.
- `scripts/mesh-hire-submit --test`: package `OK` (`ghIsPureTrash`, branch
  `warn-on-dot-in-keyword`); fresh acceptance `ACCEPT` on `trovu/trovu` (rule files
  `AGENTS.md`, `README.md`).
- Credential gate: `ABSENT` at `~/.mesh/secrets/github-hire.env`; exit `2`. No token was created
  or read, and no outward action occurred.
- Funnel remains ready-to-send and blocked only on the operator provisioning the dedicated mode-600
  credential containing `GH_HIRE_TOKEN`; rerun `--test` before any `--send`.

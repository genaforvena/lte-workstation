# Hire submission gate receipt — trovu/trovu#391

- Lane: `hire`
- Captured: `2026-09-08T14:46:00Z`
- Command: `scripts/mesh-hire-submit --test`
- Exit: `2`
- Outward action: none; `--send` was not run.

## Gate result

```text
package: OK (/home/mesh-home/.mesh/hire/trovu-391, author=ghIsPureTrash, branch=warn-on-dot-in-keyword)
acceptance: ACCEPT on trovu/trovu (2 (AGENTS.md README.md))
credential: ABSENT (/home/mesh-home/.mesh/secrets/github-hire.env) — the operator's step, nothing else to do here
```

The only failing gate is the operator-owned GitHub credential organ. The expected file is absent;
therefore token identity and scope could not be checked, and no comment, fork, push, or pull
request was attempted. The package identity is `ghIsPureTrash`; the target rule files were freshly
read and accepted by `mesh-hire-scan`.

## Exact next action

After the operator provisions mode-600 `~/.mesh/secrets/github-hire.env` with the dedicated
`GH_HIRE_TOKEN`, rerun:

```text
scripts/mesh-hire-submit --test
```

Run `scripts/mesh-hire-submit --send` only if that fresh test also reports the expected token
identity and an allowed `public_repo` or `repo` scope.

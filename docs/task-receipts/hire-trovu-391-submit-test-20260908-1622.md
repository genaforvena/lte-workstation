# Hire receipt — trovu#391 submission test

- Time: 2026-09-08T16:22Z
- Receipt acknowledged: `ack:b1e26f036c3047e9`
- Command: `./scripts/mesh-hire-submit --test`
- Result: exit `2` (credential gate; no outward submission)

Observed output:

```text
package: OK (/home/mesh-home/.mesh/hire/trovu-391, author=ghIsPureTrash, branch=warn-on-dot-in-keyword)
acceptance: ACCEPT on trovu/trovu (2 (AGENTS.md README.md))
credential: ABSENT (/home/mesh-home/.mesh/secrets/github-hire.env) — the operator's step, nothing else to do here
```

The prepared package is valid and names `ghIsPureTrash`; the target scanner currently accepts the
lane. The required operator-provisioned mode-600 credential file is absent, so `--send` was not run.
The next action is to provision that file with a classic `public_repo` token, then rerun this test
and send only if the API identity and scopes match.

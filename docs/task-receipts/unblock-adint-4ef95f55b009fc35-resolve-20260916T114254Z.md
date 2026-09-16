# adint unblock-resolution receipt — 2026-09-16T11:42:54Z

Task: `unblock/adint/4ef95f55b009fc35/resolve`
Owner: `adint`
Parent: `unblock/health/47f1ba654a52aca9/resolve`

## Fresh read-only verification

- `mesh-health --once` exited `0` at `2026-09-16T11:42:54Z`; `imac-rozalia`
  (`100.121.88.110`) was reported `PASS`.
- Bounded probe:

  ```text
  timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true
  mesh-home@100.121.88.110: Permission denied (publickey,password,keyboard-interactive).
  ```

  Exit status: `255`.

Transport/reachability is present, but the authorized SSH credential is still refused. No remote
credential, SSH configuration, router state, or substrate state was changed.

## Disposition

Concrete `external-event` block remains: an authorized administrator must correct or authorize the
SSH key/account configuration on `imac-rozalia`.

## Exact retry edge

After that credential correction is explicitly evidenced, run:

```text
mesh-task check dispatch health-warning/8a568c80615a3a8320e9/triage health
mesh-health --once
timeout 12s ssh -o BatchMode=yes -o ConnectTimeout=5 100.121.88.110 true
```

Only a successful authorized SSH probe permits resuming the parent health triage.

# Reconcile stale Redmi frontier health warning

At 2026-09-14T19:01Z, triaged `health-warning/ca247f980b3920f1eef3/triage`,
which re-dispatched the 2026-09-11T20:03:13Z health FYI about the completed
`artifacts/discover/frontier-dry-20260911T1941Z.txt` sweep and the Redmi SSH gap.

## Evidence

- The frontier artifact says the sweep was dry: every reachable local surface was
  already catalogued, and Redmi was offline. No new capability was claimed.
- The exact Redmi retry already exists as
  `discover-redmi-termux-frontier-followup-20260914/retry-redmi-termux-frontier`,
  whose durable retry condition is
  `event:first-successful-redmi-ssh-port-8022-probe`.
- Its receipt, `task-receipts/discover-redmi-termux-frontier-followup-20260914.md`,
  records three bounded SSH timeouts at 09:24Z and confirms there was no command
  sample. The linked resolver
  `unblock/discover/0bc9bb716a55f76d/resolve` was rejected as an external
  prerequisite after checking the live paths; see
  `task-receipts/unblock-discover-redmi-8022-0bc9bb716a55f76d-20260914.md`.
- Fresh live state still shows Redmi 10 `Online=false`, peer `100.103.99.16`,
  `LastSeen=2026-09-03T09:53:36.1Z`; `mesh-health` reports it offline. No new
  reachability event justifies repeating the timed-out SSH probes.

## Disposition

Reject `health-warning/ca247f980b3920f1eef3/triage` as a stale duplicate of the
already represented frontier and exact blocked Redmi follow-up. No new prerequisite
can be created from this node: the next safe action is triggered only by the
observable event `first successful Redmi SSH port 8022 probe`. On that event,
resume the existing follow-up and run its remaining Termux candidates. Until then,
Redmi access remains a named external blind spot, not an uninvestigated health
warning.

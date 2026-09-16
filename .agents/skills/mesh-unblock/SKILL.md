---
name: mesh-unblock
description: Use when mesh-owned work is blocked by missing node resources, dependencies, contention, or recoverable runtime failures and the agent must proceed autonomously.
---

# Mesh unblock

Use this skill for work that can be completed with resources owned by the mesh node or
repository. The mesh chooses the resource, install path, retry timing, and recovery route;
a human is never a routine dependency or permanent blocker, and is not a routine
approver, chooser, or unblocker. Human or external action may be required only at
an explicit safety or authority boundary; it is then recorded as an external
boundary, not treated as ordinary task progress.

## Operating contract

- Inspect the repository, current task state, and live node evidence before deciding.
- Use available mesh-owned CPU, RAM, GPU, storage, network access, services, and peripherals
  within their declared safety boundaries. Prefer sharing, an alternate node/slot, or a
  bounded lease over stopping unrelated work.
- Install a missing dependency only when it is an allowed mesh/repository dependency and the
  installation is reversible or recorded. Verify the installed capability with the real tool
  path, not only a package-manager success message.
- For temporary scarcity or contention, record the measured condition, queue or defer the work,
  and retry with a bounded cadence. Re-check the resource before each retry; do not spin.
- If recovery cannot proceed, leave a typed machine-only block containing the exact failed
  predicate and the next retry event. “Ask the operator” is not a recovery strategy.
- Produce a durable artifact for every completed capability: a test result, output file, receipt,
  or other evidence that a later mind can inspect.

## Safety boundary

This skill authorizes autonomy only over mesh-owned node resources and repository-scoped work.
Do not terminate, reconfigure, or consume unrelated external processes, accounts, hosts, or
people's workloads. Do not change routing, DNS, firewall, VPN, credentials, claims, task
ownership, or other substrate state; hand those to their designated single writer. Do not hide
an unavailable organ behind a fabricated default or claim success from reachability alone.

## Minimal decision loop

1. Name the blocked predicate and inspect the live evidence that proves it.
2. Choose one safe local recovery: share, install, alternate resource, bounded lease, queue, or
   retry.
3. Execute it and verify the real artifact.
4. If it fails, preserve the evidence and next retry event as a typed block.

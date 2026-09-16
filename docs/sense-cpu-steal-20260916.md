# CPU steal sense — live artifact

- Observed: `2026-09-16T00:44:41Z`
- Probe: `scripts/mesh-cpu-steal`
- Source: Linux `/proc/stat`, aggregate `cpu` row, steal-time jiffies
- Live result: `CLEAR`, `total_jiffies=0`, `delta_jiffies=0`, `window_ms=250`
- Interpretation: this node reported no CPU time stolen by a hypervisor during the sample; this is a real zero, not a fallback.
- Honest failure: unreadable or malformed `/proc/stat` exits `2` and writes no reading.
- Verification: `tests/test-mesh-cpu-steal.sh` passed; `scripts/mesh-cpu-steal --test` passed with a real `/proc/stat` read.
- Wiring: intentionally on-demand while uncommitted; `mesh-autowire` refused the working-tree source under the tracked-at-HEAD gate. No commit made.

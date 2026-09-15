# Addendum: load spike settled after the triage receipt

This addendum preserves later evidence without changing the completed task artifact
`health-warning-1dd6d282dffb54b6e468-20260912.md` (ledger SHA-256 remains
`bb74ef5639b6db4277a58fc51208d5e3ddf365584b0f430a57881d9e6ab350ec`).

At 13:25Z, `mesh-dash --once check` showed a sharp transient: `load=102.60/16`,
`load1=133.09/16`, CPU `red` at 79% frequency. The simultaneous process snapshot showed many
ledger queue scans, Whisper/audio work, and Ollama activity, but did not isolate one cause. At
13:26Z, a read-only `mesh-resource-guard` pass reported 15,223 MiB available, 993 MiB swap free,
and node `OK`; it also retained node-omega accumulation and a `NODE-CRITICALITY` warning. The
transient load had eased by that sample. No process was killed or reniced.

The resource reflex remains wired and live: cron journal records the 13:24 and 13:26 `--alert`
runs, and `.resource-guard-state` was freshly updated with `OK`. Its `resource-guard.log` is an
alert-output log, so its older mtime alone does not indicate a dead reflex. The separate 12:37Z
global OOM remains real; its Python command line and exact pressure-crossing time are not retained,
so attribution and gaps between the two-minute samples remain known limitations. This addendum does
not change the original task verdict or its recorded evidence hash.

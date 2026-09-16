# Health-warning triage: JUNK-LOAD at chat.log line 60964

Task: `health-warning/junk-load-20260916/triage`
Owner: `health`
Observed warning: `~/.mesh/chat.log` physical line 60964, 2026-09-13T20:12:20Z:
`[JUNK-LOAD] CPU=JUNK-LOAD · GPU=GPU-IDLE · top=python[?] 93.0% · load1=18.52/16c`.

## Current non-destructive recheck

At 2026-09-16T07:02:44Z, `mesh-load-audit --json` returned rc 0 and reported:

```json
{"label":"ORGAN-LOAD","cpu_label":"ORGAN-LOAD","cpu_reason":"top CPU=python[organ] 354.5% (known workload — build/inference)","gpu_label":"GPU-IDLE","load1":26.97,"nproc":16,"top_cpu":354.5,"top_comm":"python","cpu_inst":354.5,"cpu_iv":82.6,"top_comm_iv":"python","won":"inst","impossible_rows":0,"node_conn":1}
```

The independent process check at the same recheck found PID 2015364 running:
`.venv/bin/python main.py --low-memory /tmp/tmp.um1S0FHUMs/norm.mp3 /tmp/tmp.um1S0FHUMs/out/ amc l 120 w 4 ss 1.0 s 0.75 c 100,8000 m poly pr 5 rv 0.15 env 25`.
It was a live, CPU-consuming Python workload (86.7% CPU, 1.2 GB RSS, elapsed 4:02).
`uptime` reported load averages `26.97, 31.34, 41.54` on 16 CPUs. No kill, restart,
substrate edit, or other disruptive action was justified.

## Disposition

The historical JUNK-LOAD alert is safely attributable to a Python workload; the current
classifier identifies the same class of work as known `ORGAN-LOAD`. This is an observe-only
transient/reclassified warning, not an actionable runaway process. Leave the workload intact.

Retry edge: open a new exact health triage only if a fresh load-audit alert again classifies
the process as `JUNK-LOAD`/unknown, or if the current workload loses its known-workload
attribution and remains sustained across the configured recheck interval.

## Delegation and verification

Delegated `health-junk-load-audit` for independent read-only analysis. The worker could not
authenticate (`Login expired · Please run /login`), produced no evidence, and its report was
not used. I personally inspected the source line, task plan, live `mesh-load-audit --json`,
`uptime`, and `ps` output above. No repository or substrate changes besides this receipt and
its required findings manifest were made.

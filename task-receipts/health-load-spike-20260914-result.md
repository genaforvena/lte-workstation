# Minute-53 CPU-load follow-up — 2026-09-14

Task: `health-load-spike-20260914/observe-0353`  
Raw capture: `task-receipts/health-load-spike-20260914-observation.md`

The read-only capture ran from 03:52:30Z through 04:01:00Z around the wired 03:53 minute slot.
It confirms `mesh-random-track-grind` started by 03:53:30Z and remained active through the final
sample. At 03:54:00Z its process tree included `mesh-soundscape --measure`; the measurement worker
reached 229% CPU, then 545% at 03:55:00Z and 628% at 03:55:30Z. Other audio-buffer measurement
workers also appeared. The grinder shell itself used 0% CPU while waiting on that work.

The system was already heavily loaded before the grinder appeared: at 03:52:30Z load averages were
57.95/50.78/41.45, with the grinder absent and `llama-server` at 134% CPU plus task queue/audit
processes near 100%. After the grinder's measurement worker appeared, 1-minute load fell to 18.69
at 03:54Z, then varied from 11 to 30 through 04:01Z while the worker ran. This shows the scheduled
grind lane is a substantial CPU consumer, but it does not explain the much larger historical
00:53Z/01:53Z peaks by itself. The 03:53:01Z USB record is `n/a — no USB-attached net interface to
resolve`.

Disposition: the next-slot capture confirms scheduled CPU-heavy audio analysis overlaps the
minute-53 cadence; historical peak attribution remains unknown because the 00:53/01:53 process
tables were not retained and the grinder output has no per-run timestamps. No scheduler, process,
or substrate change is justified by this observation. To verify historic causality would require
another captured peak with competing load sources accounted for; this task makes no sole-cause
claim.

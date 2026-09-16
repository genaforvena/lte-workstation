# tmp-guard leak triage — 2026-09-16

Task: `witness-chat-range-review-near-61371-61435-correctives/triage-tmp-guard-20260916`, owner `health`.

## Disposition

**Bounded / known leak, no safe deletion or substrate action taken.** The current
non-destructive sample is still LEAKING. The age sweep is not ineffective in the
sense of failing to run: it finds no eligible mesh-owned targets (`swept=0`),
while the population is dominated by fresh `.mesh-land-pool.*` files that are
not safe for this triage to remove. The remaining producer attribution is a
follow-up, not a proven single-process cause.

## Fresh evidence

- At 2026-09-16T07:20Z, `mesh-tmp-guard --dry-run` returned exit 0:
  `LEAKING`, `would-remove=0`, `entries=4283`, `other-owner=23`, `/tmp` use
  `31%`, flux `21061.8MB/h` on `dm-0`, cron `10849.7MB/h`, window `2365s`,
  `swept_share=0.000%`; residue was `.me*23:2048(.mesh-land-pool.1561815)`.
- The command was explicitly dry-run; it made no deletion and did not update
  the guard state or logs.
- A read-only population census found 2644 `.mesh-land-pool.*` entries, 305
  `tmp.*` entries, and 1324 other entries at the sample. Recent pool files were
  still being created through 07:20Z, so the count is live and moving.
- `mesh-tmp-guard --unwind-scan` named 22 Python and 22 shell producers with
  unwind gaps, plus 156 shell counted-only producers; this identifies cleanup
  coverage debt but does not prove which producer owns the pool files.
- Historical guard rows show the same mechanism: 2960 entries / 0 swept at
  2026-09-14T00:41Z and 2423 / 0 swept at 2026-09-14T18:41Z. The flux log shows
  sustained device write rates and `swept_share=0.000%` in recent windows.

## Retry edge

On the next tmp-guard cadence, rerun `mesh-tmp-guard --dry-run` and compare the
pool-family count and flux window. If the pool remains the dominant residue,
route a producer-specific, non-destructive ownership trace to the responsible
owner before any cleanup decision. Do not use broad `rm`, `mesh-tmp-guard`
write mode, or alter routing/services from this evidence.

Delegation: a read-only chat-range evidence review was launched through the
shared Codex relay (`health-witness-review`); at final inspection it had no
returned artifact and remained `working`, so this receipt relies on the direct
commands and files listed above, which were personally inspected.

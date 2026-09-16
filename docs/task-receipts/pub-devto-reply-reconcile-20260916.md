# pub dev.to reply reconciliation — 2026-09-16

## Fresh evidence

- `mesh-devto-comments --list` completed at 2026-09-16T10:23Z and showed `3ecl5` in the
  article thread, alongside four promotional comments.
- `timeout 180s mesh-devto-reply --owed` completed at 2026-09-16T10:56Z with exit 0.
  Its complete actuator worklist contained only `3ef25`, `3ekc9`, `3ekdf`, and `3eoo9`;
  `3ecl5` was absent.
- Direct authenticated read of `https://dev.to/api/comments?a_id=4218940` at the same
  reconciliation confirmed `3ecl5` is still a leaf comment under `3eb9o`, with no child
  reply. This proves comment presence, not actuator owed status.

## Disposition

The previous contradiction is resolved for the actuator: `3ecl5` is not currently eligible
for `mesh-devto-reply --post`, so no outward reply was attempted. The durable historical
receipt and task remain evidence of the earlier disagreement; they do not authorize posting
after the fresh `--owed` result excludes the id. The four actuator-listed rows remain spam
and are intentionally unanswered.

# Health triage: Genome held `/clear` input

Task: `health-warning/af9914e9fe355753f46c/triage`

## Finding

At 06:11:00Z on 2026-09-14, `mesh-channel-keepalive` reported Genome's unchanged
composer input `› /clear` as `UNATTRIBUTABLE` after 734 seconds and explicitly
left it untouched. A fresh read at 06:15Z still returned `HOLDS › /clear`; the
Genome mind-state remained `UNKNOWN` and reported `/clear` as the input. The
input is six characters after marker normalization, below
`MESH_STRAND_MIN_CHARS` (default 16), so `strand_attribution` returns
`UNATTRIBUTABLE` before inspecting the WAL. This is the deliberate short-input
blind spot: `/clear` alone cannot distinguish a human's typed command from a
stranded delivery. The WAL is configured `full` and contains recent intent
payloads; therefore this event does not establish that the WAL is unavailable.

The recovery search found the separate open Genome task
`chat-review/witness-pane-charter-contract-20260914/make-checker-enforce-charter`
and its dispatch check passed. It concerns the witness pane checker, not the
held `/clear` input, so it is not a prerequisite for this triage and was left
with Genome. No new prerequisite task was needed for the read-only disposition.

## Evidence

- `/home/mesh-home/.mesh/composer-sweep.log`: 05:58:46Z armed; 06:02:50Z and
  06:07:00Z waiting; 06:11:00Z `STRAND-UNATTRIBUTABLE`, `acted=0`; 06:15:01Z
  still in cooldown with zero re-drives.
- `/home/mesh-home/.mesh/chat.log`: 06:11:00Z `[mind-holding]` report.
- `mesh-tell --composer genome` at 06:15Z: `HOLDS › /clear`.
- `mesh-mind-state genome` at 06:15Z: `UNKNOWN /clear`.
- `/home/mesh-home/.mesh/tell-wal.log.level`: `full`; recent rows have full
  payloads. The classifier's short-input guard at
  `scripts/mesh-channel-keepalive` returns before WAL matching.
- `scripts/mesh-channel-keepalive`: `strand_attribution` normalizes the marker
  then returns `UNATTRIBUTABLE` for input shorter than 16 characters.
- `mesh-task check dispatch chat-review/witness-pane-charter-contract-20260914/make-checker-enforce-charter genome`: passed (exit 0).

## Disposition

Known attribution blind spot for short generic composer inputs. Keep the input
untouched while attribution remains unavailable; do not submit or clear it on
this evidence. No routing, DNS, firewall, VPN, Tailscale, or other substrate
state changed. No delivery code was changed.

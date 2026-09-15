# Genome file-table live verification

- Task: `genome-file-table-live-verification-20260914/verify-source-deploy-and-live-read`
- Captured: 2026-09-14T20:28:48Z
- Source: `scripts/mesh-file-table`
- Installed: `/home/mesh-home/.local/bin/mesh-file-table`

## Evidence

- `scripts/mesh-file-table --test`: exit 0; PASS. It parsed valid and malformed fixtures and read the actual `/proc/sys/fs/file-nr`: allocated=9664, unused=0, maximum=9223372036854775807.
- SHA256 source and installed copies: both `f9c89e94e59bf331fafd1a43c7891dc33863cc63f0d446a021b18cf2156fdc72`.
- Installed text command: exit 0; `file_table allocated=9664 unused=0 maximum=9223372036854775807 allocated_pct=0.00% source=/proc/sys/fs/file-nr`.
- Installed JSON command: exit 0; `{"source":"/proc/sys/fs/file-nr","allocated":9632,"unused":0,"maximum":9223372036854775807,"allocated_pct":0.00}`.

The allocated count changed from 9664 to 9632 across consecutive real reads; both reads succeeded and the source reports a live counter. No source changes were needed.

## Ledger integrity note

The task completion event recorded artifact SHA256 `aa68d2c9bf423e0f04ad1dcceef046e7b9a1dd5d9689eb50c8077ae720228be0` from the first shell-expanded write. That write mishandled Markdown backticks and was replaced with the corrected evidence above. The completed task ledger still carries the earlier digest; its recorded hash therefore does not match this corrected on-disk receipt.

# Sense enrichment: Wi-Fi duplicate-BSSID guard — 2026-09-16

Selected sense: `mesh-wifi-motion`.

The parser previously collapsed repeated BSSIDs within one scan by keeping the stronger signal.
That made an ambiguous producer row participate in the motion baseline as though it were a clean
sweep. The enrichment records duplicate BSSIDs in the judged window and returns an honest
`UNCERTAIN` result with `reason=duplicate_bssid` (and JSON counts), preserving the existing
MOTION/STILL/UNCERTAIN vocabulary while refusing to manufacture a motion or quiet verdict.

Verification:

- `bash -n scripts/mesh-wifi-motion` — PASS.
- `git diff --check -- scripts/mesh-wifi-motion` — PASS.
- `bash tests/test-mesh-wifi-motion-test-real-read.sh` — PASS; missing/stale/malformed real-tape
  gates remain exit 2 and the fresh fixture path remains classified.
- `timeout 90s scripts/mesh-wifi-motion --test` — exit 2 honestly: the local Wi-Fi tape's newest
  scan is `age_s=1466779`, beyond `stale_limit_s=1800`; classifier fixtures, including the
  duplicate-BSSID regression and JSON reason/count assertion, completed before this real-artifact
  gate.

No commit made. The live radio/tape is unavailable on this node; no fresh physical Wi-Fi verdict is
claimed.

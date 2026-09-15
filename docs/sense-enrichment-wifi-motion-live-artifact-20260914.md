# Wi-Fi motion live-artifact gate — 2026-09-14

The resumed `mesh-wifi-motion` work adds a real-input gate to `--test`. Classifier fixtures alone
no longer certify the sense: the test now needs a fresh, parseable `~/.mesh/wifi.log` artifact and
must run the ordinary JSON classifier against it with state isolated and feeder refresh disabled.
Missing, stale, excessively future-dated, or unassessable evidence exits 2. A tape within the
configured clock-skew allowance remains classifiable and publishes `freshness=UNKNOWN`; a regression
guards that distinction. The test also covers missing, fresh-classifiable, stale, and malformed
tapes.

## Verification

- `bash tests/test-mesh-wifi-motion-test-real-read.sh` — PASS. The fresh tape here is a fixture and
  verifies the test gate; it is not claimed as a physical radio read. The test also covers tolerated
  future clock skew and checks the negative `age_s` stays paired with `freshness=UNKNOWN`.
- TDD red/green: the new tolerated-skew assertion first failed with exit 1 (`age_s=-58`,
  `freshness=UNKNOWN`); after the gate accepted that runtime-supported pair, the focused suite passed.
- `bash -n scripts/mesh-wifi-motion` and `git diff --check -- scripts/mesh-wifi-motion` — PASS.
- `scripts/mesh-wifiscan --test` — exit 2: `no wifi radio / scan backend on mesh-home`.
- The real `~/.mesh/wifi.log` is 913,255 bytes but its newest scan is from 2026-08-30; during final
  verification it was 1,316,878 seconds old, beyond the 1,800-second limit. No feeder or test wrote
  to this liveness tape.
- `scripts/mesh-wifi-motion --test` — exit 2 after classifier fixtures, explicitly reporting the
  stale real artifact (`age_s=1316878`). `MESH_WIFI_MOTION_REFRESH=0 scripts/mesh-wifi-motion --json`
  also exited 2 with `reason=tape_stale` (`age_s=1316876`); it did not turn the old scans into STILL.

The live radio is unavailable on this node, so no fresh Wi-Fi motion verdict is claimed. The
sensor's tested outcome is honest degradation (exit 2), not a fabricated all-clear. No commit was
made.

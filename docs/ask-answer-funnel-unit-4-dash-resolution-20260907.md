# Ask-answer funnel Unit 4 — dash resolution

## Contract

The fused `mesh-dash chat`/`witness` pane must expose Unit 3's
`ask_open`, `ask_stale_h`, and `ask_resolve` measurements together with the
age/denominator gates (`ask_den`, `ask_p90_h`, `ask_unknown`). The dash is a
read-only consumer of the latest witness ledger row: it does not reparse the
board or promise sources. Missing, malformed, `UNKNOWN`, or `None` fields
render as `UNKNOWN`, never as zero or a green verdict.

## Red before green

The focused test was first run before the renderer existed:

```text
tests/test-mesh-dash-ask-resolution.sh
rc=1
FAIL: dash lacks ask resolution section
```

## Implementation

- Added `render_ask_resolution` to `scripts/mesh-dash`.
- Added `tests/test-mesh-dash-ask-resolution.sh` with valid and gated/UNKNOWN
  ledger fixtures.
- The renderer is called in the fused `witness|chat` path immediately after
  the embedded witness tape.

## Verification

- Focused test: rc `0`, output SHA256
  `6a2b635f43f78eb70fd02506e984ded7a9a0bb034a7a45980d6501cacc3c3687`.
- `bash -n scripts/mesh-dash`: rc `0`.
- `bash scripts/mesh-dash --test-fast`: rc `0`, output SHA256
  `a4a52c9b5009fffdc6c5a64d01313cb7ce4f696c4a6f0525243c1549a8e8926c`.
- Source `scripts/mesh-dash` SHA256
  `ad3d80c715b1456b96d3f1f6926659ff116280e02ca47faa62b27b4076cd2ab2`.
- Deployed `/home/mesh-home/.local/bin/mesh-dash` SHA256 is identical:
  `ad3d80c715b1456b96d3f1f6926659ff116280e02ca47faa62b27b4076cd2ab2`.
- Live deployed frame `/tmp/unit4-live-chat.out`: rc `0`, output SHA256
  `42547417399332131ac3307a0199339ef61b250048156e0ebc54f17729bb7189`.
  It rendered:

```text
-- ask resolution (age/denominator-gated; UNKNOWN-safe) --
  open=2 oldest_stale_h=10.4 resolved=0.922 denominator=218 p90_h=10.3 unknown=0 source=2026-09-07T18:12:05Z
```

The sound-collage task remains visibly BLOCKED and was not altered by this
Unit 4 change.

## Recheck

The artifact was rechecked after a transient visibility report and is present.
The focused test remains green: rc `0`, output SHA256
`6a2b635f43f78eb70fd02506e984ded7a9a0bb034a7a45980d6501cacc3c3687`.
Source and deployed hashes remain identical. A fresh deployed full
`mesh-dash --test` was attempted with 180-second and 300-second bounds but did
not reach a terminal result (both rc `124`; output SHA256s
`1a8027f40b22cecae502d33544eaa399576fe517e949aebcae05e9ad005491c3` and
`b4a6c06672677cf0e25ec72bec83beae33305cee4b8087f168962014373b02bb`). The
traced run shows the outer test fence waiting on its nested full suite, ending
with `Terminated`; this is retained as an honest unresolved full-suite gate,
not a done claim. The previously completed deployed live frame remains the
live wiring evidence recorded above.

## Independent disposition

Witness independently accepted the implementation artifact, focused test,
source/deployed parity, and live `--once chat` frame. The remaining full
deployed `/home/mesh-home/.local/bin/mesh-dash --test` gate was independently
rechecked at a 120-second bound and returned rc `124` with no completion
output. This is an explicit `BLOCKED` disposition for the full-suite gate;
the Unit 4 implementation is not represented as fully verified until a
completed deployed `--test` receipt exists.

## Full-suite fence repair and terminal result

The full-suite stall was isolated to repeated temporary `check` renders:
empty fixture caches caused each render to wait on live fleet and health-organ
probes. The renderer now keeps production probe bounds unchanged while the
smoke suite uses bounded fixture values (`MESH_FLEET_HEALTH_TIMEOUT=2`,
`MESH_CHECK_PROBE_TIMEOUT=1`, retry sleep `0`). Source and deployed
`mesh-dash` are byte-identical at SHA256
`7eb808708671a5275089d773cf98bbc20deefc014dad8267c1def14067039a54`.

The completed deployed full run returned rc `2`, output SHA256
`d39e04453a036410e56c78c196d7a61100ccd4a6f16797f8222d1b224c6c0194`. Its
only remaining result is an honest node-condition `n/a`: the pinned 27-row
cap cannot fit this node's 28-row untrimmable fixed floor. This is a terminal
result, not a timeout or a full green claim; Unit 4 remains conditionally
blocked on the node-specific cap disposition.

Fresh deployed wiring frame after the fence repair: `/tmp/u4-live-fixed.out`,
rc `0`, output SHA256
`d3ec7621a42797ee85b1d787426643884c4233c62fee2638735697d41f436f08`;
rendered `open=1 oldest_stale_h=11.0 resolved=0.918 denominator=219
p90_h=10.9 unknown=0`.

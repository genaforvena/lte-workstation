# Integration-family migration progress — 2026-09-12

Task: `tg-scripts-layout-migration-20260912/integration-family-slices` (owner: genome).

This is the first isolated family slice, not completion of the task. The phone body-motion sensor
implementation now lives at `scripts/integrations/mesh-body-motion`; the original executable path is
retained as a compatibility shim. The manifest classifies the nested implementation as
`integrations/tool/none`, and the shim as the sole installable `mesh-body-motion` entry. The
manifest domain classifier now recognizes the `scripts/integrations/` destination directly.

Runtime contract: `mesh-body-motion` is a read-only phone sensor adapter. It obtains a fused sensor
sample over SSH/Termux and publishes the same state artifact and confidence/freshness vocabulary.
Its test explicitly preserves the honest unavailable result (exit 2) when the phone or
`termux-sensor` cannot be reached. The separate `mesh-body-context` tool is downstream fusion, not
a device/protocol adapter, so it remains in the top-level operations inventory.

The caller census found references across the phone/body fusion and presentation tools; those
callers continue resolving the old basename. No caller or scheduled command was rewritten. The
existing header cadence and the single live entry at
`~/.mesh/reflexes.cron:219` (`7-59/10 * * * *`) remain unchanged; no second cadence was added.

## Bluetooth controller family slice

The local BlueZ connected-peripherals sense now lives at
`scripts/integrations/mesh-bt-link`, with its old executable path retained as a compatibility shim.
The manifest recognizes `mesh-bt-*` as integrations by basename and inventories the nested
implementation as non-deploying under the shim's compatibility owner. Runtime classification is
based on its actual contract: it reads this node's powered local Bluetooth controller and its
connected peripherals; it does not scan nearby BLE advertisers or inspect a roaming phone.

Caller and cadence census: source references remain at `mesh-audio-path`, `mesh-chaos`, and
`mesh-bt-census`; no caller path changed. The single live schedule remains
`~/.mesh/reflexes.cron:139` (`*/9 * * * *`, `--edge`), with cadence, args, and doctor-artifact
declarations preserved on the shim. No duplicate schedule was introduced.

```text
scripts/mesh-bt-link
  exit 2: OFFLINE|no bluetooth controller / bluetoothd down
~/.mesh/.bt-link-state
  mtime 2026-09-12 17:18:37 UTC; contents OFFLINE|no bluetooth controller / bluetoothd down
  fresh unavailable-state artifact; current controller coverage is unavailable, not zero devices
scripts/mesh-bt-link --test
  exit 2: BT sensor unreachable; classifier/offline gate verified, live enumeration skipped
bash tests/test-mesh-bt-link-integration-slice.sh
  PASS: destination/domain/ownership and the shim's actual --test outcome (0 with a live-read
  artifact or 2 with an explicit unavailable result)
bash -n scripts/mesh-bt-link scripts/integrations/mesh-bt-link \
  tests/test-mesh-bt-link-integration-slice.sh
  PASS
```

Post-land parity check: `cmp scripts/mesh-bt-link ~/.local/bin/mesh-bt-link` passed;
`scripts/mesh-manifest --check` passed with 1203 complete rows and no duplicate installed
basenames. The parity rows report `scripts/mesh-bt-link` as `same` and the nested implementation as
non-deployed. The deployed `~/.local/bin/mesh-bt-link --test` returned the same honest exit 2 because
the controller remains absent. `HEAD == origin/main` after landing.

The body-motion slice landed as `a228cb01`, `c1f3d7e3`, `047230ef`, `4f9a98ab`, and `af5c0495`;
the Bluetooth slice landed as `3b871827`, `f9d1dee2`, `50363d99`, `ecef458e`, and `52dfbed8`.
Each change went through path-limited `mesh-land` commits; the commit-subject scan found no
task-specific suggested subject in `~/.mesh/chat.log`.

## Local camera family slice

The `mesh-camera` adapter now lives at `scripts/integrations/mesh-camera`; its original executable
basename remains as the compatibility shim. Runtime classification follows its local contract:
it captures one still from this node's `/dev/video0`, trying the bundled/system ffmpeg path and then
fswebcam. It is separate from `mesh-imac-cam`, whose implementation captures from a remote iMac.

The caller census found references at `mesh-doctor`, `mesh-object-id`, `mesh-card`,
`mesh-capture-inuse`, `mesh-chaos-doctor`, `mesh-imac-cam`, `mesh-see`, `mesh-hear`, and
`mesh-organ`; all continue using the old basename. No cadence, service, or cron entry was found, so
this on-demand capture adds no recurring camera load.

```text
scripts/mesh-camera --test
  PASS: real one-frame capture created a non-empty JPEG and its 0xffd8 signature was checked
bash tests/test-mesh-camera-integration-slice.sh
  PASS: manifest ownership and compatibility path plus a real capture (or an explicit BUSY result)
bash -n scripts/mesh-camera scripts/integrations/mesh-camera \
  tests/test-mesh-camera-integration-slice.sh
  PASS
scripts/mesh-manifest --check
  PASS: 1204 complete rows; no duplicate installed basenames
```

Post-land camera parity: `cmp scripts/mesh-camera ~/.local/bin/mesh-camera` passed; the manifest
reports the shim as deployed `same` and the nested source as non-deployed. The deployed
`~/.local/bin/mesh-camera --test` returned 0 with `camera present but BUSY`, which is the tool's
explicit pass state when another process holds the real device. The pre-move test had produced and
validated a real JPEG frame. Camera commits: `6410ecde`, `3f543e88`, `6ecf044f`, and `c2f2b737`.

## Open-Meteo external-service family slice

The `mesh-weather` client now lives at `scripts/integrations/mesh-weather`, with the existing
top-level command retained as the installable shim and its `23 * * * *` cadence declaration kept
there. Runtime classification is an external forecast API adapter: it fetches hourly Open-Meteo
temperatures using only city-level coordinates from gitignored `~/.mesh/weather.env`. The config
file and coordinates remain outside the repository. The downstream `mesh-therm-watch` and
`mesh-climate` consumers keep their old command path.

The live cadence census found exactly one existing entry at `~/.mesh/reflexes.cron:128`; no second
cron or service schedule was found. The task test passed its parser, thermal flag/edge, blind, and
unseeded fixtures, then parsed a live response for the already-seeded coordinates:

```text
bash tests/test-mesh-weather-integration-slice.sh
  PASS: destination/domain/owner, shim dispatch, fixture behavior, and live fetch parse
env -u MESH_WEATHER_SRC MESH_STATE_DIR=/tmp/mesh-weather-slice.O4LxXe \
  MESH_WEATHER_ENV=/home/mesh-home/.mesh/weather.env \
  MESH_WEATHER_TAPE=/tmp/mesh-weather-slice.O4LxXe/weather.log MESH_WEATHER_CHAT=0 \
  scripts/mesh-weather
  PASS: real fetch artifact at /tmp/mesh-weather-slice.O4LxXe/.weather-state, mtime
  2026-09-12 17:31:58 UTC, `now_c=16.4 today_max_c=17.1 peak_hour=15 thermal_day=0`
  Chat output was disabled and all state/tape writes were confined to the temporary directory.
bash -n scripts/mesh-weather scripts/integrations/mesh-weather \
  tests/test-mesh-weather-integration-slice.sh
  PASS
scripts/mesh-manifest --check
  PASS: 1205 complete rows; no duplicate installed basenames
```

Post-land Open-Meteo parity: `cmp scripts/mesh-weather ~/.local/bin/mesh-weather` passed;
manifest parity reports the shim `same` and the nested implementation non-deployed. The deployed
`~/.local/bin/mesh-weather --test` again parsed a live response. Weather commits: `4ae1a689`,
`b5a25357`, `aad04267`, `c2096108`, and `ce49b2de`.

## Phone Wi-Fi protocol family slice

The `mesh-wifi-link` implementation now lives at `scripts/integrations/mesh-wifi-link`; its shim
retains the old command path and the observer-probe, cadence, args, state, and blind-marker headers.
Its runtime contract is a Termux Wi-Fi connection-info read over SSH to the phone, not a local `iw`
read. The source comment on the shim states this actual protocol. Existing callers remain on the
legacy basename; the census found references across doctor, link/traffic senses, Wi-Fi fusion,
phone AP, operator-state, and simulation tools.

The single live reflex remains `~/.mesh/reflexes.cron:227` (`2-59/5 * * * *`, `--edge`); no second
cadence was added. The focused migration test runs the tool's real-read gate and accepts exit 0 only
with numeric link fields, or exit 2 only with an explicit `n/a`. This node's actual result is
unavailable: the phone did not provide `termux-wifi-connectioninfo`, so there is no current Wi-Fi
reading. The honest offline artifact is `~/.mesh/.wifi-link-offline`, freshly touched at
2026-09-12 17:40:23 UTC; `.wifi-link.state` remains the older `GOOD` sample from 2026-09-03, and
must not be presented as current coverage.

```text
scripts/mesh-wifi-link --test
  exit 2: smoke-test n/a; phone/Termux Wi-Fi source unavailable
bash tests/test-mesh-wifi-link-integration-slice.sh
  PASS: manifest ownership/cadence declaration and honest real-read result through the shim
bash -n scripts/mesh-wifi-link scripts/integrations/mesh-wifi-link \
  tests/test-mesh-wifi-link-integration-slice.sh
  PASS
scripts/mesh-manifest --check
  PASS: 1206 complete rows; no duplicate installed basenames
```

Post-land Wi-Fi verification: `cmp scripts/mesh-wifi-link ~/.local/bin/mesh-wifi-link` passed;
manifest parity marks the top-level shim `same` and the nested implementation non-deployed. The
deployed `--test` and one deployed normal read both returned exit 2; the latter refreshed the honest
OFFLINE marker at 17:40:23 UTC. The older `GOOD` sample was left untouched. Wi-Fi commits:
`2ea204e4`, `762c6047`, `ca5fee73`, `f79e3a69`, and `4aea2ba2`.

The local `mesh-wifi-quality` tool is not folded into this family: its current `--test` says
`FAIL (no wireless iface)`, so its local-adapter result needs separate diagnosis. `mesh-phone-sensors`
also remains in place because its current `--test` checks command presence/reachability rather than
asserting a real sensor read; it needs a real-read gate before it can meet this task's verification
contract.

## Note 3 ADB battery family slice

The `mesh-note3-battery` implementation now lives at `scripts/integrations/mesh-note3-battery`,
with its installable compatibility shim retaining the original basename, `5-59/10 * * * *`
cadence, and `--edge` args. Runtime classification is a local ADB protocol adapter for the
authorized Samsung Galaxy Note 3; it reads `dumpsys battery`. It remains distinct from the Redmi
phone's Termux-over-SSH body sensors and this node's sysfs battery senses.

The only runtime schedule found is the existing `~/.mesh/reflexes.cron:330` entry with that same
cadence and `--edge`; no source command caller, second cron, or service was found. The focused test
passed fixtures and a real ADB battery read. A separate one-shot JSON read produced a current
sample at 2026-09-12T17:44:52Z: level `100/100`, temperature `26.7°C`, power source `USB`. The
device serial is omitted from this receipt. That one-shot did not write the change-detection state
or board.

```text
bash tests/test-mesh-note3-battery-integration-slice.sh
  PASS: manifest ownership, cadence header, fixtures, and real ADB read through the shim
rtk scripts/mesh-note3-battery --json | parse fields
  PASS: current read timestamped 2026-09-12T17:44:52Z
bash -n scripts/mesh-note3-battery scripts/integrations/mesh-note3-battery \
  tests/test-mesh-note3-battery-integration-slice.sh
  PASS
scripts/mesh-manifest --check
  PASS: 1207 complete rows; no duplicate installed basenames
```

Post-land Note 3 parity: `cmp scripts/mesh-note3-battery ~/.local/bin/mesh-note3-battery` passed;
manifest parity reports the shim `same` and nested source non-deployed. The deployed test again
passed with a live ADB battery read, and the single `--edge` cron line remained unchanged. Note 3
commits: `62fa542f`, `86983f53`, `201e94e0`, and `18c406e8`.

## Remote iMac camera protocol slice

The one-shot `mesh-imac-cam` SSH/SCP adapter now lives at
`scripts/integrations/mesh-imac-cam`; its Objective-C capture helper moved with it to
`scripts/integrations/mesh-imac-cam.m`, and the original executable basename remains the installable
compatibility shim. The adapter checks remote camera consent, deploys/compiles the paired helper when
needed, and returns a settled JPEG. Its existing `--test` compiles and runs the portable settle-core
cases before attempting an actual consented camera read.

Runtime classification for the ambiguous watchers: `mesh-phone-watch` is a ten-minute ADB/Termux
sshd repair and anchoring reflex (one existing cron at `~/.mesh/reflexes.cron:78`), not a phone
measurement adapter. `mesh-cam-watch` and `mesh-imac-cam-watch` are continuous motion/classification
loops owned by systemd services, not capture adapters. The one-shot `mesh-imac-cam` is the remote
camera protocol adapter called by `mesh-imac-cam-watch`; it declares `orphan-ok` and has no cadence
or duplicate service. The camera watcher's installed unit is currently inactive; its
`.imac-cam-watch.state` and baseline are from 2026-07-24 and do not establish current camera coverage.

```text
tests/test-mesh-imac-cam-integration-slice.sh
  PASS: nested tool/helper manifest ownership, on-demand cadence, shim dispatch, settle-core, and
  real-read/unavailable result
scripts/mesh-imac-cam --test
  exit 2: portable settle-core passed all 8 cases; iMac unreachable at 192.168.8.214, so no live
  frame was produced or claimed
scripts/mesh-manifest --check
  PASS: 1208 complete rows; no duplicate installed basenames
```

The caller census keeps `mesh-imac-cam-watch` on the old public basename. The existing iMac watcher
service remains unchanged. The source path `.m` is a runtime companion to the nested implementation;
mesh-land's asset-pair rules kept the source pair together. Post-land parity reports the public shim
`same` at `~/.local/bin/mesh-imac-cam`, with both nested implementation/helper correctly
non-deployed. The deployed compatibility command reran the same settle-core and honest unreachable
gate. Commits: `9a49272a`, `53ac3aeb`, `d319129f`, `fb436379`, `a653595a`, and `9b423af0`.

`scripts/mesh-land --test` passed after a one-line fixture correction made its synthetic untracked
lane tool executable before asking the real manifest enumerator to classify it. The scoped quiet
`mesh-land --check` returned 1 because the selected migration files were settled candidates, as its
documented contract specifies. The landing printed a stale old-path `pathspec` warning while
processing the helper rename; the final tree has no old helper path, the new pair is in the manifest,
and `HEAD == origin/main` after the landing.

Remaining phone-tool disposition: `mesh-wifi-quality --test` reports no local wireless interface,
and `mesh-phone-sensors --test` does not assert a real sensor read, so neither has been moved. The
already-landed Wi-Fi-link slice is the verified Termux Wi-Fi protocol adapter. Those exclusions keep
unavailable or unverified inputs from appearing as healthy coverage.

Verification:

```text
bash tests/test-mesh-integration-family-slice.sh
  PASS: manifest classification; source shim and regular deployed-copy fallback resolve to the
  nested implementation and return a fresh fixture state without phone access
bash tests/test-mesh-manifest.sh
  PASS: inventory fixture matrix and duplicate installed-basename guard
scripts/mesh-manifest --check
  PASS: 1202 complete rows; no duplicate installed basenames
bash tests/test-mesh-manifest-consumers.sh
  PASS: both consumer --test paths outside the repository
scripts/mesh-sync-tools --test
scripts/mesh-doctor --test
scripts/mesh-autowire --test
scripts/mesh-land --test
scripts/mesh-vitality --test
  PASS (mesh-doctor emitted existing Python SyntaxWarnings; no test failure)
bash tests/test-mesh-body-motion-test-real-read.sh
bash tests/test-mesh-body-motion-status-freshness
  PASS: two-sample read gate and state freshness behavior
bash -n scripts/mesh-body-motion scripts/integrations/mesh-body-motion \
  tests/test-mesh-integration-family-slice.sh
  PASS
scripts/mesh-body-motion --test
  classifier and simulation-isolation checks PASS; real sensor arm returned exit 2 after SSH
  timeout to 100.103.99.16:8022; the sensor is unavailable, not reported as healthy
~/.mesh/.body-motion-state
  current contents `|OFFLINE||||`, mtime 2026-09-12 17:00:23 UTC; fresh OFFLINE marker, no current
  hardware coverage claim
runtime cadence census
  exactly one matching reflexes.cron entry; no matching systemd or /etc/cron entry
```

The first concurrent source/deployed `--test` run raced over the shared `*-simulate` fixtures and
produced one false isolation failure. A serialized rerun passed. The same test command must not be
run concurrently for this tool.

Rollback: move `scripts/integrations/mesh-body-motion` back to `scripts/mesh-body-motion`, remove
the compatibility shim and empty integration directory, revert the one path-classification branch
in `scripts/mesh-manifest`, and remove the focused test. Then run
`scripts/mesh-manifest --check` and the restored tool's `--test` from outside the repository.

## Note 3 ADB sensor family slice

The motion, proximity, orientation, and ambient implementations moved from the top level into
`scripts/integrations/`. Their bytes match the four original top-level sources at starting HEAD
`7487565d`, so the move preserves their implementation. Each former top-level basename is now an
executable compatibility shim to the nested source, with its original cadence and arguments. These
four tools share the Note 3 ADB device/protocol family, but remain separate sensors and keep their
distinct schedules. The battery adapter remains the separately completed Note 3 battery slice above.

The caller census found downstream references through the original basenames, including
`mesh-note3-desk`, `mesh-note3-thermal`, `mesh-note3-magevent`, `mesh-stress`, and
`mesh-ambient-level`. No caller or scheduled command was rewritten. The live
`~/.mesh/reflexes.cron` has exactly one entry for each adapter: motion `4-59/5` with `--edge`, prox
`3-59/5` with `--edge`, orient `0-59/5` with `--edge`, and ambient `7-59/10` without `--edge`.
No matching systemd timer/service was found; the migration adds no cadence.

The real-read gates passed serially on the Note 3:

```text
mesh-note3-motion --test
  PASS: LIVE adb read -120,335,16991; unrailed and carrying gravity
mesh-note3-prox --test
  PASS: LIVE adb read raw=8
mesh-note3-orient --test
  PASS: LIVE adb read 191.647,13.3566,-85.5458,24679866715269 -> TILTED
mesh-note3-ambient --test
  PASS: LIVE Note3 env 992.4hPa, 22.0958C, 53.1126% RH, dewpoint 12.1C
tests/test-mesh-note3-sensor-family-integration-slice.sh
  PASS: manifest ownership, compatibility paths, preserved cadence headers, serial real-read gates
  Also passes when invoked from /tmp.
scripts/mesh-manifest --check
  PASS: 1212 complete rows; no duplicate installed basenames
```

At 18:13 UTC, the production state artifacts were fresh: motion 18:09, prox 18:13, orient 18:12,
and ambient 18:07. The ambient artifact is under its declared 2400-second freshness bound; each
scheduled edge sensor remains under its 10-minute doctor horizon. The focused integration test
first failed against the prior layout, then passed through the compatibility paths after the shim
change. Shell syntax checks passed for all four shims, implementations, and the test driver.

Rollback is an inverse path move of the four implementations back to their old top-level paths,
restoring their prior file contents there, then removing the four shims and focused slice test. The
existing cron lines need no edit because they still resolve the old paths. Re-run the real-read gates
and `scripts/mesh-manifest --check` after rollback.

Post-land verification on 2026-09-12: `tests/test-mesh-note3-sensor-family-integration-slice.sh`
passed after all four wrappers were landed. Its serial installed `--test` gates passed with live
motion `312,175,17183`, proximity raw `9`, orientation `162.526,-41.5158,-62.1756 -> TILTED`, and
ambient `992.284hPa, 23.327C, 54.0237%`. `mesh-manifest --check` passed with 1212 rows and no
duplicate installed basenames; `mesh-sync-tools --test` passed inventory, nested ownership, shim
basename, and cleanup checks. SHA-256 hashes of each repository shim and installed shim match.
Wrapper commits: `f324b698` (motion), `904e713c` (ambient), `9005f21c` (orientation), and
`18ccf5a1` (proximity). Nested source commits: `cb098f48`, `31983160`, `f9949a5f`, and `dc3b526e`
respectively. The focused regression landed as `f4472fbc`; only this receipt remains to be landed
before closing the slice.

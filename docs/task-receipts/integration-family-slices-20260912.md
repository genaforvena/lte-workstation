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

Next: finish the remaining isolated phone, network, camera, and external adapter families; classify
ambiguous watch/platform tools by actual runtime contract; verify each sensor's real artifact and
freshness/coverage, caller resolution, manifest inventory, deployed parity, and cadence before
closing the task. No whole-task completion is claimed here.

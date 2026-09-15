# TG scripts audit — semantic duplicate/dead-code coverage

Task: `tg-intake-coverage-followup-20260912/scripts-semantic-coverage`  
Owner: `genome`  
Audited: 2026-09-12  
Input map: [scripts layout inventory](tg-scripts-layout-audit-map-20260907.md)  
Input gap review: [TG intake coverage review](design-spec-audit-tg-intake-20260912.md)

## Result

The map's candidates do not establish semantic duplication or dead code. The caller and deployed
copy checks below support retaining the live tools and treating launcher/unit pairs as one deploy
unit. The only positive cleanup classification is generated Python cache: it is ignored, absent from
the tracked tree, and explicitly non-deployable in the manifest. Nothing was moved, deleted,
installed, or rewired.

## Candidate dispositions

| candidate | caller and installed-copy evidence | disposition, risk, priority |
|---|---|---|
| `mesh-cam-watch` + `.service`; `mesh-card-watchdog` + `.service`/`.timer`; `mesh-liveness-loop` + `.service`; `mesh-textin` + `.service`; `mesh-tuner-eye` + `.service`; `mesh-voice-rx` + `.service` | All six executable tools are byte-identical to `~/.local/bin`. `mesh-cam-watch.service`, `mesh-liveness-loop.service`, `mesh-textin.service`, and `mesh-voice-rx.service` are active/enabled. The iMac watcher unit is installed but disabled/inactive. Card-watchdog and tuner-eye units are absent from this node's user-unit directory; their tools are installed. `mesh-cam-watch.service` has a local `CAM_CHAT` channel override; `mesh-textin.service` uses an equivalent absolute home path in place of `%h`; liveness-loop, voice-rx, and iMac watcher unit copies are identical to source. | **Expected launcher/unit pairs, not duplicate implementations. Retain together.** High removal risk for active pairs; medium for the node-local inactive/absent units. No delete or unit-normalization task: the observed differences are a node-specific channel override, equivalent path expansion, or non-installed local units—not evidence of dead source. |
| `mesh-imac-cam`, `mesh-imac-cam-watch`, `mesh-imac-cam.m`, `mesh-camera` | The three installed mesh executables (`mesh-imac-cam`, `mesh-imac-cam-watch`, `mesh-camera`) match source byte-for-byte. Caller scan finds consumers including `mesh-bruno`, `mesh-bruno-watch`, `mesh-desk-state`, `mesh-object-id`, `mesh-see`, and `mesh-room-sense-loss`. Source headers distinguish the macOS/iMac Objective-C capture adapter and its watcher from Linux v4l2 `mesh-camera`; the wrapper self-deploys/compiles its `.m` helper on the iMac. | **Distinct platform and capture contracts; no duplicate proven. Retain.** High risk: removing one would break a platform-specific producer or its readers. Revisit only in a named camera migration slice with a caller census. |
| `mesh-body-*`, `mesh-phone-*`, `mesh-note3-*` | All 9 body, 13 phone, and 19 Note3 executables match their `~/.local/bin` copies (41/41). Caller scan found references across 111 files, including `job/mesh-job-calls`, `mesh-card`, `mesh-activity-light`, `mesh-baro`, and `mesh-bruno-watch`. Headers show separate layers/modalities: body power/thermal/load readings and usage fusion, phone transport/sensor adapters, and Note3-specific sensor/actuator interfaces. | **Layered sensor and device interfaces; prefixes alone do not imply duplication. Retain.** High risk because deployed callers and sensor/actuator boundaries exist. No consolidation task until a per-tool overlap claim has measured same-input/same-output behavior. |
| UXN binaries and generated `.rom`/`.sym` files | `git ls-files 'scripts/uxn/bin/*' '*.rom' '*.sym'` finds 27 tracked assets. `scripts/uxn/build.sh` assembles ROMs from `.tal` sources; `scripts/uxn/README.md` documents their runtime role; `scripts/uxn/test-rom-binary-contract` asserts tracked ROM/source/symbol treatment. `scripts/uxn/bin/` itself is ignored by the UXN-local `.gitignore`. | **Retain the tracked ROMs/symbols as build/runtime/test assets; do not infer dead code from generated form.** High risk if excluded from a move or deploy inventory without dependency proof. Defer build-output relocation/exclusion to existing `tg-scripts-layout-migration-20260912` step 7, which requires a UXN build manifest. |
| `scripts/__pycache__/`, `job/__pycache__/` | Both cache directories are ignored by the root `.gitignore` and contain no tracked files. `scripts/mesh-manifest` classifies `.pyc` under `__pycache__` as `kind=asset`, `deploy=none`, `cadence=none`. | **Generated runtime cache, not a production tool; exclude from deployment and future runtime moves.** Low risk to exclude from install enumeration; no deletion was performed. |

## Verification evidence

Read-only checks on this node:

```text
listed candidate executables:         9/9 in launcher/camera sample; all 41 sensor-family copies match
installed body executables:          9/9 byte-identical
installed phone executables:         13/13 byte-identical
installed Note3 executables:         19/19 byte-identical
launcher units active:               cam-watch, liveness-loop, textin, voice-rx
launcher unit enabled/disabled:      cam-watch, liveness-loop, textin, voice-rx enabled;
                                     iMac watcher installed disabled
unit source differences:             cam-watch adds local CAM_CHAT; textin expands %h to the
                                     current home path; neither indicates duplicate/dead code
tracked UXN bin/ROM/SYM assets:       27
Python cache:                        ignored; zero tracked; manifest says deploy=none
```

The candidate caller search is evidence of references, not a claim that every text mention is an
executing call. Positive call-path examples and each tool's declared runtime contract were checked
before disposition. Unit states are this node's current state only; absence/inactivity here does not
prove fleet-wide deadness. No new owner task is necessary for this audit: all candidates now have an
explicit keep/exclude/defer disposition, and the existing migration chain already owns the UXN
manifest prerequisite.

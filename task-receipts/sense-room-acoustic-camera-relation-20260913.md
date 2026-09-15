# Sense enrichment: room-sense acoustic/camera relation

Date: 2026-09-13  
Sense: `mesh-room-sense`

Added `acoustic_camera_relation`, an additive relation between the local ambient-level read and
camera motion classification. It reports `JOINT_ACTIVITY`, `AUDIO_WITH_STILL_CAMERA`,
`CAMERA_MOTION_WITH_QUIET_AUDIO`, or `JOINT_QUIET` only when both inputs are classifiable; any
unavailable or unclassified input yields `UNKNOWN`. The field is exposed in JSON and in `signals=`
(therefore the existing observation tape). It does not alter occupancy, confidence, or degraded
status.

This preserves the useful distinction between, for example, audio activity with a still image and
both channels being quiet. The label is evidence about the pair, not an occupancy claim.

## Verification

- Test-first: before adding the classifier, `mesh-room-sense --test` failed at the new fixture with
  `classify_acoustic_camera_relation: command not found` and exit 1.
- `bash -n scripts/mesh-room-sense`: pass.
- `timeout 120s bash scripts/mesh-room-sense --test`: classifier/regression fixtures completed;
  live gate returned exit 2 with `n/a (BLE organ unreachable — live mesh-presence read exited 2)`.
  The unreachable condition remains explicit and is not converted into empty occupancy.
- `timeout 75s bash scripts/mesh-room-sense --json`: exit 0 with a fresh, real partial artifact at
  `2026-09-13T17:09:55Z`:

  ```json
  {"verdict":"UNCERTAIN","status":"DEGRADED","occupancy":"UNKNOWN","confidence":"low","room_mode":"OFFLINE","degraded":"phone-unreachable,ble-unavailable,body-unknown,wifi-unknown,kbd-unknown","signals":"kbd=UNKNOWN screen=UNKNOWN cam=STILL camera_face=UNKNOWN ble=NONE body=UNKNOWN wifi=UNKNOWN light=LOW ambient=MODERATE acoustic_camera=AUDIO_WITH_STILL_CAMERA ambient_peak_db=-2.1 ambient_coverage=0.985 ambient_age_s=5 ambient_source=tap ambient_clock=UNKNOWN presence_familiarity=INITIAL presence_session_max_s=-1 tamper_recency=COLD audio_self=SILENT","reason":"ambient MODERATE but camera live+STILL & no phone/BLE — likely TV/appliance, not a person","ts":"2026-09-13T17:09:55Z","phone_ok":0,"ble_ok":0,"body":"UNKNOWN","camera_face":"UNKNOWN","ambient":"MODERATE","acoustic_camera_relation":"AUDIO_WITH_STILL_CAMERA","ambient_peak_db":"-2.1","ambient_coverage":"0.985","ambient_age_s":"5","ambient_source":"tap","kbd":"UNKNOWN","presence_familiarity":"INITIAL","presence_session_max_s":-1,"tamper_recency":"COLD","dwell_s":460,"dwell_band":"STABLE","dwell_cov":"100","changes_24h":28}
  ```

- `git diff --check`: pass. No commit made.

# Note3 thermalservice probe — 2026-09-16

Task: `discover-note3-thermalservice-20260916/probe-note3-thermalservice`

## Bounded read-only probe

The authorized USB ADB device was present as `4d00553d61ab90b7` (`SM_N900`):

```text
List of devices attached
4d00553d61ab90b7       device usb:1-3 product:ha3gxx model:SM_N900 device:ha3g transport_id:5
devices_rc=0
```

Command:

```text
timeout 20s adb -s 4d00553d61ab90b7 shell dumpsys thermalservice
```

Raw result:

```text
Can't find service: thermalservice
thermalservice_rc=0
```

## Acceptance and disposition

Acceptance required at least one parseable thermal-status or temperature record. Result:
**0/1 accepted (0%)**. ADB transport is reachable, but this Android 5.0 Note3 exposes no
`thermalservice` dumpsys service, so no new telemetry seam was proven. The command's zero exit
status is not treated as success because its output is an explicit missing-service response.

No phone files, permissions, or substrate were changed. Retry after a different Note3 firmware
or an ADB service listing shows a thermal service; the existing `mesh-note3-thermal` sysfs path
remains the separate already-catalogued thermal read.

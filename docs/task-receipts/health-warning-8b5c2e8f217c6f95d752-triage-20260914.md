# Triage historical USB/SMART discovery FYI

At 2026-09-14T19:13Z, triaged
`health-warning/8b5c2e8f217c6f95d752/triage`, sourced from the 2026-09-11T22:54:35Z
health FYI about `docs/task-receipts/discover-find-verification-20260911.md`.

The cited receipt already separates verified live reads from unknown evidence:
`lsusb` observed the camera, MSI lighting controller and Samsung MTP IDs, and
`v4l2-ctl` observed the camera nodes; `smartctl -H /dev/nvme0n1` returned
`Permission denied`, so SMART health is explicitly `UNKNOWN`, not CLEAN. The
current `mesh-health` reports this node and iMac online and several fleet peers
offline; nothing in the current feed supplies new SMART permission or drive
health evidence. The repository contains no exact active task that can obtain
the missing read without changing privilege/configuration.

Disposition: the FYI is already evidence-backed and its only unresolved part is a
named visibility limit. No safe mesh-owned state change follows from this old
observation. Keep SMART health unknown until the ordinary read succeeds under
authorized existing access; do not infer CLEAN from absence of an error or repeat
the same denied probe without a changed access condition.

## Later live evidence (2026-09-14 19:36Z)

The historical disposition above was correct at 19:13Z. A later `mesh-hw-health` read completed
successfully at 19:36Z and reports SMART overall-health `PASSED`, wear 2%, critical warning
`0x00`, spare 100% (threshold 1%), and zero media errors. This clears the prior SMART visibility
blind for the current read; it does not retroactively change the earlier denied read. Hardware
status was `HW: OK` with a maximum reported temperature of 74°C. No hardware state was changed.

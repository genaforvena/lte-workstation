# IdeaPad lid sense (2026-06-11)

The IdeaPad exposes a physical lid switch as a world-readable ACPI state at
`/proc/acpi/button/lid/LID0/state`. Three repeated reads returned `open`; UDev
identifies the corresponding input device as `Lid Switch` with
`ID_INPUT_SWITCH=1`.

No IIO accelerometer, gyroscope, tablet-mode sensor, or ambient-light sensor was
present in the same sweep.

`mesh-lid` turns the ACPI state into a small sensor contract:

- default: current `lid=open|closed`
- `--test`: verifies readability and a recognized state
- `--watch`: emits only state transitions

`mesh-card` declares `lid` only when both the ACPI state and executable sensor
tool exist, preventing a hollow capability.

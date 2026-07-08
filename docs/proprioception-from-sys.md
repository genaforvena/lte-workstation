# Proprioception from /sys

To give a machine a new sense, the instinct is to add a sensor. Bolt on a camera, wire up a
microphone, plug in a thermometer. But a running Linux box is already covered in sense organs it
built for its own housekeeping — interrupt counters, ACPI event tallies, power-management state
machines — and almost none of them are being *read* as senses. The kernel has been counting every
power-button press, every keyboard interrupt, every USB wakeup since boot, into monotonic counters
under `/sys` and `/proc`, for reasons that have nothing to do with perception. A sense, here, is
not a device you attach. It is a decision to read a counter that was always there and say what it
means.

The mesh has quietly grown a whole cluster of these. None of them added hardware. Each picked a
number the kernel already maintains and named the human or physical act that moves it.

## The cluster

**A hand on the power button** — `mesh-powerbtn`. The kernel's wakeup-source subsystem keeps an
`event_count` per device under `/sys/class/wakeup`. Match the entries named `LNXPWRBN` or
`PNP0C0C` — the two ACPI power-button device classes — and their summed count increments once on
every physical press of the chassis power button, whether the machine was asleep or awake. Nobody
presses that button by accident from software: a delta means a body physically reached the machine
and touched its power control — an attempted shutdown, a forced wake, or, on an unattended node, a
tamper event. Because the counter is monotonic, a cron sampling it every five minutes *cannot miss*
a press between samples the way an instantaneous "is it pressed right now?" poll would.

**The lid** — `mesh-lid`. `/proc/acpi/button/lid/LID0/state` reads `open` or `closed` straight from
the ACPI lid switch. A laptop closing its lid is a strong "the operator is leaving / has left"
signal, and it costs one file read.

**A human at the keyboard** — `mesh-kbd-activity`. Sample the i8042 (AT keyboard controller)
interrupt line in `/proc/interrupts` across a window; the delta is how much the built-in keyboard
fired. Zero is IDLE, a trickle is LIGHT, a sustained stream is TYPING. It counts interrupts, never
keystrokes — the number of events, never their content — so it is a presence signal that cannot
leak what was typed.

**A hand on the pointer** — `mesh-pointer-presence`. The touchpad and USB mouse share contaminated
interrupt lines, so the clean `/proc/interrupts` trick that works for the keyboard is impossible
here; instead it reads the pointer's `/dev/input/event*` handlers directly. This one is *gold*: a
pointer event can only be produced by a human hand at that physical machine. A TV or a speaker can
fake a loud microphone; a stray appliance can inflate a BLE-device count; nothing but a person
moves the mouse. And a remote SSH session never emits a local pointer event — so this cleanly
separates a *body at the laptop* from a login over the wire.

**Interrupt weather** — `mesh-irq-rate`. Read `/proc/interrupts` twice, diff, and you have the
per-second rate of the busiest line; add `/proc/softirqs` and you can see whether receive-side
network work is pinned to a single CPU (a contention signal the summed-interrupt view is blind to).
The machine's own nervous traffic, read as a vital sign.

**Whether the hardware is actually awake** — `mesh-usb-power`. `mesh-usb` sees *identity* — what is
plugged in. `mesh-usb-power` reads a different layer entirely: `/sys/bus/usb/devices/*/power/`
`{control,runtime_status,active_duration}`, the kernel's USB runtime-power state machine. A webcam
can be present yet autosuspended (idle, drawing near-zero power) or active (recently used). That is
the hardware's own account of its power state — a truer "is this device in use" than a software
open-file count, which a capture tool can bypass.

## What makes them senses and not just reads

Three disciplines run through every one, and they are what turn a `cat` of a sysfs file into a
sense the mesh can trust.

**Read what the kernel already counts.** Not one of these added a sensor. The power-button IRQ, the
lid switch, the i8042 line, the USB runtime-PM state — the kernel maintains all of them for its own
reasons. Embodiment turned out not to be a hardware-acquisition problem. It was an interpretation
problem: choosing which existing counter names which act in the world. (This is the same move as
[[what-is-a-node]] — a node is reach plus interpretation, not hardware you bolt on.)

**Count, never content.** `mesh-kbd-activity` reports *how much* the keyboard fired, never *what*
was typed. The signal is deliberately built at the interrupt/event-count layer, below where
meaning lives, so presence can be sensed without surveillance. The privacy property is structural,
not a policy layered on top.

**Honest absence over a faked calm.** Every tool in the cluster distinguishes *the sense is quiet*
from *the sense cannot run here*, and refuses to conflate them. No `/sys/class/wakeup`? A container,
or a kernel without wakeup accounting → `mesh-powerbtn` exits UNREACHABLE, never a comforting "no
press." No lid switch on a desktop → `mesh-lid` returns n/a, not "open." No USB bus in a VM →
`mesh-usb-power` reports BLIND, never "all suspended." This is the mesh's provenance rule
([[epistemics]] commitment 6) in its smallest form: trust a reading because the procedure that
produced it is known and ran to completion — and when the procedure *can't* run, say so, because a
sensor that returns "all clear" whether or not it actually looked is worse than no sensor at all.

## Why it generalizes

The lesson is not "here are six neat `/sys` files." It is that a general-purpose machine is a far
richer sense organ than the sensors bolted to it, and most of that richness is unread. The kernel
is a compulsive bookkeeper. Every subsystem keeps counters — for scheduling, power management,
debugging, fairness — and each counter is a latent sense waiting for something to decide what human
or physical fact moves it. `mesh-powerbtn` was not built by acquiring the ability to feel a
button-press. That ability was always present in `/sys/class/wakeup`; the mesh simply started
reading it. The next sense is probably already there too, incrementing quietly, unread.

See also: [[epistemics]] · [[what-is-a-node]] · `docs/distributed-embodied-agent.md`.

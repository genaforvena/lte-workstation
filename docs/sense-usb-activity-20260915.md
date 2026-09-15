# USB activity sense — 2026-09-15

New live relation: the USB host-controller interrupt delta from `/proc/interrupts` (`xhci_hcd`)
and the count of USB devices whose sysfs `power/runtime_status` is `active`. The joint labels are
`ACTIVE`, `IRQ_ONLY`, `DEVICE_ONLY`, and `QUIET`; either unreadable/reset axis returns UNKNOWN
(exit 2). The tool does not convert missing hardware into zero.

Artifact: `scripts/mesh-usb-activity` (executable, on-demand `orphan-ok`) and its deployed canonical
symlink at `~/.local/bin/mesh-usb-activity`.

Evidence from the live node:

```text
scripts/mesh-usb-activity --test
smoke-test: ok (joint fixtures + REAL USB read: irq_delta|active_before|active_after=387|7|6)

scripts/mesh-usb-activity --json
{"label":"ACTIVE","xhci_irq_delta":356,"active_before":7,"active_after":10,"interval_s":0.2,"ts":"2026-09-15T12:34:50Z"}
```

`mesh-doctor --test` passed. A full `mesh-doctor` run traversed the repository’s long node-aware
smoke/orphan sweep and exceeded the 1200-second wrapper before its terminal summary; its completed
sections had only pre-existing warnings and no `mesh-usb-activity` orphan entry. `mesh-autowire`
also correctly refused this uncommitted source under the repository’s `tracked-at-HEAD` guard, so
the sense remains explicitly on-demand until it is landed; no commit was made.

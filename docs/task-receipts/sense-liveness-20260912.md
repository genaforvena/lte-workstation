# Sense liveness check — 2026-09-12

`mesh-reflex-health --check` found 36 scheduled reflex artifacts fresh, while correctly separating
two live reflexes from their blind organs: `lan-newdevice` and `wifi-link`. This pass used
`wifi-link` as the decayed sense. Its five-minute cron entry is present, but `mesh-wifi-link --test`
returned 2 (`phone unreachable or no termux-wifi-connectioninfo`); the last real link state is
2026-09-03 09:47 UTC and the offline marker was refreshed by a real probe. No Wi-Fi quality reading
was produced, so the reflex heartbeat is not evidence of a live link.

The historical comparison covers both requested ranges. Timestamped `chat.log` rows mentioning
`wifi-link` number 5 in the last 24 hours and 118 in the last 7 days. Neither range contains a real
`[wifi-link]` quality reading; the counts include 1 and 59 blind/offline mentions, respectively.
The nominal five-minute cadence represents 288 and 2,016 scheduled opportunities, but actual
attempt counts cannot be recovered: `wifi-link.log` contains no per-run timestamps. Treat that
denominator as unknown, not as proof every scheduled attempt ran.

`lan-newdevice` also remains blind: `mesh-lan-newdevice --status` reported router DHCP and LAN ARP
unreachable. Its classifier smoke test passed, but it produced no live LAN reading. The source
already labels this axis `DECAYED` (2026-09-12); `mesh-reflex-health` refreshed only its blind marker.
The two absent organs, `kbd-activity` and `wifi-rf`, remain `n/a` per their own gates.

Updated `scripts/mesh-sense-evolve` so the liveness directive requires comparison of timestamped
evidence across 24-hour and 7-day windows, distinguishes real reads from empty/unreachable results,
and treats missing history as UNKNOWN. The new regression assertion failed before the directive
change and `mesh-sense-evolve --test` passes afterward.

Fresh independent real artifact after the liveness decision: `mesh-note3-battery --edge` read the
Note3 over ADB at 2026-09-12 20:23:19 UTC (`present=true level=100/100 temperature=26.3°C power=USB
status=5 voltage=4302mV`) and refreshed
`/home/mesh-home/.mesh/.note3-battery-state` (81 bytes).

No commit made. The live router and phone Wi-Fi organs remain unavailable; their readings stay
blind until a real hardware read succeeds.

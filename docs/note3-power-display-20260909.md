# Note 3 PowerManager/display-state sense

Landed `scripts/mesh-note3-power-display` as a read-only, on-demand ADB organ. It reads one
`dumpsys power` snapshot and emits `ON`, `OFF`, or `UNKNOWN`; it does not cache, write state, post
edges, or actuate the phone.

The live artifact [`artifacts/discover/note3-power-display-20260909.txt`](../artifacts/discover/note3-power-display-20260909.txt)
supplied the parser contract: `mWakefulness`, `mInteractive`, and `mDisplayReady` all parse with
the allowed enum/boolean values (1/1 acceptance). A snapshot's capture age is published; stale,
malformed, contradictory, or unreachable input is `UNKNOWN` rather than a remembered value.

Verification:

- `bash -n scripts/mesh-note3-power-display` — PASS.
- Fixture read with `mWakefulness=Awake`, `mInteractive=true`, `mDisplayReady=true` — `ON`, JSON
  included `age_seconds` and `reason=fresh`.
- Stale fixture — `UNKNOWN`, `reason=stale`, exit 2.
- Contradictory fixture — `UNKNOWN`, `reason=contradictory-fields`, exit 2.
- Live `adb -s 4d00553d61ab90b7 get-state` — `device`; live `mesh-note3-power-display` — `ON`.

No cron/reflex wiring was added: the organ is intentionally read-only and on-demand until a real
consumer exists.

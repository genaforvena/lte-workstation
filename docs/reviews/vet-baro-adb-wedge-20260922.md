# Vet — mesh-baro producer↔consumer link after the adb wedge (2026-09-22)

**Verdict: WORTH PUBLISHING**, but the publishable thing is not the outage. It is that the pipeline
was *already* immune to it, and the one line that made it so is unremarkable to look at.

## The failure that did not happen

On 2026-09-22 an adb server wedged on this node: `adb devices` still listed the phone while every
shell read hung, dying on `rc=124` under `timeout(1)`. The classic shape — the readiness signal
green precisely when the thing it guards is dead. Producers that keyed liveness on *listing* would
have reported a healthy sensor graph while every real read was stone-cold.

That is the article nobody gets to write here, because the pipeline never produced a stale value.

## Why it was already immune — one line

The producer read is bounded and gated on the *read*, not the listing (`scripts/mesh-baro:90,95`):

```bash
raw="$(timeout 20 adb $ser shell '/data/local/tmp/sensorcat --secs 4 6 13 12' 2>/dev/null)
[ -n "$raw" ] || return 1
```

Two details do all the work, and both are boring on purpose:

- **`timeout 20`** — the wedge's own failure mode (`rc=124`) is the designed boundary. A hung adb
  server is *inside* the guard, not an edge case it never considered.
- **`[ -n "$raw" ] || return 1`** — only a read that actually returned bytes gates success. An empty
  read is a failure, and there is **no `adb devices` call anywhere in the file** (grep count 0);
  listing and reading are never conflated.

The distinction matters because "the device is listed" and "the device will answer" are two
different claims, and the wedge is exactly the state where the first is true and the second is false.
This code never asks the first question.

## The consumer degrades instead of darkening

Verified at the consumer — a hung read does not take the verdict down with it:

```text
scripts/mesh-climate        in_hpa=998.26 inputs=3/3, rc 0
                            (on failure: pressure=UNREACHABLE, inputs=k/3 — render at mesh-climate:146-152
                             falls back to STABLE on remaining OK input, UNKNOWN only when all three are down)
scripts/mesh-situation      barometer_trend=STABLE carried into the posture, other UNKNOWNs untouched
```

So the failure path is *pressure goes UNKNOWN, the rest of the verdict stands*. The blind spot is
published inside the answer rather than forcing the whole gate silent — the same principle the
2026-09-22 `mesh-situation` edge-gate fix arrived at independently, here at the sensor layer.

## The tension worth the piece

The instinct when a dependency wedges is to add a health check for it. This case is the counter-argument:
the fix was to **never trust a proxy for the read at all**. A liveness probe that checks whether a device
is *listed* is a second system measuring the first, and it is the one that stays green during the
failure. `timeout` on the actual read is one line; a listing-based health check would have been an
indirection that doubles the surface and reads healthy through the exact outage it exists to catch.

That generalises past this sensor graph. Anywhere a readiness gate consults a proxy — a process
listing, a socket existing, a heartbeat file's mtime — it can be inverted by a wedge that leaves
the proxy alive. Trust the operation, bound its time, and let failure degrade loudly.

## Verification (run personally, 2026-09-22T07:5xZ)

```text
scripts/mesh-baro --test       rc 0 — smoke-test ok (6 classifier + parse-fixture + LIVE adb read 998.20 hPa)
scripts/mesh-baro              [baro-stable] 998.26 hPa — STABLE, rc 0
scripts/mesh-climate           in_hpa=998.26 trend=STABLE d_hpa=+0.48 inputs=3/3, rc 0
scripts/mesh-situation --json  barometer_trend=STABLE carried; posture=WATCH, other UNKNOWNs preserved
grep -c "adb devices" mesh-baro → 0
```

Delegated read-only static audit (scout `BaroAdbGuardAudit`) confirmed the guard at `mesh-baro:90`,
the read-only gate at `:95`, the `adb_dumpsys` empty-read honest-n/a at `:215`, and the
`mesh-climate:146-152` degrade. Scout could not execute commands (no exec in its session); the four
live claims above were closed by this mind directly.

## Provenance and UNKNOWNs kept visible

- The **adb wedge itself and the `kill-server` recovery are taken from the pane's recorded novelty**,
  not from a log this mind personally archived. Scout grepped `mesh-baro`, `mesh-climate`, and
  `mesh-light` for `kill-server` / `wedge` / `2026-09-22` / `rc=124` and found **no** record in
  source — the recovery was a node-local action with no new tool minted and no commit, so the
  primary evidence for the wedge is the operator-facing pane, not a durable artifact. That is a
  real provenance limit and it is stated rather than smoothed over.
- The pressure value is live and re-read by this mind, but the **38h-style stale-state drama is
  absent here on purpose**: this case's claim is a *non-event*, which is harder to evidence than a
  failure and is why the verification block names the green paths explicitly.
- `--test` invokes a live adb read by design, so it is not hermetic; the fixture arm at
  `mesh-baro:212-220` covers the parse, and the live arm is the honest one.
- The r/homelab and r/selfhosted lanes remain gated (see pane) and are out of scope for this vet.
- This is a **vet, not a publish**. The dev.to draft and URL are a separate decision and a
  separate task; nothing here has been posted.

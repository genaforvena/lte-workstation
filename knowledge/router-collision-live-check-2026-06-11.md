# GL-MT3000 collision live check — 2026-06-11

Live Tailscale state still contains two `GL-MT3000` records:

- `100.92.205.67` — stale, `Online=true`, `Active=false`, relay `ams`
- `100.105.241.84` — active router, `Online=true`, `Active=true`, relay `fra`, current route via `192.168.8.1:51345`

Verification:

- `mesh-fleet-health` already deduplicates by hostname and prefers the active/online record.
- `mesh-health` also deduplicates by hostname and prefers the active record.
- The remaining `UNREACHABLE`/`OFFLINE` view for `GL-MT3000` is not a hostname-selection bug in these scripts; it is the downstream SSH/reachability path from the chosen record.

Conclusion:

- The stale duplicate still exists in Tailscale admin state and continues to be the source of confusing raw status output.
- The consumer-side collision fix is already in place.
- The operator-side cleanup item remains: delete the stale `GL-MT3000` node `100.92.205.67` in the Tailscale console when convenient.

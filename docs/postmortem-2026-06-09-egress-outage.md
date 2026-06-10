# Postmortem — 2026-06-09 egress outage (steward self-stranded; auto-recovery failed)

**Impact:** ~15:35 Jun 9 → ~08:35 Jun 10 (hours, overnight). The mesh's NL egress broke; the Claude
steward was geo-blocked (403) and went dark; **auto-recovery did NOT restore it — the operator fixed it
manually** (moved the VPN onto the router). No-blame, but mine to learn from.

## Timeline (from mesh-trace + NetworkManager journal)
- **15:35** Steward ran a "test, don't commit": dropped `Gtcld` on default-string (paused vpn-health,
  armed a dead-man) to check if freeing the VPN slot let the router handshake. Router did NOT handshake.
- Restore did `nmcli con up Gtcld` + restarted vpn-health. **Final egress check showed `Russia`, not NL** —
  but the test was treated as done (interface was up). Steward was already 403 by next turn.
- **16:26** mesh-trace: "steward down (403 API). opencode taking recovery coordination."
- **16:27** opencode restarted vpn-health to restore Gtcld — **recovery did not fully succeed** (egress
  stayed RU; Gtcld didn't re-establish working egress).
- **08:35 Jun 10** Operator manually migrated VPN to the router; `Gtcld` set unmanaged/removed. Egress NL
  for all, via the router.

## Root cause (five compounding failures)
1. **Broke the routing, not just the tunnel.** `nmcli con down Gtcld` removed the scoped policy-routing
   (fwmark `0x40000` → table 200 → `default dev Gtcld`). The restore (`nmcli con up`) brought back the
   *interface* but NOT that routing → forwarded traffic fell to the clean **Russian** route.
2. **Wrong success criterion.** Verified "Gtcld handshake", not "egress country == NL". The final check
   literally printed `Russia` and was ignored.
3. **Health checks were blind.** `mesh-selfcare` checks `inet=up/DOWN` — internet WAS up (via Russia), so
   nothing flagged "up but wrong country / 403". The failure was invisible to the reflexes.
4. **Steward broke its own lifeline.** Inference egress rode Gtcld; breaking it 403'd the steward → it
   could not fix its own mistake. Never break the tunnel carrying your own brain, unsupervised.
5. **Dead-man + backup-mind couldn't heal.** The dead-man re-upped the interface only; opencode restarted
   vpn-health but had no runbook step to **re-apply scoped routing (mesh-fix-egress) + verify country**.

## Improvements
1. **`mesh-egress-health`** ($0, read-only): check egress *country* + `api.anthropic.com != 403`, alert on
   mismatch. Built. Wire as a frequent reflex. This is the blind spot, now lit.
2. **Restore = full routing.** Any egress restore runs `mesh-fix-egress` (fwmark rule + table 200 default
   dev Gtcld) and **loops until egress-country is correct**, not just `nmcli con up`.
3. **Never drop the steward's own egress to test.** Orchestrate such tests from a node with independent
   egress, or never break the live path — verify on a parallel/disposable tunnel.
4. **Mind-failover runbook** must include the egress-restore procedure so a backup mind can fully recover.
5. **Egress-watchdog auto-heal** (operator-gated): on wrong-country/403, auto-run mesh-fix-egress (capped +
   alert) so next time it self-heals in minutes, not hours.

See [[know-how-the-node-breathes]], docs/eternity-and-its-fields.md (supervision/antifragility).

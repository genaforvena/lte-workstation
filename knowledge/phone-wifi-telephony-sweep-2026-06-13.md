# Phone body: wifi-scan + telephony sweep — two more mesh-novel senses (read-only)

Date: 2026-06-13
Node: Redmi 10 (the body) — 100.103.99.16:8022, u0_a386
Mind: capability-research (discover)

Completes the read-only sweep queued after the sensor-matrix inventory
(`phone-sensor-inventory-2026-06-13.md`). Both are senses no other mesh node has.
NOTE: the phone has **no python3** (Bionic/Termux) — parse termux JSON on the laptop side.

## 1. Wi-Fi — `termux-wifi-connectioninfo` + `termux-wifi-scaninfo`

**Connection (live artifact):**
```
ssid GL-MT3000-765  bssid 66:fb:a6:69:f9:bd  rssi -73..-75 dBm  ip 192.168.8.146
freq 2472MHz  link 96Mbps  mac 02:00:00:00:00:00 (randomized — explains the "new MAC" churn)
```
**Scan (live artifact): 28 APs visible.** Strongest neighbors:
`70mai_A400_399e -61` · `SkyNet5G -70` · `MTSRouter_4D0878 -70` · `Keenetic-3244 -74` ·
`GL-MT3000-765 -75` · `N7 -75` · `SkyFall_5G -76` · `Keenetic-5466 -76`.

**Mesh-novel value:**
- **Indoor localization fingerprint** — 28 BSSID+RSSI tuples are a stable location signature that
  works *where GPS fails* (indoors). A change in the visible-AP set = the body moved rooms/buildings,
  without a GPS fix. The mesh's only indoor-position sense.
- **Neighbor-network census / RF environment** — what's broadcasting around the body (incl. a 70mai
  dashcam, several home routers). Coarse occupancy + a security surface (new AP appearing).
- The connection RSSI is also a **link-quality sense** for the body's own uplink.

## 2. Telephony — `termux-telephony-deviceinfo` + `termux-telephony-cellinfo`

**Device (live artifact):**
```
operator MegaFon (25002)  country ru  network_type lte  phone_type gsm  phone_count 2 (dual-SIM)
sim_state ready  data_state disconnected/dormant (wifi is primary)  device_id/sim_serial null (no READ_PHONE_STATE grant)
```
**Cellinfo (live artifact): 4 cells** — 1 **registered LTE** (serving) + 1 neighbor LTE + 2 WCDMA
neighbors. (Per-cell dbm null without the fine-grained signal permission, but registration +
cell count are real.)

**Mesh-novel value:**
- **Carrier-diverse location anchor** — the serving LTE cell is an independent coarse-location signal
  (cell ID → tower area), orthogonal to GPS and Wi-Fi. Three independent location senses now:
  GPS (`mesh-location`), Wi-Fi fingerprint (this), cell (this).
- **Independent LTE uplink presence/health** — `network_type=lte`, `sim_state=ready` confirms the body
  has a **carrier uplink distinct from the home LAN/router path** (docs/body.md "Connectivity:
  out-of-band/backup ingress"). A sense that the body's backup path is alive — even if Wi-Fi drops,
  the LTE leg is there. (data currently dormant because Wi-Fi is primary; the leg is ready.)

## Decision: OFFER, wire on demand (doctrine)

The inventory is the artifact. No consumer is pulling indoor-position or cell-presence yet, so no
poller is wired (avoid churn). Cleanest organs *when demanded*:
- **`mesh-wifi-fingerprint`** — hash the visible-BSSID set → a stable "zone" id; `--edge` on zone
  change = indoor move detection (GPS-free). Feeds `mesh-body-context`'s location slot cheaply.
- **`mesh-uplink`** — body's LTE-leg health/presence (carrier, registered cell, sim_state) as a
  backup-path liveness sense.

Read shape (parse on the laptop, not the phone — no python3 on the body):
```bash
ssh -p 8022 u0_a386@100.103.99.16 "timeout 12 termux-wifi-scaninfo"        # → 28-AP JSON
ssh -p 8022 u0_a386@100.103.99.16 "timeout 10 termux-telephony-cellinfo"   # → cell list JSON
```

# Reticulum radio lane — off-internet transport scope

**Status (2026-07-24):** software lane LIVE on mesh-home (RNS 1.4.0, `rnsd` transport
node, verified E2E Link over TCP — `mesh-rns-linkcheck`). Radio lane = **hardware not yet
acquired**; this doc scopes what to buy and how it wires in. `rnodeconf` (the RNode flasher)
is already installed in `~/.venv-rns/bin` — the toolchain is ready, only the transceiver is
missing.

## Why radio

The TCP/AutoInterface lane still rides the internet uplink (phaedra WG egress here). A LoRa
transceiver gives Reticulum a link that is **independent of any internet or cellular
infrastructure** — hash-addressed, E2E-encrypted, multi-km range, license-free ISM band. This
is the piece that makes the mesh survive an uplink outage, which is the operator's stated goal
("an internet-independent mesh").

## RNode — the reference hardware

Reticulum's native radio interface is **RNode**: open firmware (by Mark Qvist / unsigned.io)
flashed onto commodity ESP32/nRF52 + LoRa-modem boards. It presents to the host over USB
serial and is configured in Reticulum as an `RNodeInterface`. `rnodeconf -a <port>`
auto-installs the firmware; radio params (`--freq --bw --txp --sf --cr`) are set per region.

### Board options (flash-your-own — cheapest path)

| Board | SoC + LoRa modem | GPS | Approx | Notes |
|-------|------------------|-----|--------|-------|
| **LilyGO T-Beam v1.1** | ESP32 + SX1276/78 | yes (NEO-6M) | $35–45 | The classic RNode. GPS useful for future location fusion. 18650 holder. |
| **LilyGO T-Beam Supreme** | ESP32-S3 + SX1262 | yes | $50–65 | Newer SX1262 (better sensitivity/low-power), more RAM. |
| **Heltec LoRa32 V3** | ESP32-S3 + SX1262 | no | $20–30 | OLED, compact, well-supported by RNode autoinstall. |
| **LilyGO T3 / LoRa32** | ESP32 + SX1276 | no | $18–28 | Cheapest viable RNode; no GPS. |
| **RAK4631 (WisBlock)** | nRF52840 + SX1262 | opt module | $30–40 | Lowest power; good for a battery/solar relay node. |

All above are flashed identically via `rnodeconf -a`. **SX1262-based boards are preferred**
for new buys (better link budget + lower idle current than SX127x).

### Turnkey option (no flashing)

- **Official RNode** (handheld / board) from unsigned.io shop — pre-flashed, ~€70–90. Buy
  this if avoiding the flash step is worth the premium; functionally identical interface.

### Frequency / region

- **868 MHz** (EU ISM) — our region (operator EU). License-free at ≤25 mW ERP / duty-cycle
  limits. This is the band to buy.
- 915 MHz (US/ISM), 433 MHz (worldwide, lower throughput) — wrong band for here.
- **Buy the 868 MHz variant explicitly** — boards are band-specific (the SX modem + antenna
  match the band); a 915 MHz board is the wrong purchase.

## How it wires into this node

1. Plug RNode into a USB port on mesh-home → enumerates as `/dev/ttyACM0` or `/dev/ttyUSB0`.
2. Flash once: `~/.venv-rns/bin/rnodeconf -a /dev/ttyACM0` (autoinstall latest firmware),
   then set region params, e.g. EU 868:
   `rnodeconf --freq 868000000 --bw 125000 --txp 22 --sf 8 --cr 5 /dev/ttyACM0`
   (SF8/BW125 is a balanced range/throughput default; SF handshakes with peers' config —
   every RNode on the same channel must share freq/bw/sf/cr).
3. Add to `~/.reticulum/config`:
   ```
   [[RNode LoRa]]
     type = RNodeInterface
     interface_enabled = True
     port = /dev/ttyACM0
     frequency = 868000000
     bandwidth = 125000
     txpower = 22
     spreadingfactor = 8
     codingrate = 5
   ```
4. `systemctl --user restart` the rnsd unit (or restart rnsd); `rnstatus` shows the RNode
   interface Up with its own reachable-peers count.
5. A **second** RNode on another node (or the operator's handheld) closes the first true
   off-internet hop. One transceiver alone proves the interface comes up but cannot prove a
   radio LINK — that needs two radios in range, same as the TCP proof needed two instances.

## Minimum viable radio buy

- **2× LilyGO T-Beam v1.1 (868 MHz)** or **2× Heltec LoRa32 V3 (868 MHz)** — one for
  mesh-home, one for a second mesh node / operator handheld. ~$40–90 total.
- 2× 868 MHz antennas (usually included; confirm SMA + correct band).
- USB cables. 18650 cells if untethered relay use is wanted.

Two radios is the floor because the verification artifact for the radio lane is a **Link over
RF between two nodes**, not "the RNode interface came up" (same doctrine as the TCP proof:
reachable ≠ producing).

## Alternative / adjacent interfaces (not recommended first)

- **KISS/TNC over ham packet radio** (`KISSInterface`) — higher power/range but needs a ham
  license and a TNC + transceiver. Overkill vs LoRa for our goal.
- **Serial `PipeInterface`/`SerialInterface`** — for bridging over an existing radio/modem
  link you already own; no new spectrum benefit on its own.

LoRa/RNode is the correct first radio lane: license-free, cheap, no operator license, and
directly supported by the RNS stack already installed here.

## Verification checklist (when hardware arrives)

- [ ] `rnodeconf -i /dev/ttyACM0` reports the board + firmware version (device present).
- [ ] `rnstatus` shows `RNodeInterface` **Up** after config (interface loaded).
- [ ] Second RNode in range: `rnpath <hash>` resolves + `mesh-rns-linkcheck`-style Link
      round-trips a nonce **over RF with both ethernet/wifi down** (the real off-internet
      artifact — pull the uplink and watch a byte still cross).

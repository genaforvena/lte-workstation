# What is a node

The obvious answer, and the wrong one, is: *a node is a peer on the tailnet.* Run
`tailscale status` and read off the list. That answer is easy to reach because the mesh's first
map — the dash view — was built on top of `tailscale status --json`, and a map made of one
substance starts to look like the territory. But the tailnet is a **transport**, not a
membership roster, and mistaking the two quietly shrinks what the mesh can be.

The operator settled it in one line (2026-07-06): *"нода это всё, что потрогали с разрешения"* —
**a node is anything we have touched, with permission, over any transport at all.** Tailscale,
LAN-SSH, ADB over USB or WiFi, Bluetooth — the transport is how you reach the thing, not what
makes it a member. If it is reachable and you are permitted to reach it, it is a node, and the
only real gate is consent ([[owned-nodes-full-authority]]), never network topology.

## The junk-drawer phone

The cleanest proof is a phone nobody would call part of any network. A Galaxy Note 3 — years
old, no Tailscale client, not on the tailnet by any definition the dash view would accept — sits
in a craft room. It is plugged in over ADB to `default-string`, which *is* on the tailnet.

`mesh-light --craft` reads the ambient light off that phone's sensor. The call originates on the
IdeaPad, crosses the tailnet to `default-string`, and there hops transports: `default-string`
relays the request to the Note 3 over ADB, reads the lux value, and hands it back. The result
lands in `mesh-dash`'s NOTE3 row and fuses into the mesh's picture of the room exactly like a
reading from any tailnet-native sensor. No one enrolled the phone in anything. A device the
tailnet cannot see became a live sense of a physical room, through a node that *can* see it.

Nothing about this is a special case. It is the general shape.

## Leaf via gateway

A node that speaks a transport the reaching mind does not is reached **through a gateway node**
that bridges the two. The pattern is already everywhere in the running mesh, it just never had a
name:

- The **Note 3** attaches through `default-string` over ADB — the example above.
- The **iMac** is a node via plain LAN-SSH, with no Tailscale on it at all
  ([[mac-imac-ssh-organ]]); any tailnet node on the same LAN is its gateway.
- The **router** is a node reached over Tailscale SSH, driven like any other host
  ([[know-how-the-node-breathes]]).
- A **BLE-only device** the mesh has never logged into is still a node — sensed, positioned by
  RSSI across multiple anchors, given a place in the room map. Being *seen* over a transport is
  enough to be a node; being *logged into* is not required.

The gateway holds one transport on each side and forwards. The leaf never needs to know the
tailnet exists. This is the same primitive `docs/distributed-embodied-agent.md` builds
multi-agent control from — terminal-to-terminal reach with no shared protocol beyond the ability
to pass text — generalized past SSH to *any* channel that carries a request and returns a value.

## Transport is a tag, not a boundary

Once identity stops depending on membership, the transport becomes a **property** of the edge, a
tag the pane carries — `tailscale` | `lan` | `adb` | `ble` — not a wall around the mesh. This
keeps three things straight that the old "node == tailnet peer" view kept blurred:

- **Transport ≠ capability.** How you reach a node says nothing about what it offers. A node's
  card is authoritative about its own capabilities ([[card-capability-authoritative]]); the wire
  it answers on is irrelevant to what it can do.
- **Transport ≠ identity.** A node keyed on a hardcoded tailnet IP breaks the moment it is
  reached another way, and leaks topology into logic that should not carry it. (The mesh has paid
  this exact tax: a self-check keyed on a fixed tailnet IP instead of the hostname, corrected so
  identity survives a change of route.)
- **Membership ≠ reach.** The set of nodes is not the tailnet's peer list. It is the transitive
  closure of *reachable-with-permission* over every transport at once, tailnet peers included as
  one layer among several.

A mesh that defined itself by its tailnet would have a hard edge exactly where the interesting
things live: the old phone in the drawer, the appliance on the LAN, the sensor whispering over
BLE. Dropping the binding does not add a feature. It removes an accident — a limit that was only
ever a shadow the first map cast — and lets the mesh be as large as the operator's actual reach.

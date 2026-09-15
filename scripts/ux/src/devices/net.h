/*
Copyright (c) 2026 lte-workstation mesh — MIT, same terms as the vendored uxn tree.

net.h — network device (0xd0) for the vendored uxncli: CONNECT (step 1) + stream BIND
(step 2) + datagram BIND/RECVFROM (step 3).

The port map is copied VERBATIM from uxn2 (src/uxn2.c, enum network_ports @2fbaa62)
so a ROM written for either emulator addresses the same ports. The IMPLEMENTATION is
not ported: uxn2's is welded to SDL_Thread/SDL_PushEvent, and this uxncli's main loop
blocks on fgetc(stdin) with no event pump to deliver a callback into. Ours is plain
POSIX getaddrinfo/connect/accept, blocking and synchronous — no vector, no threads.

CHANNELS. The channel port (df) SELECTS which endpoint every other port addresses:
  channel 0        — the OUTBOUND lane (connect/read/write, step 1)
  channel 1..MAX   — an INBOUND lane: a stream accepted from the bound listener (step 2),
                     or, on the one channel a datagram bind was issued from, the bound
                     datagram socket itself (step 3)
There is one bind at a time; bind (dd/de) puts it up, action 1 (Unbind) takes it down.

STREAM AND DATAGRAM LANES ARE NOT THE SAME LANE WEARING A SCHEME, and the differences are
readable at the ports rather than hidden behind them:

  · a stream bind fans ONE listener across all eight inbound lanes and each state read is
    an accept. A datagram bind occupies the SELECTED CHANNEL ONLY — nothing is accepted, so
    there would be nothing to put in the other seven, and seven lanes answering Bound over
    no socket is a true-looking answer to a question the ROM did not ask.
  · a datagram lane never reads CONNECTED. Bound = up and quiet, HasData = a packet is
    queued. There is no peer to be connected to, and the next packet may be from anyone.
  · the handle (db) names the family: 1 = the outbound lane, 0x01xx = an accepted stream,
    0x02xx = a bound datagram socket. Reading db is also the only way to ask "is anything
    attached" WITHOUT the state port's blocking accept.
  · a datagram bind takes a NAMED address — '*', 0.0.0.0 and :: are all refused, in every
    spelling, because the refusal is made against the resolved sockaddr and not the text.
    A stream bind still takes a written-out '*'; it no longer takes 0.0.0.0 or :: dressed
    as an ordinary host, which it silently did through step 2.
  · a write on a bound datagram lane goes to whoever last wrote to it. With nothing read
    yet there is no address, and the write is refused rather than aimed somewhere.

Binding requires a channel to have been SELECTED FIRST (df != 0). A bind issued while
channel 0 is selected is refused loudly rather than accepted, because the state port
would then answer for the outbound lane — a true answer to a question the ROM did not
ask is still an answer it will misread.

State 5 Binding is NEVER reported: our bind is synchronous, so no window exists in
which it is in progress. A state a ROM can never observe must not be faked.
*/

#define NET_VECTOR   0xd0 /* d0 d1 — accepted and stored, never dispatched */
#define NET_ADDR     0xd2 /* d2 d3 — DEO lb: connect to the NUL-terminated URI at ram[addr] */
#define NET_LENGTH   0xd4 /* d4 d5 — DEO lb: set buffer length · DEI: length the last op moved */
#define NET_READ     0xd6 /* d6 d7 — DEO lb: recv up to length into ram[addr] */
#define NET_WRITE    0xd8 /* d8 d9 — DEO lb: send length bytes from ram[addr] */
#define NET_STATE    0xda /* da    — DEI: state · DEO: action (same byte, as in uxn2) */
#define NET_HANDLE   0xdb /* db dc — DEI: handle of the SELECTED endpoint; 0 is "none" */
#define NET_BINDADDR 0xdd /* dd de — DEO lb: bind on the URI at ram[addr] (+listen if stream) */
#define NET_CHANNEL  0xdf /* df    — endpoint selector: 0 outbound, 1..MAX inbound */

#define NET_MAX_CHANNELS 8

#define NET_STATE_DISCONNECTED 0
#define NET_STATE_CONNECTING   1
#define NET_STATE_CONNECTED    2
#define NET_STATE_HASDATA      3
#define NET_STATE_UNBOUND      4
#define NET_STATE_BINDING      5 /* never reported — our bind is synchronous */
#define NET_STATE_BOUND        6

#define NET_ACTION_DISCONNECT 0
#define NET_ACTION_UNBIND     1

/*
IDENTIFY — our extension to uxn2's action set, and the reason it has to exist.

On an emulator with NO device on this page, emu_dei falls through to `return uxn.dev[addr]`
— a bare memory read of a page nothing writes. State 0 is what comes back, and state 0 IS
Disconnected. So "this emulator has no network at all" and "the far node refused the
connection" arrive at the ROM as the SAME BYTE. Measured on the Note3 (2026-07-24): the
pre-net emulator and a genuine ECONNREFUSED both give net-echo.rom stdout "NA" and rc 2,
byte-identical; only stderr differs, and the old binary is silent there. An absent organ
that answers a plausible state is the declaring-an-organ-before-arming-it shape.

The probe is a write the memory page cannot fake: DEO action 0xd0 makes the DEVICE poke a
magic into the length register. A ROM clears that register first, so a page-only emulator
reads back its own zero.

    #0000 #d4 DEO2   ( clear the length register )
    #d0  #da DEO     ( identify )
    #d4  DEI2        ( d0xx = device present · anything else = no device here )

The HIGH byte is the device, the LOW byte is the STEP, so a ROM tells a connect-only
emulator (d001) from one that also binds a stream (d002) or a datagram (d003) and asks
for what it needs: net-echo wants any d0xx, net-listen refuses below d002, a datagram ROM
refuses below d003. The emulator is now the
thing that drifts across the mesh, and a travelling ROM must be able to ask what it landed
on. A ROM that pinned the WHOLE word would refuse every future step of its own device —
which is why the step is compared as an ordering, never as equality.

INTEROP CAVEAT, stated rather than hidden: uxn2 does not know action 0xd0, so a ROM
probing on uxn2 reads "no device" even though uxn2 HAS one. That is wrong-but-fail-closed
— the ROM refuses instead of fabricating — and it costs uxn2-targeted ROMs nothing, since
they never send the probe. It becomes interop-true only if uxn2 adopts the same action.

THE STEP IS A CLAIM ABOUT THE BINARY, NOT ABOUT THE SOURCE TREE, which is why bumping it
is half a change: mesh-uxn-drift (cadence 23, every 6h) reads this define and compares it
against what the RUNNING emulator answers, so a bump with no rebuild reads as drift on a
node whose source is perfectly correct. Bump and rebuild — and cross-build for the nodes
that have no compiler (cross-build.sh, verify-note3.sh) — in the same change.
*/
#define NET_ACTION_IDENTIFY   0xd0
#define NET_IDENT             0xd003 /* device 0xd0, step 3 — connect, stream bind, datagram bind */

Uint8 net_dei(Uint8 addr);
void net_deo(Uint8 addr);

/*
Copyright (c) 2026 lte-workstation mesh — MIT, same terms as the vendored uxn tree.

net.h — CONNECT-ONLY network device (0xd0) for the vendored uxncli.

The port map is copied VERBATIM from uxn2 (src/uxn2.c, enum network_ports @2fbaa62)
so a ROM written for either emulator addresses the same ports. The IMPLEMENTATION is
not ported: uxn2's is welded to SDL_Thread/SDL_PushEvent, and this uxncli's main loop
blocks on fgetc(stdin) with no event pump to deliver a callback into. Ours is plain
POSIX getaddrinfo+connect, blocking and synchronous — no vector, no threads.

SCOPE (step 1): OUTBOUND ONLY. The bindaddr/channel ports exist so the map stays
verbatim, but binding is refused LOUDLY and reports Unbound — it is never silently
accepted. Threat model is unchanged from the ssh hop the mesh already runs: an
authenticated outbound call the operator's own node initiates.
*/

#define NET_VECTOR   0xd0 /* d0 d1 — accepted and stored, never dispatched in v1 */
#define NET_ADDR     0xd2 /* d2 d3 — DEO lb: connect to the NUL-terminated URI at ram[addr] */
#define NET_LENGTH   0xd4 /* d4 d5 — DEO lb: set buffer length · DEI: length the last op moved */
#define NET_READ     0xd6 /* d6 d7 — DEO lb: recv up to length into ram[addr] */
#define NET_WRITE    0xd8 /* d8 d9 — DEO lb: send length bytes from ram[addr] */
#define NET_STATE    0xda /* da    — DEI: state · DEO: action (same byte, as in uxn2) */
#define NET_HANDLE   0xdb /* db dc — the connection handle; 0 is "none" */
#define NET_BINDADDR 0xdd /* dd de — DEO lb: refused in step 1 */
#define NET_CHANNEL  0xdf /* df    — bound-channel selector; always Unbound in step 1 */

#define NET_STATE_DISCONNECTED 0
#define NET_STATE_CONNECTING   1
#define NET_STATE_CONNECTED    2
#define NET_STATE_HASDATA      3
#define NET_STATE_UNBOUND      4
#define NET_STATE_BINDING      5
#define NET_STATE_BOUND        6

#define NET_ACTION_DISCONNECT 0
#define NET_ACTION_UNBIND     1

Uint8 net_dei(Uint8 addr);
void net_deo(Uint8 addr);

/* 200809L, not 200112L: strdup is only declared from POSIX.1-2008, and under the older
   macro it falls back to an implicit int return — a pointer truncated to 32 bits on a
   64-bit host, i.e. a crash that only shows up once the heap is above 4 GB. */
#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <netdb.h>

#include "../uxn.h"
#include "net.h"

/*
Copyright (c) 2026 lte-workstation mesh — MIT, same terms as the vendored uxn tree.

net.c — network device: CONNECT (step 1) + BIND/ACCEPT (step 2). Blocking, synchronous.

WHY THE DEVICE AT ALL, when the mesh already ships ROMs over ssh: the pipe gives
TRANSPORT, the device gives ADDRESSING. With mesh-uxn-hop the shell wrapper picks the
next hop and the far node needs bash; with this device the travelling ROM picks its own
next hop and the far node needs only uxncli. Step 2 closes the other half — with bind,
the far node's uxncli is the thing that ANSWERS, so a hop needs a shell on neither end.

WHY NOT PORT uxn2's: its endpoint is an SDL_Thread posting SDL_PushEvent into an event
loop, and this uxncli has no pump — its main loop blocks on fgetc(stdin). A ported
version would need a whole event layer to deliver a callback nothing here can receive.
Blocking read/write on DEI/DEO needs neither, so there is no vector and no threads. The
PORT MAP is still copied verbatim, so interop with uxn2-targeted ROMs is free.

THE THREAT MODEL CHANGED IN STEP 2, and saying so is part of the change. Step 1 was
outbound only — an authenticated call the operator's own node initiates, the same shape as
the ssh hop the mesh already runs. A listener ACCEPTS whatever can reach the port, so:
  · the bind address is always NAMED by the ROM. There is no default. Any-address is the
    explicit host '*' (tcp:*:port) and nothing else — a listener on every interface when
    the ROM asked for one is precisely the plausible wrong answer this file exists to
    refuse, and it is the difference between the tailnet and the open LAN.
  · the mesh's own use binds the tailscale address, so reach is the tailnet ACL.

CONTAINMENT, and why each guard is here rather than "obviously fine":
  · ram is a flat 64 KB and a recv/send length comes from the ROM, so every transfer is
    CLAMPED to the page: a ROM asking for 0x2000 bytes at 0xf000 would otherwise write
    0x1000 bytes past the end of the allocation. The clamp is loud.
  · a failed connect must NEVER leave the state readable as Connected, and a failed bind
    must never leave a lane readable as Bound. Every failure path closes the fd, drops the
    endpoint and prints why — the silent-fallback doctrine: a default that is
    indistinguishable from success will be taken for one.
  · a CONNECTED endpoint's state poll does not block. It is the port a ROM reads in a
    loop, so it uses select() with a zero timeout (pure POSIX — MSG_DONTWAIT is not) and
    only then peeks a byte to tell HasData from a peer that closed. The ACCEPT poll is the
    one deliberate exception; its whole reasoning is at net_accept_into.
  · a ROM can ask whether this device EXISTS (action 0xd0 Identify → d002 in the length
    register). Without it an emulator with no d0 page answers Disconnected — the same
    byte a refused connect gives — so "no network here" and "the far node said no" are
    indistinguishable to the program deciding. See net.h for the measured artifact.
*/

static int net_fd[NET_MAX_CHANNELS + 1] = { -1, -1, -1, -1, -1, -1, -1, -1, -1 };
static Uint8 net_state[NET_MAX_CHANNELS + 1];
static int net_listen_fd = -1;
static Uint16 net_buffer_length = 0;
static Uint16 net_success_length = 0;

/* handle 0 means "none" (uxn2's convention). The outbound lane is 1, an inbound lane is
   0x0100|channel, so the two families are never confusable in a ROM's eyes. */
#define NET_OUT_HANDLE 1

/*
EVERY socket op is time-boxed — connect and accept via non-blocking + select, recv/send
via SO_RCVTIMEO/SO_SNDTIMEO. A blocked op must surface as a STATE the ROM can read, never
as a hang: a wedged endpoint is the stale-lease family, and a hung emulator reads green to
everything watching it because it never returns to say otherwise.

A TIMEOUT IS NOT A DISCONNECT. It sets length 0 and leaves the state Connected, so the
ROM can poll or retry; only a real error tears the endpoint down. Collapsing the two would
make a slow peer indistinguishable from a dead one. The same distinction downward: an
accept that expires leaves the lane BOUND, never Disconnected — nobody called is not the
same fact as the listener being gone.
*/
static int
net_timeout_secs(void)
{
	const char *e = getenv("UXN_NET_TIMEOUT");
	int v;
	if(e == NULL || *e == '\0')
		return 10;
	v = atoi(e);
	return v > 0 ? v : 10;
}

static void
net_fail(const char *what, const char *detail)
{
	fprintf(stderr, "net: %s: %s\n", what, detail);
	fflush(stderr);
}

static void
net_say(const char *what, const char *detail, int chan)
{
	fprintf(stderr, "net: %s: %s (channel %d)\n", what, detail, chan);
	fflush(stderr);
}

/*
The channel port SELECTS the endpoint every other port addresses. An out-of-range channel
addresses NOTHING rather than being folded to 0: quietly serving the outbound lane to a
ROM that asked for channel 99 is the wrong-answer-that-looks-right class.
*/
static int
net_chan(void)
{
	int c = uxn.dev[NET_CHANNEL];
	return c > NET_MAX_CHANNELS ? -1 : c;
}

static void
net_deadlines(int fd)
{
	struct timeval tv;
	tv.tv_sec = net_timeout_secs();
	tv.tv_usec = 0;
	setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof tv);
	setsockopt(fd, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof tv);
}

static void
net_drop(int c)
{
	if(c < 0)
		return;
	if(net_fd[c] >= 0)
		close(net_fd[c]);
	net_fd[c] = -1;
	/* an inbound lane returns to the listener's pool; only the outbound lane goes
	   Disconnected, because only it has nothing behind it to wait on */
	net_state[c] = (c > 0 && net_listen_fd >= 0) ? NET_STATE_BOUND : NET_STATE_DISCONNECTED;
}

static void
net_unbind(void)
{
	int c;
	if(net_listen_fd >= 0)
		close(net_listen_fd);
	net_listen_fd = -1;
	for(c = 1; c <= NET_MAX_CHANNELS; c++) {
		net_drop(c);
		net_state[c] = NET_STATE_UNBOUND;
	}
}

/* Clamp a ram transfer to the page. Returns the usable length, 0 if none. */
static Uint16
net_clamp(Uint16 addr, Uint16 len)
{
	Uint32 end = (Uint32)addr + (Uint32)len;
	if(end <= PAGE_SIZE)
		return len;
	fprintf(stderr, "net: transfer of %u at %04x clamped to the page\n",
		(unsigned)len, (unsigned)addr);
	fflush(stderr);
	return (Uint16)(PAGE_SIZE - addr);
}

/*
URI is COLON-separated, not slash-separated: scheme:host:port | host:port | scheme:host |
host. Same shape uxn2 accepts, so the same address string works on both. Only stream/tcp
and datagram/udp are known schemes; an unknown scheme is an error rather than a silent
default to tcp — guessing the transport is exactly the class of fallback that renders a
failure as a plausible success.

passive: resolve for BIND. Only there does the host '*' mean any-address, and only when it
is written out; a MISSING host stays an error in both directions, because the convenient
reading of "no host given" is the one that opens a port on every interface.
*/
static int
net_resolve(const char *uri, struct addrinfo **res, int passive)
{
	struct addrinfo hints;
	char *s, *scheme, *host, *port, *service, *p;
	int rv;

	s = strdup(uri);
	if(s == NULL)
		return EAI_MEMORY;
	scheme = s;
	host = strchr(s, ':');
	port = strrchr(s, ':');
	service = scheme;

	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	if(passive)
		hints.ai_flags = AI_PASSIVE;

	if(host == port) {
		if(host == NULL) {
			host = s, scheme = NULL, port = NULL;
		} else {
			for(p = port + 1; *p; p++) {
				if(isdigit((unsigned char)*p))
					continue;
				port = NULL;
				break;
			}
			if(port != NULL)
				host = s, scheme = NULL;
		}
	}
	if(host[0] == ':') {
		*host++ = '\0';
		if(host[0] == '/' && host[1] == '/')
			host += 2;
	}
	if(port != NULL && port[0] == ':')
		*port++ = '\0';
	if(port != NULL)
		service = port;

	if(scheme != NULL) {
		if(strcmp(scheme, "stream") == 0 || strcmp(scheme, "tcp") == 0)
			hints.ai_socktype = SOCK_STREAM;
		else if(strcmp(scheme, "datagram") == 0 || strcmp(scheme, "udp") == 0)
			hints.ai_socktype = SOCK_DGRAM;
		else {
			net_fail("unknown scheme", scheme);
			free(s);
			return EAI_SERVICE;
		}
	}
	if(port == NULL) {
		net_fail("no port in address", uri);
		free(s);
		return EAI_SERVICE;
	}
	if(passive && hints.ai_socktype != SOCK_STREAM) {
		/* listen() is meaningless on a datagram socket, and a bind that silently became
		   connectionless would answer Bound while nothing could ever be accepted */
		net_fail("bind", "only stream/tcp can be bound — no datagram listener in this build");
		free(s);
		return EAI_SERVICE;
	}
	if(!passive && strcmp(host, "*") == 0) {
		net_fail("connect", "'*' is a BIND address — there is nothing to dial");
		free(s);
		return EAI_NONAME;
	}

	rv = getaddrinfo(passive && strcmp(host, "*") == 0 ? NULL : host, service, &hints, res);
	free(s);
	return rv;
}

/* Copy the NUL-terminated URI out of ram, bounded by the page. */
static int
net_uri_from_ram(Uint16 addr, char *buf, size_t cap)
{
	size_t i;
	for(i = 0; i < cap - 1; i++) {
		Uint32 at = (Uint32)addr + (Uint32)i;
		if(at >= PAGE_SIZE)
			break;
		buf[i] = (char)uxn.ram[at];
		if(buf[i] == '\0')
			return 1;
	}
	buf[i] = '\0';
	return 0; /* ran off the page or the buffer without a terminator */
}

/*
Time-boxed connect: go non-blocking, start the handshake, wait on select for at most the
timeout, then restore blocking mode and install the recv/send deadlines. A plain
blocking connect() to an unreachable host sits in the kernel's SYN retry ladder for
minutes with nothing able to interrupt it.
*/
static int
net_connect_timed(int fd, struct addrinfo *ai)
{
	int flags, err = 0, secs = net_timeout_secs();
	socklen_t elen = sizeof err;
	struct timeval tv;
	fd_set wf;

	flags = fcntl(fd, F_GETFL, 0);
	if(flags < 0 || fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0)
		return -1;
	if(connect(fd, ai->ai_addr, ai->ai_addrlen) != 0) {
		if(errno != EINPROGRESS)
			return -1;
		FD_ZERO(&wf);
		FD_SET(fd, &wf);
		tv.tv_sec = secs;
		tv.tv_usec = 0;
		if(select(fd + 1, NULL, &wf, NULL, &tv) <= 0) {
			errno = ETIMEDOUT;
			return -1;
		}
		if(getsockopt(fd, SOL_SOCKET, SO_ERROR, &err, &elen) < 0 || err != 0) {
			errno = err ? err : ECONNREFUSED;
			return -1;
		}
	}
	if(fcntl(fd, F_SETFL, flags) < 0)
		return -1;
	net_deadlines(fd);
	return 0;
}

static void
net_connect(Uint16 addr)
{
	char uri[512];
	struct addrinfo *res = NULL, *ai;
	int rv, fd = -1;

	net_drop(0);
	if(!net_uri_from_ram(addr, uri, sizeof uri)) {
		net_fail("address is not NUL-terminated within 511 bytes", uri);
		return;
	}
	net_state[0] = NET_STATE_CONNECTING;
	rv = net_resolve(uri, &res, 0);
	if(rv != 0) {
		net_fail(uri, gai_strerror(rv));
		net_state[0] = NET_STATE_DISCONNECTED;
		return;
	}
	for(ai = res; ai != NULL; ai = ai->ai_next) {
		fd = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
		if(fd < 0)
			continue;
		if(net_connect_timed(fd, ai) == 0)
			break;
		close(fd);
		fd = -1;
	}
	freeaddrinfo(res);
	if(fd < 0) {
		net_fail(uri, strerror(errno));
		net_state[0] = NET_STATE_DISCONNECTED;
		return;
	}
	net_fd[0] = fd;
	net_state[0] = NET_STATE_CONNECTED;
}

/*
BIND (step 2). Synchronous: when this returns the listener is up, or it is not and every
inbound lane says Unbound. There is no Binding window, so state 5 is never reported.

A CHANNEL MUST BE SELECTED FIRST. Binding while channel 0 is selected is refused by name,
because the state port would then answer for the outbound lane: the ROM would read
Disconnected — a TRUE answer to a question it did not ask, which it reads as "the bind
failed" or, worse, as the listener's state. Refusing costs the ROM one instruction and
removes the whole class.
*/
static void
net_bind(Uint16 addr)
{
	char uri[512];
	struct addrinfo *res = NULL, *ai;
	int rv, fd = -1, on = 1, c = net_chan();

	if(c < 0) {
		net_fail("bind", "channel out of range — select 1..8 on port df first");
		return;
	}
	if(c == 0) {
		net_fail("bind", "select an inbound channel on df first — channel 0 is the outbound lane");
		return;
	}
	net_unbind(); /* a rebind replaces the listener; two would be one nobody is reading */
	if(!net_uri_from_ram(addr, uri, sizeof uri)) {
		net_fail("bind address is not NUL-terminated within 511 bytes", uri);
		return;
	}
	rv = net_resolve(uri, &res, 1);
	if(rv != 0) {
		net_fail(uri, gai_strerror(rv));
		return;
	}
	for(ai = res; ai != NULL; ai = ai->ai_next) {
		fd = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
		if(fd < 0)
			continue;
		/* REUSEADDR only: a ROM restarting on the same port must not have to wait out
		   TIME_WAIT. REUSEPORT is deliberately NOT set — it would let a second process
		   silently share the port, and "someone else answered" is unattributable. */
		setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof on);
		if(bind(fd, ai->ai_addr, ai->ai_addrlen) == 0
			&& listen(fd, NET_MAX_CHANNELS) == 0)
			break;
		close(fd);
		fd = -1;
	}
	freeaddrinfo(res);
	if(fd < 0) {
		/* every lane is left Unbound by net_unbind above — a failed bind can never be
		   read as Bound, the same rule as a failed connect never reading as Connected */
		net_fail(uri, strerror(errno));
		return;
	}
	net_listen_fd = fd;
	for(c = 1; c <= NET_MAX_CHANNELS; c++)
		net_state[c] = NET_STATE_BOUND;
	net_say("bound", uri, uxn.dev[NET_CHANNEL]);
}

/*
ACCEPT — the one poll that WAITS, deliberately, up to UXN_NET_TIMEOUT.

Reading the state of an inbound lane with no connection is the vector-less equivalent of
uxn2's arrival callback: it is the only place a ROM can learn that a peer has come. A
zero-timeout poll would be honest and would force every listening ROM into a spin loop
burning a core to wait on a socket — a listening node the mesh cannot afford to leave up.
So it blocks with the SAME deadline as every other op here, and on expiry answers BOUND:
"the listener is up, nobody called". Never Connected (there is no peer), never
Disconnected (the listener is fine). A ROM wanting a cheap look lowers UXN_NET_TIMEOUT; a
ROM wanting to wait longer loops, which now costs it nothing.

The wait is a select() on the listener, so the deadline is real and observable in WALL
CLOCK — which is how the gate asserts it, because a deadline nobody has watched fire is a
hang waiting for its first slow peer.
*/
static int
net_accept_into(int c)
{
	fd_set rf;
	struct timeval tv;
	int fd;

	if(net_listen_fd < 0)
		return 0;
	FD_ZERO(&rf);
	FD_SET(net_listen_fd, &rf);
	tv.tv_sec = net_timeout_secs();
	tv.tv_usec = 0;
	if(select(net_listen_fd + 1, &rf, NULL, NULL, &tv) <= 0)
		return 0; /* nobody called — the lane stays Bound */
	fd = accept(net_listen_fd, NULL, NULL);
	if(fd < 0) {
		net_fail("accept", strerror(errno));
		return 0;
	}
	net_deadlines(fd);
	net_fd[c] = fd;
	net_state[c] = NET_STATE_CONNECTED;
	net_say("accepted", "inbound connection", c);
	return 1;
}

/*
Readable-without-blocking, then one peeked byte to separate "data waiting" from "peer
closed". select() alone cannot tell them apart: EOF makes a socket readable forever.
*/
static Uint8
net_live_state(int c)
{
	fd_set rf;
	struct timeval tv;
	char b;
	ssize_t n;

	if(net_fd[c] < 0)
		return net_state[c];
	FD_ZERO(&rf);
	FD_SET(net_fd[c], &rf);
	tv.tv_sec = 0;
	tv.tv_usec = 0;
	if(select(net_fd[c] + 1, &rf, NULL, NULL, &tv) <= 0)
		return NET_STATE_CONNECTED;
	n = recv(net_fd[c], &b, 1, MSG_PEEK);
	if(n > 0)
		return NET_STATE_HASDATA;
	if(n == 0) {
		net_drop(c); /* Bound again on an inbound lane, Disconnected on the outbound one */
		return net_state[c];
	}
	return NET_STATE_CONNECTED;
}

static Uint8
net_chan_state(int c)
{
	if(c < 0)
		return NET_STATE_UNBOUND; /* an out-of-range channel addresses no endpoint */
	if(c == 0)
		return net_live_state(0);
	if(net_listen_fd < 0)
		return NET_STATE_UNBOUND;
	if(net_fd[c] < 0 && !net_accept_into(c))
		return NET_STATE_BOUND;
	return net_live_state(c);
}

static Uint16
net_handle(int c)
{
	if(c < 0 || net_fd[c] < 0)
		return 0;
	return c == 0 ? NET_OUT_HANDLE : (Uint16)(0x0100 | c);
}

static void
net_read(void)
{
	Uint16 addr = PEEK2(&uxn.dev[NET_READ]), len;
	int c = net_chan();
	ssize_t n;

	net_success_length = 0;
	if(c < 0 || net_fd[c] < 0) {
		net_fail("read", "not connected");
		return;
	}
	len = net_clamp(addr, net_buffer_length);
	if(len == 0)
		return;
	n = recv(net_fd[c], &uxn.ram[addr], len, 0);
	if(n < 0) {
		if(errno == EAGAIN || errno == EWOULDBLOCK) {
			/* deadline hit, peer may still be alive: length 0, state stays Connected */
			net_fail("read", "timed out — length 0, still connected");
			return;
		}
		net_fail("read", strerror(errno));
		net_drop(c);
		return;
	}
	if(n == 0) { /* orderly close — length 0 AND the state says why */
		net_drop(c);
		return;
	}
	net_success_length = (Uint16)n;
}

static void
net_write(void)
{
	Uint16 addr = PEEK2(&uxn.dev[NET_WRITE]), len;
	int c = net_chan();
	ssize_t n;

	net_success_length = 0;
	if(c < 0 || net_fd[c] < 0) {
		net_fail("write", "not connected");
		return;
	}
	len = net_clamp(addr, net_buffer_length);
	if(len == 0)
		return;
	n = send(net_fd[c], &uxn.ram[addr], len, 0);
	if(n < 0) {
		if(errno == EAGAIN || errno == EWOULDBLOCK) {
			net_fail("write", "timed out — length 0, still connected");
			return;
		}
		net_fail("write", strerror(errno));
		net_drop(c);
		return;
	}
	net_success_length = (Uint16)n; /* a short write is REPORTED, never retried silently */
}

Uint8
net_dei(Uint8 addr)
{
	switch(addr) {
	case NET_STATE: return net_chan_state(net_chan());
	case NET_LENGTH: return net_success_length >> 8;
	case NET_LENGTH + 1: return net_success_length & 0xff;
	/* the handle describes the SELECTED endpoint and is computed on read: a handle stored
	   at connect time goes stale the moment the ROM selects another channel */
	case NET_HANDLE: return net_handle(net_chan()) >> 8;
	case NET_HANDLE + 1: return net_handle(net_chan()) & 0xff;
	}
	return uxn.dev[addr];
}

void
net_deo(Uint8 addr)
{
	switch(addr) {
	case NET_ADDR + 1:
		net_connect(PEEK2(&uxn.dev[NET_ADDR]));
		break;
	case NET_LENGTH + 1:
		net_buffer_length = PEEK2(&uxn.dev[NET_LENGTH]);
		break;
	case NET_READ + 1:
		net_read();
		break;
	case NET_WRITE + 1:
		net_write();
		break;
	case NET_STATE: /* same byte as the state port, per the uxn2 map */
		switch(uxn.dev[NET_STATE]) {
		case NET_ACTION_DISCONNECT: net_drop(net_chan()); break;
		case NET_ACTION_UNBIND: net_unbind(); break;
		case NET_ACTION_IDENTIFY:
			/* the one answer a device-less memory page cannot forge — see net.h */
			net_success_length = NET_IDENT;
			break;
		default: net_fail("unknown action", "only 0 Disconnect, 1 Unbind and d0 Identify exist"); break;
		}
		break;
	case NET_BINDADDR + 1:
		net_bind(PEEK2(&uxn.dev[NET_BINDADDR]));
		break;
	case NET_CHANNEL:
		/* refused where it is WRITTEN, so the ROM learns at the selection rather than
		   three ports later through a read that quietly addressed nothing */
		if(uxn.dev[NET_CHANNEL] > NET_MAX_CHANNELS)
			net_fail("channel out of range", "0 is outbound, 1..8 are inbound lanes");
		break;
	}
}

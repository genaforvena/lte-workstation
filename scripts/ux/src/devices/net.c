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
#include <netinet/in.h>
#include <netdb.h>

#include "../uxn.h"
#include "net.h"

/*
Copyright (c) 2026 lte-workstation mesh — MIT, same terms as the vendored uxn tree.

net.c — network device: CONNECT (step 1) + BIND/ACCEPT (step 2) + DATAGRAM BIND/RECVFROM
(step 3). Blocking, synchronous.

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
  · a ROM can ask whether this device EXISTS (action 0xd0 Identify → d003 in the length
    register). Without it an emulator with no d0 page answers Disconnected — the same
    byte a refused connect gives — so "no network here" and "the far node said no" are
    indistinguishable to the program deciding. See net.h for the measured artifact.

STEP 3 ADDS THE DATAGRAM LISTENER, and it is a different animal from the stream one in
three ways that each had to be spelled out rather than inherited:

  · THE ANY-ADDRESS IS REFUSED IN EVERY SPELLING on a datagram bind — '*', 0.0.0.0, ::,
    and a missing host alike. A stream listener still accepts a written-out '*' (step 2's
    contract, unchanged), because a stream peer must complete a handshake this node can
    see and drop. A datagram lane has no handshake: whatever can put a packet on the wire
    is already inside the ROM's read loop, and the ROM this exists for merges what it
    reads into a ledger. uxn carries no crypto; the whole authentication story is the
    tailnet ACL, and an ACL only means something if the socket is on the tailnet address.
    So a datagram listener binds a NAMED address or it does not come up.
  · 0.0.0.0 and :: are now refused on a STREAM bind too, and that is a bug fix, not a new
    rule: this file already claimed any-address was "the explicit host '*' and nothing
    else", while `tcp:0.0.0.0:port` sailed through net_resolve as an ordinary named host
    and opened every interface. A doctrine the code does not enforce is a comment.
  · A DATAGRAM LANE IS NEVER "CONNECTED" and never accepts. The bound socket IS the
    endpoint, on the selected channel and no other; state reads Bound (up, nothing came)
    or HasData (a packet is queued). Saying Connected would name a peer relationship that
    does not exist and will not exist for the next packet either. The handle says so too:
    0x02xx is a datagram lane, 0x01xx an accepted stream, 1 the outbound lane — three
    families a ROM can tell apart, because "which kind of thing am I holding" is exactly
    the question a wrong answer to is unrecoverable.
*/

static int net_fd[NET_MAX_CHANNELS + 1] = { -1, -1, -1, -1, -1, -1, -1, -1, -1 };
static Uint8 net_state[NET_MAX_CHANNELS + 1];
static int net_listen_fd = -1;
static Uint16 net_buffer_length = 0;
static Uint16 net_success_length = 0;

/* per-lane: is this endpoint a datagram socket? Set at connect (outbound) and at bind
   (inbound), cleared on every drop. It is not derivable after the fact — a fd tells you
   nothing about how it was made — and every branch below that behaves differently for
   datagrams reads it, so a lane that lost this flag would be quietly mis-served. */
static Uint8 net_lane_dgram[NET_MAX_CHANNELS + 1];

/* the last sender on a datagram lane, which is the ONLY address a reply can go to: the
   socket is unconnected by construction, so send(2) has nowhere to aim. Length 0 means
   nothing has been received yet, and a write then refuses instead of guessing. */
static struct sockaddr_storage net_peer[NET_MAX_CHANNELS + 1];
static socklen_t net_peer_len[NET_MAX_CHANNELS + 1];

/* handle 0 means "none" (uxn2's convention). The outbound lane is 1, an accepted stream is
   0x0100|channel and a bound datagram lane is 0x0200|channel, so the three families are
   never confusable in a ROM's eyes. */
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

/*
A REFUSAL FROM net_resolve HAS ALREADY SAID WHY, and its callers must not say it again in
another vocabulary. Returning EAI_SERVICE/EAI_NONAME made them print gai_strerror on top —
so a datagram bind on '*' answered with our named refusal AND "Name or service not known",
which points at DNS, a layer that was never involved. An error message names a cause; a
second one names the wrong cause and is where the next hour goes.
*/
#define NET_REFUSED (-9999)

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
	int was_dgram;
	if(c < 0)
		return;
	if(net_fd[c] >= 0)
		close(net_fd[c]);
	net_fd[c] = -1;
	was_dgram = net_lane_dgram[c];
	net_lane_dgram[c] = 0;
	net_peer_len[c] = 0;
	if(c == 0) {
		net_state[0] = NET_STATE_DISCONNECTED;
		return;
	}
	/* a datagram lane has NO listener behind it — the bound socket was the endpoint, so
	   closing it IS unbinding, and reporting Bound afterwards would name a socket that is
	   gone. An accepted stream returns to the listener's pool, which is still up. */
	if(was_dgram) {
		net_state[c] = NET_STATE_UNBOUND;
		return;
	}
	net_state[c] = net_listen_fd >= 0 ? NET_STATE_BOUND : NET_STATE_DISCONNECTED;
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
IS THIS RESOLVED ADDRESS THE ANY-ADDRESS? Asked of the SOCKADDR, never of the string,
because that is the only place the question has one answer: '*', 0.0.0.0, ::, 0, 0x0,
::ffff:0.0.0.0 and an empty host all arrive at getaddrinfo as different text and leave it
as the same in_addr. A guard that pattern-matched the spelling would refuse the two forms
somebody thought of and wave through the rest — and every one of them opens the node.
*/
static int
net_any_addr(struct addrinfo *list)
{
	struct addrinfo *ai;
	for(ai = list; ai != NULL; ai = ai->ai_next) {
		if(ai->ai_addr->sa_family == AF_INET
			&& ((struct sockaddr_in *)ai->ai_addr)->sin_addr.s_addr == INADDR_ANY)
			return 1;
		if(ai->ai_addr->sa_family == AF_INET6
			&& memcmp(&((struct sockaddr_in6 *)ai->ai_addr)->sin6_addr,
				&in6addr_any, sizeof in6addr_any) == 0)
			return 1;
	}
	return 0;
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

TWO BIND-SIDE REFUSALS LIVE HERE, and they are different rules:
  · a DATAGRAM bind refuses the any-address in every spelling. There is no handshake to
    watch, the ROM merges what it reads, and the tailnet ACL is the entire authentication
    story — so it binds a named address or it does not come up.
  · a STREAM bind still takes a written-out '*' (step 2's contract), but no longer takes
    0.0.0.0 or :: dressed as a host. Those were reaching bind(2) as ordinary named hosts
    and opening every interface while this file claimed '*' was the only way to ask.
*/
static int
net_resolve(const char *uri, struct addrinfo **res, int passive)
{
	struct addrinfo hints;
	char *s, *scheme, *host, *port, *service, *p;
	int rv, star;

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
			return NET_REFUSED;
		}
	}
	if(port == NULL) {
		net_fail("no port in address", uri);
		free(s);
		return NET_REFUSED;
	}
	if(!passive && strcmp(host, "*") == 0) {
		net_fail("connect", "'*' is a BIND address — there is nothing to dial");
		free(s);
		return NET_REFUSED;
	}
	star = strcmp(host, "*") == 0;
	if(passive && star && hints.ai_socktype != SOCK_STREAM) {
		net_fail("bind", "a datagram listener takes a NAMED address, never '*' — nothing "
			"handshakes on a datagram lane, so every host that can reach this node would "
			"be inside the ROM's read loop, and uxn's only authentication is the tailnet ACL");
		free(s);
		return NET_REFUSED;
	}

	rv = getaddrinfo(passive && star ? NULL : host, service, &hints, res);
	if(rv == 0 && passive && !star && net_any_addr(*res)) {
		/* the address resolved to 0.0.0.0/:: — the any-address under a host's name. It is
		   refused rather than corrected, because "did you mean every interface" is a
		   question only the ROM can answer and the wrong answer opens the node. */
		if(hints.ai_socktype == SOCK_STREAM)
			net_fail("bind", "that address IS the any-address (0.0.0.0/::) — write it out "
				"as '*' if binding every interface is what you meant");
		else
			net_fail("bind", "that address IS the any-address (0.0.0.0/::), and a datagram "
				"listener takes a NAMED address — there is no any-address form on this lane, "
				"not even the written-out '*'");
		freeaddrinfo(*res);
		*res = NULL;
		free(s);
		return NET_REFUSED;
	}
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
	int rv, fd = -1, dgram = 0;

	net_drop(0);
	if(!net_uri_from_ram(addr, uri, sizeof uri)) {
		net_fail("address is not NUL-terminated within 511 bytes", uri);
		return;
	}
	net_state[0] = NET_STATE_CONNECTING;
	rv = net_resolve(uri, &res, 0);
	if(rv != 0) {
		if(rv != NET_REFUSED) /* a refusal has already said why, in the right words */
			net_fail(uri, gai_strerror(rv));
		net_state[0] = NET_STATE_DISCONNECTED;
		return;
	}
	for(ai = res; ai != NULL; ai = ai->ai_next) {
		fd = socket(ai->ai_family, ai->ai_socktype, ai->ai_protocol);
		if(fd < 0)
			continue;
		if(net_connect_timed(fd, ai) == 0) {
			/* captured HERE: freeaddrinfo below takes the answer away, and every
			   read/write branch downstream needs to know which kind of lane this is */
			dgram = ai->ai_socktype == SOCK_DGRAM;
			break;
		}
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
	net_lane_dgram[0] = (Uint8)dgram;
	/* NOTE, stated because it is a real limit of this lane and not an oversight: a datagram
	   connect() only records a peer — no packet leaves, so nothing on the far side has to
	   exist for this to read Connected. What "connected" can mean for a connectionless
	   socket is the open question the net-boundary task carries; it is NOT closed here. */
	net_state[0] = NET_STATE_CONNECTED;
}

/*
BIND (step 2 stream, step 3 datagram). Synchronous: when this returns the listener is up,
or it is not and every inbound lane says Unbound. No Binding window, so state 5 is never
reported.

A DATAGRAM BIND OCCUPIES EXACTLY THE SELECTED CHANNEL and no other, because there is
nothing to accept: the bound socket IS the endpoint. The stream path fans one listener out
across all eight lanes; the datagram path would have nothing to put in the other seven, and
seven lanes reading Bound with no socket behind them is the plausible-wrong-answer class
this file exists to refuse. Either kind of bind replaces whatever was bound before — two
listeners would be one nobody is reading.

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
	int rv, fd = -1, on = 1, dgram = 0, c = net_chan(), lane;

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
		if(rv != NET_REFUSED)
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
		/* listen(2) is meaningless on a datagram socket — the ORIGINAL reason this whole
		   scheme was refused. It is skipped, never faked: a bind that quietly became a
		   stream would answer Bound while nothing could ever arrive on it. */
		dgram = ai->ai_socktype == SOCK_DGRAM;
		if(bind(fd, ai->ai_addr, ai->ai_addrlen) == 0
			&& (dgram || listen(fd, NET_MAX_CHANNELS) == 0))
			break;
		close(fd);
		fd = -1;
		dgram = 0;
	}
	freeaddrinfo(res);
	if(fd < 0) {
		/* every lane is left Unbound by net_unbind above — a failed bind can never be
		   read as Bound, the same rule as a failed connect never reading as Connected */
		net_fail(uri, strerror(errno));
		return;
	}
	if(dgram) {
		net_deadlines(fd);
		net_fd[c] = fd;
		net_lane_dgram[c] = 1;
		net_peer_len[c] = 0;
		net_state[c] = NET_STATE_BOUND;
		net_say("bound (datagram)", uri, c);
		return;
	}
	net_listen_fd = fd;
	for(lane = 1; lane <= NET_MAX_CHANNELS; lane++)
		net_state[lane] = NET_STATE_BOUND;
	net_say("bound", uri, c);
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
	/* A DATAGRAM SOCKET HAS NO EOF, so the peek below cannot be run on one: a legal EMPTY
	   packet peeks as 0 bytes, which on a stream means "the peer closed" — and the lane
	   would be torn down by any host willing to send nothing. Readable IS HasData here. */
	if(net_lane_dgram[c])
		return NET_STATE_HASDATA;
	n = recv(net_fd[c], &b, 1, MSG_PEEK);
	if(n > 0)
		return NET_STATE_HASDATA;
	if(n == 0) {
		net_drop(c); /* Bound again on an inbound lane, Disconnected on the outbound one */
		return net_state[c];
	}
	return NET_STATE_CONNECTED;
}

/*
THE DATAGRAM WAIT — the accept poll's counterpart, and the same deliberate blocking read.

An inbound datagram lane is never CONNECTED: there is no peer relationship to be in, and
naming one would tell a ROM it holds something that will not be there for the next packet.
It answers BOUND (the socket is up, nothing arrived within the deadline) or HASDATA (a
packet is queued) — which is also why a ROM can poll it in a loop without a spin: the wait
is the device's, with the same UXN_NET_TIMEOUT as every other op, so a silent wire surfaces
as a readable state and never as a hang.
*/
static Uint8
net_dgram_state(int c)
{
	fd_set rf;
	struct timeval tv;

	if(net_fd[c] < 0)
		return NET_STATE_UNBOUND;
	FD_ZERO(&rf);
	FD_SET(net_fd[c], &rf);
	tv.tv_sec = net_timeout_secs();
	tv.tv_usec = 0;
	if(select(net_fd[c] + 1, &rf, NULL, NULL, &tv) <= 0)
		return NET_STATE_BOUND; /* nobody sent — the socket is fine, which is the point */
	return NET_STATE_HASDATA;
}

static Uint8
net_chan_state(int c)
{
	if(c < 0)
		return NET_STATE_UNBOUND; /* an out-of-range channel addresses no endpoint */
	if(c == 0)
		return net_live_state(0);
	if(net_lane_dgram[c])
		return net_dgram_state(c); /* nothing to accept: the bound socket is the endpoint */
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
	if(c == 0)
		return NET_OUT_HANDLE;
	/* 0x02xx says datagram, 0x01xx says accepted stream. A ROM that could not tell them
	   apart would read a bound socket as a caller that had already arrived. */
	return (Uint16)((net_lane_dgram[c] ? 0x0200 : 0x0100) | c);
}

/*
RECVFROM (step 3). Three things a stream recv can assume and a datagram recv cannot:

  · n == 0 IS NOT A CLOSE. It is a legal EMPTY packet. Reading it as an orderly close, the
    way the stream path correctly does, would hand any host that can reach the port a
    one-packet teardown of our listener — a remote unbind, spelled as a normal read.
  · A DATAGRAM TOO BIG FOR THE BUFFER IS DISCARDED, LOUDLY, not delivered short. The
    kernel truncates silently and the ROM cannot see the cut, so half a record would parse
    as a whole shorter one. MSG_TRUNC makes the real size visible where it exists; where it
    does not, a packet that exactly fills the buffer is called out as possibly cut, because
    "cannot tell" must not print as "fine".
  · THE SENDER IS THE ONLY REPLY ADDRESS. The socket is unconnected by construction, so it
    is recorded here or a reply has nowhere to go. It is recorded even for a packet we then
    refuse: who sent it is still true.

An empty packet and an expired deadline both leave the ROM reading length 0 — the ports
have no way to separate them — so both say which they were on stderr. That is the honest
limit of a 16-bit length register, stated rather than papered over.
*/
static void
net_dgram_read(int c, Uint16 addr, Uint16 len)
{
	struct sockaddr_storage from;
	socklen_t flen = sizeof from;
	ssize_t n;
	int flags = 0;
#ifdef MSG_TRUNC
	flags = MSG_TRUNC; /* returns the REAL datagram size, so an oversized one is detectable */
#endif
	memset(&from, 0, sizeof from);
	n = recvfrom(net_fd[c], &uxn.ram[addr], len, flags, (struct sockaddr *)&from, &flen);
	if(n < 0) {
		if(errno == EAGAIN || errno == EWOULDBLOCK) {
			net_fail("read", "no datagram within the deadline — length 0, still bound");
			return;
		}
		net_fail("read", strerror(errno));
		net_drop(c);
		return;
	}
	if(flen > 0 && flen <= sizeof from) {
		memcpy(&net_peer[c], &from, sizeof from);
		net_peer_len[c] = flen;
	}
	if((size_t)n > (size_t)len) {
		fprintf(stderr, "net: read: datagram of %ld bytes does not fit %u — DISCARDED, "
			"raise the length; a short record reads as a whole smaller one\n",
			(long)n, (unsigned)len);
		fflush(stderr);
		return;
	}
#ifndef MSG_TRUNC
	if((size_t)n == (size_t)len)
		net_fail("read", "datagram exactly filled the buffer — it MAY have been truncated "
			"and this build cannot tell (no MSG_TRUNC); raise the length to be sure");
#endif
	if(n == 0)
		net_fail("read", "empty datagram received — length 0, and the lane is NOT closed "
			"(a datagram socket has no close)");
	net_success_length = (Uint16)n;
}

static void
net_read(void)
{
	Uint16 addr = PEEK2(&uxn.dev[NET_READ]), len;
	int c = net_chan();
	ssize_t n;

	net_success_length = 0;
	if(c < 0 || net_fd[c] < 0) {
		net_fail("read", "no endpoint on this channel — nothing connected or bound");
		return;
	}
	len = net_clamp(addr, net_buffer_length);
	if(len == 0)
		return;
	if(net_lane_dgram[c]) {
		net_dgram_read(c, addr, len);
		return;
	}
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
		net_fail("write", "no endpoint on this channel — nothing connected or bound");
		return;
	}
	len = net_clamp(addr, net_buffer_length);
	if(len == 0)
		return;
	if(net_lane_dgram[c] && c > 0) {
		/* A BOUND DATAGRAM LANE REPLIES TO WHOEVER LAST WROTE TO IT and to nobody else:
		   the socket is unconnected, so send(2) has no destination, and inventing one —
		   the last peer of some other lane, a broadcast — is the class of guess this file
		   refuses. With nothing received yet there is no address, and that is said. */
		if(net_peer_len[c] == 0) {
			net_fail("write", "no datagram sender recorded on this lane — a bound datagram "
				"lane replies to the last packet it read, so read one first");
			return;
		}
		n = sendto(net_fd[c], &uxn.ram[addr], len, 0,
			(struct sockaddr *)&net_peer[c], net_peer_len[c]);
	} else
		n = send(net_fd[c], &uxn.ram[addr], len, 0);
	if(n < 0) {
		if(errno == EAGAIN || errno == EWOULDBLOCK) {
			net_fail("write", "timed out — length 0, still connected");
			return;
		}
		net_fail("write", strerror(errno));
		/* a datagram lane survives a failed send: not reaching ONE peer says nothing about
		   the socket, and the next packet may come from somebody else entirely */
		if(!net_lane_dgram[c])
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

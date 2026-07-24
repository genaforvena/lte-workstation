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

net.c — CONNECT-ONLY network device. One endpoint, blocking, synchronous.

WHY THE DEVICE AT ALL, when the mesh already ships ROMs over ssh: the pipe gives
TRANSPORT, the device gives ADDRESSING. With mesh-uxn-hop the shell wrapper picks the
next hop and the far node needs bash; with this device the travelling ROM picks its own
next hop and the far node needs only uxncli.

WHY NOT PORT uxn2's: its endpoint is an SDL_Thread posting SDL_PushEvent into an event
loop, and this uxncli has no pump — its main loop blocks on fgetc(stdin). A ported
version would need a whole event layer to deliver a callback nothing here can receive.
Blocking read/write on DEI/DEO needs neither, so v1 has no vector and no threads. The
PORT MAP is still copied verbatim, so interop with uxn2-targeted ROMs is free.

CONTAINMENT, and why each guard is here rather than "obviously fine":
  · ram is a flat 64 KB and a recv/send length comes from the ROM, so every transfer is
    CLAMPED to the page: a ROM asking for 0x2000 bytes at 0xf000 would otherwise write
    0x1000 bytes past the end of the allocation. The clamp is loud.
  · a failed connect must NEVER leave the state readable as Connected. Every failure
    path sets Disconnected, closes the fd, zeroes the handle and prints why — the
    silent-fallback doctrine: a default that is indistinguishable from success will be
    taken for one.
  · the STATE poll must not block. It is the one port a ROM reads in a loop, so it uses
    select() with a zero timeout (pure POSIX — MSG_DONTWAIT is not) and only then peeks
    a byte to tell HasData from a peer that closed.
  · binding is refused LOUDLY and reads Unbound. An unimplemented port that answered a
    plausible state would be an organ declared before it was armed.
*/

static int net_fd = -1;
static Uint8 net_state = NET_STATE_DISCONNECTED;
static Uint16 net_buffer_length = 0;
static Uint16 net_success_length = 0;

/* handle 0 means "none" (uxn2's convention); step 1 has exactly one endpoint, handle 1 */
#define NET_LIVE_HANDLE 1

/*
EVERY socket op is time-boxed — connect via non-blocking + select, recv/send via
SO_RCVTIMEO/SO_SNDTIMEO. A blocked read must surface as a STATE the ROM can read, never
as a hang: a wedged endpoint is the stale-lease family, and a hung emulator reads green
to everything watching it because it never returns to say otherwise.

A TIMEOUT IS NOT A DISCONNECT. It sets length 0 and leaves the state Connected, so the
ROM can poll or retry; only a real error tears the endpoint down. Collapsing the two
would make a slow peer indistinguishable from a dead one.
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
net_drop(void)
{
	if(net_fd >= 0)
		close(net_fd);
	net_fd = -1;
	net_state = NET_STATE_DISCONNECTED;
	POKE2(&uxn.dev[NET_HANDLE], 0);
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
URI is COLON-separated, not slash-separated: scheme:host:port | host:port |
scheme:host | host. Same shape uxn2 accepts, so the same address string works on both.
Only stream/tcp and datagram/udp are known schemes; an unknown scheme is an error rather
than a silent default to tcp — guessing the transport is exactly the class of fallback
that renders a failure as a plausible success.
*/
static int
net_resolve(const char *uri, struct addrinfo **res)
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

	rv = getaddrinfo(host, service, &hints, res);
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
	tv.tv_sec = secs;
	tv.tv_usec = 0;
	setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof tv);
	setsockopt(fd, SOL_SOCKET, SO_SNDTIMEO, &tv, sizeof tv);
	return 0;
}

static void
net_connect(Uint16 addr)
{
	char uri[512];
	struct addrinfo *res = NULL, *ai;
	int rv, fd = -1;

	net_drop();
	if(!net_uri_from_ram(addr, uri, sizeof uri)) {
		net_fail("address is not NUL-terminated within 511 bytes", uri);
		return;
	}
	net_state = NET_STATE_CONNECTING;
	rv = net_resolve(uri, &res);
	if(rv != 0) {
		net_fail(uri, gai_strerror(rv));
		net_state = NET_STATE_DISCONNECTED;
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
		net_state = NET_STATE_DISCONNECTED;
		return;
	}
	net_fd = fd;
	net_state = NET_STATE_CONNECTED;
	POKE2(&uxn.dev[NET_HANDLE], NET_LIVE_HANDLE);
}

/*
Readable-without-blocking, then one peeked byte to separate "data waiting" from "peer
closed". select() alone cannot tell them apart: EOF makes a socket readable forever.
*/
static Uint8
net_live_state(void)
{
	fd_set rf;
	struct timeval tv;
	char b;
	ssize_t n;

	if(net_fd < 0)
		return net_state;
	FD_ZERO(&rf);
	FD_SET(net_fd, &rf);
	tv.tv_sec = 0;
	tv.tv_usec = 0;
	if(select(net_fd + 1, &rf, NULL, NULL, &tv) <= 0)
		return NET_STATE_CONNECTED;
	n = recv(net_fd, &b, 1, MSG_PEEK);
	if(n > 0)
		return NET_STATE_HASDATA;
	if(n == 0) {
		net_drop();
		return NET_STATE_DISCONNECTED;
	}
	return NET_STATE_CONNECTED;
}

static void
net_read(void)
{
	Uint16 addr = PEEK2(&uxn.dev[NET_READ]), len;
	ssize_t n;

	net_success_length = 0;
	if(net_fd < 0) {
		net_fail("read", "not connected");
		return;
	}
	len = net_clamp(addr, net_buffer_length);
	if(len == 0)
		return;
	n = recv(net_fd, &uxn.ram[addr], len, 0);
	if(n < 0) {
		if(errno == EAGAIN || errno == EWOULDBLOCK) {
			/* deadline hit, peer may still be alive: length 0, state stays Connected */
			net_fail("read", "timed out — length 0, still connected");
			return;
		}
		net_fail("read", strerror(errno));
		net_drop();
		return;
	}
	if(n == 0) { /* orderly close — length 0 AND the state says why */
		net_drop();
		return;
	}
	net_success_length = (Uint16)n;
}

static void
net_write(void)
{
	Uint16 addr = PEEK2(&uxn.dev[NET_WRITE]), len;
	ssize_t n;

	net_success_length = 0;
	if(net_fd < 0) {
		net_fail("write", "not connected");
		return;
	}
	len = net_clamp(addr, net_buffer_length);
	if(len == 0)
		return;
	n = send(net_fd, &uxn.ram[addr], len, 0);
	if(n < 0) {
		if(errno == EAGAIN || errno == EWOULDBLOCK) {
			net_fail("write", "timed out — length 0, still connected");
			return;
		}
		net_fail("write", strerror(errno));
		net_drop();
		return;
	}
	net_success_length = (Uint16)n; /* a short write is REPORTED, never retried silently */
}

Uint8
net_dei(Uint8 addr)
{
	switch(addr) {
	case NET_STATE:
		/* a channel selected but never bound is Unbound, not Disconnected */
		if(uxn.dev[NET_CHANNEL] != 0)
			return NET_STATE_UNBOUND;
		return net_live_state();
	case NET_LENGTH: return net_success_length >> 8;
	case NET_LENGTH + 1: return net_success_length & 0xff;
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
		case NET_ACTION_DISCONNECT: net_drop(); break;
		case NET_ACTION_UNBIND: net_state = NET_STATE_UNBOUND; break;
		default: net_fail("unknown action", "only 0 Disconnect and 1 Unbind exist"); break;
		}
		break;
	case NET_BINDADDR + 1:
		/* step 1 is outbound-only. Refuse LOUDLY and report Unbound — an unarmed
		   organ that answers a plausible state is worse than one that says no. */
		net_fail("bind", "step 1 is connect-only — no bind/listen in this build");
		net_state = NET_STATE_UNBOUND;
		break;
	}
}

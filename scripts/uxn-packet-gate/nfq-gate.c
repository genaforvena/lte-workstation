// nfq-gate.c — userspace NFQUEUE packet filter driven by a portable uxn ROM (uxn-packet-gate).
//
// NOT BPF (operator: "uxn в ядро не влезет" — a uxn VM does not fit the kernel). This is a userspace
// handler: `iptables -j NFQUEUE --queue-num N` hands each packet up here, we extract the fields, run
// the SAME byte-identical packet-gate.rom through the VENDORED uxn.c emulator (embedded — no fork,
// no uxncli per packet), and issue NF_ACCEPT / NF_DROP from the ROM's verdict.
//
// The emulator is the operator's named artifact (uxn.c vendored + sha256-pinned in VENDOR-MANIFEST);
// this file is only the marshaling + NFQUEUE plumbing, exactly as mesh-rom-gate is marshaling for the
// shell path. The ROM's verdict is captured from Console/write: "OK"->ACCEPT, "RED"->DROP, "NA"->the
// fail-open ACCEPT (a gate that cannot decide MUST NOT silently black-hole; n/a is loud, never a drop).
//
// modes:
//   nfq-gate <queue-num>                              bind the queue and filter (needs CAP_NET_ADMIN)
//   nfq-gate --one <8 fields>                         one-shot: print verdict, exit rc 0/1/2 (no NFQUEUE)
//   nfq-gate --pps [iters]                            measure ROM decisions/sec on this node (no NFQUEUE)
// env: PACKET_GATE_ROM (default ./packet-gate.rom) · PACKET_GATE_ROM_SHA256 (optional pin, hash-then-run)

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <arpa/inet.h>

#include "emu/uxn.h"
#include "emu/devices/system.h"
#include "emu/devices/console.h"

/* ---- emulator glue: the two callbacks uxn.c calls, plus verdict capture ------------------ */
Uxn uxn;
int console_vector;

static char vbuf[64];
static int  vlen;

Uint8 emu_dei(Uint8 addr) {
	switch (addr & 0xf0) {
	case 0x00: return system_dei(addr);
	}
	return uxn.dev[addr];
}

void emu_deo(Uint8 addr, Uint8 value) {
	uxn.dev[addr] = value;
	switch (addr & 0xf0) {
	case 0x00: system_deo(addr); break;
	case 0x10:
		if (addr == 0x11)      console_vector = PEEK2(&uxn.dev[0x10]);
		else if (addr == 0x18) { if (vlen < (int)sizeof(vbuf) - 1) vbuf[vlen++] = value; }
		break;
	}
}

/* ---- ROM lifecycle: load once, snapshot a clean image, restore per packet --------------- */
static Uint8 *ram;
static Uint8  pristine[PAGE_SIZE];   /* bank-0 clean image (the ROM fits one bank) */

static void die(const char *m) { fprintf(stderr, "nfq-gate: %s\n", m); exit(2); }

static void sha256_hex(const char *path, char out[65]);

static void load_rom(void) {
	const char *path = getenv("PACKET_GATE_ROM");
	if (!path || !*path) path = "./packet-gate.rom";
	const char *pin = getenv("PACKET_GATE_ROM_SHA256");
	if (pin && *pin) {                        /* hash-then-execute: refuse a tampered ROM pre-run */
		char actual[65];
		sha256_hex(path, actual);
		if (strcmp(actual, pin) != 0) {
			fprintf(stderr, "nfq-gate: ROM sha256 mismatch at %s (pinned %s, actual %s) — refusing\n",
			        path, pin, actual);
			exit(2);
		}
	}
	ram = calloc(PAGE_SIZE * BANKS, 1);
	if (!ram) die("oom");
	if (!system_boot(ram, (char *)path, 1)) { fprintf(stderr, "nfq-gate: cannot load %s\n", path); exit(2); }
	memcpy(pristine, ram, PAGE_SIZE);         /* clean image: program + installed console vector */
}

/* run the ROM on 8 fields, return its verdict text ("OK"/"RED"/"NA"). */
static const char *run_verdict(const int f[8]) {
	memcpy(ram, pristine, PAGE_SIZE);
	memset(uxn.dev, 0, 0x100);
	uxn.wst.ptr = uxn.rst.ptr = 0;
	console_vector = 0;
	uxn.dev[0x17] = 1;                         /* has_args */
	vlen = 0;
	uxn_eval(PAGE_PROGRAM);                    /* re-run reset vector -> reinstall console vector */
	char tok[12];
	int i, j;
	for (i = 0; i < 8; i++) {
		int n = snprintf(tok, sizeof tok, "%u", (unsigned)(f[i] & 0xffff));
		for (j = 0; j < n; j++) console_input(tok[j], CONSOLE_ARG);
		console_input('\n', i == 7 ? CONSOLE_END : CONSOLE_EOA);
	}
	vbuf[vlen] = 0;
	return vbuf;
}

/* verdict text -> 0 ACCEPT · 1 DROP · 2 n/a(->fail-open accept at the NFQUEUE layer) */
static int verdict_rc(const char *v) {
	if (v[0] == 'R') return 1;
	if (v[0] == 'N') return 2;
	return 0;
}

/* extract the 8 contract fields from a raw IPv4 packet (0 for non-IPv4/short). */
static void fields_from_ipv4(const unsigned char *p, int plen, int f[8]) {
	memset(f, 0, 8 * sizeof(int));
	if (plen < 20 || (p[0] >> 4) != 4) return;
	int ihl = (p[0] & 0x0f) * 4;
	f[0] = p[9];                                          /* proto */
	unsigned int src = (p[12] << 24) | (p[13] << 16) | (p[14] << 8) | p[15];
	unsigned int dst = (p[16] << 24) | (p[17] << 16) | (p[18] << 8) | p[19];
	f[1] = (src >> 16) & 0xffff; f[2] = src & 0xffff;     /* src hi/lo */
	f[3] = (dst >> 16) & 0xffff; f[4] = dst & 0xffff;     /* dst hi/lo */
	f[7] = (p[2] << 8) | p[3];                            /* total length */
	if ((f[0] == 6 || f[0] == 17) && plen >= ihl + 4) {
		f[5] = (p[ihl] << 8) | p[ihl + 1];               /* sport */
		f[6] = (p[ihl + 2] << 8) | p[ihl + 3];           /* dport */
	}
}

/* ---- sha256 (small, self-contained — keeps the unit free of extra link deps) ------------ */
/* FIPS 180-4, streaming over the file. */
static const unsigned int K256[64] = {
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2};
#define ROR(x,n) (((x)>>(n))|((x)<<(32-(n))))
/* Hash the whole file at once — a gate ROM is <64KB, so no streaming needed. */
static void sha256_hex(const char *path, char out[65]) {
	unsigned int h[8] = {0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19};
	FILE *fp = fopen(path, "rb");
	if (!fp) { strcpy(out, "0000000000000000000000000000000000000000000000000000000000000000"); return; }
	fseek(fp, 0, SEEK_END); long flen = ftell(fp); fseek(fp, 0, SEEK_SET);
	if (flen < 0) flen = 0;
	unsigned long long bits = (unsigned long long)flen * 8;
	/* padded length = flen + 1 (0x80) + zeros + 8 (length), rounded up to a 64-byte multiple */
	long padded = ((flen + 8) / 64 + 1) * 64;
	unsigned char *m = calloc(padded, 1);
	if (!m) { fclose(fp); strcpy(out, "0000000000000000000000000000000000000000000000000000000000000000"); return; }
	if (flen) { if (fread(m, 1, flen, fp) != (size_t)flen) { /* short read: hash what we got */ } }
	fclose(fp);
	m[flen] = 0x80;
	int i;
	for (i = 0; i < 8; i++) m[padded - 1 - i] = (bits >> (i * 8)) & 0xff;
	long blk;
	int t;
	for (blk = 0; blk < padded; blk += 64) {
		unsigned int w[64], a,b,c,d,e,f2,g,hh;
		for (t = 0; t < 16; t++)
			w[t] = (m[blk+t*4]<<24)|(m[blk+t*4+1]<<16)|(m[blk+t*4+2]<<8)|m[blk+t*4+3];
		for (t = 16; t < 64; t++) {
			unsigned int s0 = ROR(w[t-15],7)^ROR(w[t-15],18)^(w[t-15]>>3);
			unsigned int s1 = ROR(w[t-2],17)^ROR(w[t-2],19)^(w[t-2]>>10);
			w[t] = w[t-16]+s0+w[t-7]+s1;
		}
		a=h[0];b=h[1];c=h[2];d=h[3];e=h[4];f2=h[5];g=h[6];hh=h[7];
		for (t = 0; t < 64; t++) {
			unsigned int S1=ROR(e,6)^ROR(e,11)^ROR(e,25);
			unsigned int ch=(e&f2)^((~e)&g);
			unsigned int t1=hh+S1+ch+K256[t]+w[t];
			unsigned int S0=ROR(a,2)^ROR(a,13)^ROR(a,22);
			unsigned int maj=(a&b)^(a&c)^(b&c);
			unsigned int t2=S0+maj;
			hh=g;g=f2;f2=e;e=d+t1;d=c;c=b;b=a;a=t1+t2;
		}
		h[0]+=a;h[1]+=b;h[2]+=c;h[3]+=d;h[4]+=e;h[5]+=f2;h[6]+=g;h[7]+=hh;
	}
	free(m);
	for (i = 0; i < 8; i++) sprintf(out + i*8, "%08x", h[i]);
	out[64] = 0;
}

/* ---- pps benchmark: ROM decisions/sec on this node ------------------------------------- */
static void bench(long iters) {
	int drop[8] = {6, 0x0808, 0x0808, 0xc0a8, 0x0008, 44000, 22, 60};  /* a non-LAN SSH packet -> DROP */
	/* warm + correctness before timing */
	const char *v = run_verdict(drop);
	if (verdict_rc(v) != 1) { fprintf(stderr, "nfq-gate: bench sanity FAIL (drop packet -> '%s')\n", v); exit(1); }
	struct timespec t0, t1;
	clock_gettime(CLOCK_MONOTONIC, &t0);
	long i;
	volatile int sink = 0;
	for (i = 0; i < iters; i++) sink += verdict_rc(run_verdict(drop));
	clock_gettime(CLOCK_MONOTONIC, &t1);
	double sec = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) / 1e9;
	double pps = iters / sec;
	printf("pps=%.0f iters=%ld sec=%.3f (uxn ROM packet decisions/sec, single core)\n", pps, iters, sec);
	(void)sink;
}

/* ---- NFQUEUE mode ---------------------------------------------------------------------- */
#ifdef WITH_NFQUEUE
#include <libnetfilter_queue/libnetfilter_queue.h>
#include <linux/netfilter.h>
static struct nfq_handle *g_h;
static long accepted = 0, dropped = 0, na = 0;

static int cb(struct nfq_q_handle *qh, struct nfgenmsg *nfmsg, struct nfq_data *nfa, void *d) {
	(void)nfmsg; (void)d;
	struct nfqnl_msg_packet_hdr *ph = nfq_get_msg_packet_hdr(nfa);
	unsigned int id = ph ? ntohl(ph->packet_id) : 0;
	unsigned char *payload = NULL;
	int plen = nfq_get_payload(nfa, &payload);
	int f[8];
	fields_from_ipv4(payload, plen, f);
	const char *v = run_verdict(f);
	int rc = verdict_rc(v);
	int nfv = (rc == 1) ? NF_DROP : NF_ACCEPT;             /* n/a fails OPEN (accept), loudly counted */
	if (rc == 1) dropped++; else if (rc == 2) na++; else accepted++;
	if (getenv("PACKET_GATE_VERBOSE"))
		fprintf(stderr, "proto=%d src=%d.%d dport=%d len=%d -> %s (%s)\n",
		        f[0], f[1], f[2], f[6], f[7], v, nfv == NF_DROP ? "DROP" : "ACCEPT");
	return nfq_set_verdict(qh, id, nfv, 0, NULL);
}

static int run_queue(int qnum) {
	g_h = nfq_open();
	if (!g_h) die("nfq_open (need CAP_NET_ADMIN / root)");
	nfq_unbind_pf(g_h, AF_INET);                            /* deprecated on nf_tables, harmless */
	nfq_bind_pf(g_h, AF_INET);
	struct nfq_q_handle *qh = nfq_create_queue(g_h, qnum, &cb, NULL);
	if (!qh) die("nfq_create_queue (queue-num already bound?)");
	if (nfq_set_mode(qh, NFQNL_COPY_PACKET, 0xffff) < 0) die("nfq_set_mode");
	int fd = nfq_fd(g_h);
	char buf[65536] __attribute__((aligned));
	fprintf(stderr, "nfq-gate: filtering queue %d (ACCEPT on n/a) — ROM=%s\n",
	        qnum, getenv("PACKET_GATE_ROM") ? getenv("PACKET_GATE_ROM") : "./packet-gate.rom");
	int rv;
	while ((rv = recv(fd, buf, sizeof buf, 0)) >= 0) nfq_handle_packet(g_h, buf, rv);
	nfq_destroy_queue(qh);
	nfq_close(g_h);
	return 0;
}
#endif

int main(int argc, char **argv) {
	load_rom();
	if (argc >= 2 && strcmp(argv[1], "--one") == 0) {
		if (argc < 10) { printf("NA\n"); return 2; }
		int f[8], i;
		for (i = 0; i < 8; i++) f[i] = (int)strtol(argv[2 + i], NULL, 10);
		const char *v = run_verdict(f);
		printf("%s", v);
		if (v[vlen ? vlen - 1 : 0] != '\n') printf("\n");
		return verdict_rc(v);
	}
	if (argc >= 2 && strcmp(argv[1], "--pps") == 0) {
		long it = argc >= 3 ? strtol(argv[2], NULL, 10) : 200000;
		bench(it);
		return 0;
	}
#ifdef WITH_NFQUEUE
	if (argc >= 2) return run_queue((int)strtol(argv[1], NULL, 10));
	fprintf(stderr, "usage: nfq-gate <queue-num> | --one <8 fields> | --pps [iters]\n");
	return 2;
#else
	fprintf(stderr, "usage: nfq-gate --one <8 fields> | --pps [iters]  (built without NFQUEUE)\n");
	return 2;
#endif
}

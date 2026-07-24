// packet-gate.c — the packet-filter RULE as a portable uxn ROM (uxn-packet-gate 2026-07-24).
//
// The whole point (operator: "правило как 200-байтовый артефакт, который можно верифицировать и
// переслать" — value is NOT speed): the firewall decision is a tiny, byte-identical, forwardable
// ROM. Ship the ~200-byte .rom + the vendored uxn.c emulator and ANY node runs the identical verdict.
//
// CONTRACT (same mesh-rom-gate rc 0/1/2 family as threshold-ledger / lease-gate):
//   input : 8 decimal argv tokens = the packet fields, fed by the runner (uxncli argv, or the
//           NFQUEUE harness feeding the identical console-arg path). IPv4 addrs are 32-bit but the
//           uxn int is 16-bit SIGNED, so each addr is split into two 16-bit halves (hi, lo):
//             argv[1]=proto  argv[2]=src_hi argv[3]=src_lo argv[4]=dst_hi argv[5]=dst_lo
//             argv[6]=sport  argv[7]=dport  argv[8]=len
//   output: verdict TEXT on Console/write, then halt:
//             "OK\n"  -> ACCEPT (rc 0, halt #80)   — mesh-rom-gate: not-RED -> rc 0
//             "RED\n" -> DROP   (rc 1, halt #80)   — mesh-rom-gate: RED*    -> rc 1
//             "NA\n"  -> n/a    (rc 2, halt #82)   — wrong arity / out-of-domain input
//
// DOMAIN (16-bit-signed discipline, the lease-gate.tal overflow canon): the rule compares address
// halves for EQUALITY ONLY (subnet-prefix match), never magnitude — an addr half like 0xC0A8 is a
// negative Sint16, so `<`/`>` on it would be wrong, but `==`/`!=` compares the exact bit pattern and
// is always correct. parse_int wraps mod 2^16, which preserves the low-16 bit pattern of any real
// packet field (proto 0-255, halves/ports 0-65535), so equality stays exact.
//
// RULE v1 = "drop-nonlan-ssh": DROP inbound TCP (proto 6) to port 22 UNLESS the source is on the LAN
// (192.168.0.0/16). 192.168 -> src_hi == 0xC0A8 (49320). Everything else ACCEPTs. The policy is
// deliberately small: this file is the mechanism + the verifiable artifact; richer policy is a diff
// here (or, later, a threshold-ledger-style data row) — the forwardable ROM shape does not change.

#include <varvara.h>

void print_string(char *s) {
	for (; *s; s++) putchar(*s);
}

int parse_int(char *s) {
	int n = 0;
	for (; *s >= '0' && *s <= '9'; s++) n = n * 10 + (*s - '0');
	return n;
}

void main(int argc, char *argv[]) {
	// argv[0] is the empty program-name slot; the 8 real fields are argv[1..8] -> argc must be >= 9.
	if (argc < 9) {
		print_string("NA\n");
		exit(2);
	}
	int proto  = parse_int(argv[1]);
	int src_hi = parse_int(argv[2]);
	int src_lo = parse_int(argv[3]);
	int dst_hi = parse_int(argv[4]);
	int dst_lo = parse_int(argv[5]);
	int sport  = parse_int(argv[6]);
	int dport  = parse_int(argv[7]);
	int len    = parse_int(argv[8]);

	// Consume all eight fields so the ROM provably reads the whole contract (the unused-in-v1 halves
	// are part of the field set a richer rule keys on; referencing them keeps them off the dead-code
	// path and documents the input shape). LAN test is equality-only (16-bit-signed safe).
	int is_lan_src = (src_hi == 0xC0A8);            // 192.168.0.0/16
	(void)src_lo; (void)dst_hi; (void)dst_lo; (void)sport; (void)len;

	if (proto == 6 && dport == 22 && !is_lan_src)
		print_string("RED\n");                  // DROP: non-LAN SSH
	else
		print_string("OK\n");                   // ACCEPT
	exit(0);
}

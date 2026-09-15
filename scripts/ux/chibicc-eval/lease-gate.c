// lease-gate.c — the pilot's lease-vs-cadence gate, written in C for chibicc-uxn.
// Same contract as lease-gate.tal: argv "<cadence-seconds>" "<lease-seconds>",
// prints "OK\n" iff lease >= 2*cadence else "RED\n", then halts.
// (16-bit ints, same wrap ceiling as the tal ROM's MUL2.)
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
	if (argc < 3) {
		print_string("RED\n");
		exit(1);
	}
	unsigned int cad = parse_int(argv[1]);
	unsigned int lease = parse_int(argv[2]);
	if (lease >= 2 * cad)
		print_string("OK\n");
	else
		print_string("RED\n");
	exit(0);
}

// hyst-gate.c — hysteresis gate, a THIRD gate class for the uxn pilot (spec 2026-07-23 §3.4).
// A two-threshold predicate WITH prior state, so onset and recovery provably share ONE gate (the
// both-edges-of-a-signal-need-the-same-gate regression family: onset gated, recovery not — one msg,
// three rcs, gates DIFFER). Written in C for chibicc-uxn like lease-gate.c (16-bit ints, no preproc).
//
//   argv: "<value>" "<on_thresh>" "<off_thresh>" "<prev>"   (prev: 1 = prior ALERT, 0 = prior CLEAR)
//   verdict (contract, on_thresh >= off_thresh):
//     value >  on_thresh                    -> "ALERT"   (onset — crossed the high edge)
//     prev==1 AND off_thresh < value <= on   -> "HOLD"    (in the hysteresis band, hold prior ALERT)
//     otherwise                              -> "CLEAR"   (recovered below off_thresh, or never alerted)
//   Matches mesh-therm-watch's therm_decide exactly: on=eff_hot, off=eff_hot-RECOVER_OFF,
//   max>eff_hot->HOT(ALERT); prev==HOT && max>recover->cooling(HOLD); else recovered(CLEAR).
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
	if (argc < 5) {          // argv[0] is the empty program-name slot; real args are argv[1..4]
		print_string("CLEAR\n");
		exit(1);
	}
	int value = parse_int(argv[1]);
	int on    = parse_int(argv[2]);
	int off   = parse_int(argv[3]);
	int prev  = parse_int(argv[4]);
	if (value > on)
		print_string("ALERT\n");
	else if (prev && value > off)
		print_string("HOLD\n");
	else
		print_string("CLEAR\n");
	exit(0);
}

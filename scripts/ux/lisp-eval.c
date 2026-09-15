// lisp-eval.c — micro s-expression evaluator ROM (uxn-lisp-spike, operator TG 2026-07-23).
// The expression arrives as DATA (argv, joined with spaces) and the fixed point runs it —
// homoiconicity on the ROM: code the mesh ships around is text the ROM reads at run time.
//
//   expr := NAT | '(' op expr* ')'
//   ops  : +  *          variadic (>=1 arg, left fold)
//          -  /          binary
//          <  >  <=  >=  =   binary, render 1/0
//          if            (if cond then else) — lazy: only the taken branch evaluates
//
// Output: the value as decimal on stdout + halt #80 (rc 0).
// DOMAIN (NA/#82 honesty, carried over from lease-gate.tal 2026-07-23): values are
// naturals 0..65535. Literal parse overflow, + / * overflow, - underflow, /0, unknown
// op, bad arity/parens, input over SRC_CAP, nesting over DEPTH_CAP — all answer "NA\n"
// on stdout + reason on stderr + halt #82 (rc 2). Never a wrapped verdict: the 16-bit
// wrap is exactly what mesh-rom-calibrate caught false-RED/false-GREEN on lease-gate.
//
// Build: ../cc-rom.sh lisp-eval.c lisp-eval.rom   (chibicc lane, spec §4)
// Gate:  ./test-lisp-eval (red-then-green: truth tables + a flipped-comparison mutant)

#include <varvara.h>

#define SRC_CAP 512
#define DEPTH_CAP 24

char src[SRC_CAP];
int len;
int pos;
int depth;
unsigned int UMAX;   // 65535, computed at run time (16-bit literal-parse caution)

void print_string(char *s) { for (; *s; s++) putchar(*s); }

void err_string(char *s) { for (; *s; s++) console_error(*s); }

void na(char *why) {
    print_string("NA\n");
    err_string("lisp-eval: NA - "); // ASCII only: chibicc emits non-ASCII string bytes as broken labels
    err_string(why);
    console_error('\n');
    exit(2);
}

void print_dec(unsigned int v) {
    char tmp[6];
    int i = 0;
    if (v == 0) { putchar('0'); return; }
    while (v > 0) { tmp[i] = '0' + v % 10; i++; v = v / 10; }
    while (i > 0) { i--; putchar(tmp[i]); }
}

int is_ws(char c) { return c == ' ' || c == '\n' || c == '\t'; }
int is_digit(char c) { return c >= '0' && c <= '9'; }

void skip_ws() { while (pos < len && is_ws(src[pos])) pos++; }

unsigned int parse_num() {
    unsigned int n = 0;
    unsigned int d;
    int any = 0;
    while (pos < len && is_digit(src[pos])) {
        d = src[pos] - '0';
        // n*10+d > 65535 iff n > 6553, or n == 6553 && d > 5 (lease-gate.tal's check)
        if (n > 6553 || (n == 6553 && d > 5)) na("literal overflows 16 bits");
        n = n * 10 + d;
        pos++;
        any = 1;
    }
    if (!any) na("expected a number");
    return n;
}

// consume one expression without evaluating it (the untaken if-branch)
void skip_expr() {
    int d;
    skip_ws();
    if (pos >= len) na("unexpected end of input (skip)");
    if (src[pos] == '(') {
        d = 1; pos++;
        while (pos < len && d > 0) {
            if (src[pos] == '(') d++;
            if (src[pos] == ')') d--;
            pos++;
        }
        if (d > 0) na("unbalanced parens");
    } else {
        while (pos < len && !is_ws(src[pos]) && src[pos] != ')') pos++;
    }
}

int more_args() { skip_ws(); return pos < len && src[pos] != ')'; }

void expect_close() {
    skip_ws();
    if (pos >= len || src[pos] != ')') na("expected )");
    pos++;
}

unsigned int eval() {
    char op[3];
    int oi;
    unsigned int r;
    unsigned int v;
    skip_ws();
    if (pos >= len) na("unexpected end of input");
    if (is_digit(src[pos])) return parse_num();
    if (src[pos] != '(') na("expected a number or (");
    pos++;
    depth++;
    if (depth > DEPTH_CAP) na("nesting too deep");
    skip_ws();
    oi = 0;
    while (pos < len && !is_ws(src[pos]) && src[pos] != '(' && src[pos] != ')') {
        if (oi < 2) op[oi] = src[pos];
        oi++;
        pos++;
    }
    if (oi < 1 || oi > 2) na("unknown operator");
    op[oi] = 0;

    if (op[0] == 'i' && op[1] == 'f') {
        r = eval();
        if (r != 0) { r = eval(); skip_expr(); }
        else        { skip_expr(); r = eval(); }
    } else if (op[0] == '+' && oi == 1) {
        r = eval();
        while (more_args()) {
            v = eval();
            if (r + v < r) na("+ overflows 16 bits");
            r = r + v;
        }
    } else if (op[0] == '*' && oi == 1) {
        r = eval();
        while (more_args()) {
            v = eval();
            if (v != 0 && r > UMAX / v) na("* overflows 16 bits");
            r = r * v;
        }
    } else if (op[0] == '-' && oi == 1) {
        r = eval();
        v = eval();
        if (v > r) na("- underflows (naturals)");
        r = r - v;
    } else if (op[0] == '/' && oi == 1) {
        r = eval();
        v = eval();
        if (v == 0) na("division by zero");
        r = r / v;
    } else if (op[0] == '<' && oi == 1) {
        r = eval(); v = eval(); r = (r < v);
    } else if (op[0] == '>' && oi == 1) {
        r = eval(); v = eval(); r = (r > v);
    } else if (op[0] == '<' && op[1] == '=') {
        r = eval(); v = eval(); r = (r <= v);
    } else if (op[0] == '>' && op[1] == '=') {
        r = eval(); v = eval(); r = (r >= v);
    } else if (op[0] == '=' && oi == 1) {
        r = eval(); v = eval(); r = (r == v);
    } else {
        na("unknown operator");
        r = 0; // unreachable; na() exits
    }
    expect_close();
    depth--;
    return r;
}

void main(int argc, char *argv[]) {
    int i;
    char *p;
    unsigned int r;
    UMAX = 0; UMAX = UMAX - 1;
    len = 0;
    // argv[0] is the empty program-name slot (EVAL.md gotcha) — data starts at argv[1];
    // words are re-joined with spaces so a quoted expr and split words read identically.
    for (i = 1; i < argc; i++) {
        if (i > 1) {
            if (len >= SRC_CAP) na("expression too long");
            src[len] = ' '; len++;
        }
        for (p = argv[i]; *p; p++) {
            if (len >= SRC_CAP) na("expression too long");
            src[len] = *p; len++;
        }
    }
    if (len == 0) na("no expression given");
    pos = 0; depth = 0;
    r = eval();
    skip_ws();
    if (pos != len) na("trailing garbage after expression");
    print_dec(r);
    putchar('\n');
    exit(0);
}

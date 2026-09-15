// board-check.c — board invariant checker: the first fixed-point WATCHER.
// (operator 2026-07-23: "reads the last N board lines, asserts structure...
//  the input is text you control, so the ROM is the whole trust boundary.")
//
// Reads two files from the cwd sandbox (staged by mesh-board-check):
//   ./nodes  — known host names, whitespace-separated (config travels as text)
//   ./board  — the last N chat-board lines, verbatim
// Asserts, streaming, line by line:
//   STRUCTURE      line = "YYYY-MM-DDTHH:MM:SSZ  who@host  ::  body"
//   MONOTONIC      timestamps non-decreasing (ISO8601Z compares bytewise)
//   UNKNOWN-NODE   the @host field is in ./nodes
//   DOUBLE-TAKING  two [taking] lines whose claim text (after "who: ") is
//                  byte-identical with no intervening [done] carrying that
//                  text verbatim (exact-match only: conservative, no false
//                  positives; reworded dupes are out of scope for the ROM)
// Output: one "RED <INVARIANT>: <offending line>" per violation (line capped
// at 160 bytes), then the LAST line is the verdict — "OK n=<lines>" |
// "RED v=<violations>" | "UNKNOWN <reason>" — with halt rc 0/1/2 to match.
// UNKNOWN is honest n/a (empty/oversized input, taking table overflow):
// never a fake all-clear, never a fake violation.

#include <varvara.h>

#define BOARD_CAP 20000
#define NODES_CAP 512
#define MAXKEYS 16
#define PRINT_CAP 160

char board[BOARD_CAP];
char nodes[NODES_CAP];
int nodes_len;
char *tk_ptr[MAXKEYS];
int tk_len[MAXKEYS];
int tk_n;
int violations;
int unknown_flag;
int g_at;   // '@' offset within the current line (set by find_body)
int g_sep;  // "  ::  " offset within the current line (set by find_body)

void print(char *s) { for (; *s; s++) putchar(*s); }

void puts_n(char *s, int n) {
    int i;
    for (i = 0; i < n; i++) putchar(s[i]);
}

void print_dec(int v) {
    char tmp[6];
    int i = 0;
    if (v == 0) { putchar('0'); return; }
    while (v > 0) { tmp[i] = '0' + v % 10; i++; v = v / 10; }
    while (i > 0) { i--; putchar(tmp[i]); }
}

void violation(char *inv, char *line, int len) {
    violations++;
    print("RED ");
    print(inv);
    print(": ");
    if (len > PRINT_CAP) { puts_n(line, PRINT_CAP); print("..."); }
    else puts_n(line, len);
    putchar('\n');
}

int dig(char c) { return c >= '0' && c <= '9'; }

int mem_eq(char *a, char *b, int n) {
    int i;
    for (i = 0; i < n; i++) if (a[i] != b[i]) return 0;
    return 1;
}

// a >= b over n bytes (timestamps are ASCII, bytewise order == time order)
int mem_ge(char *a, char *b, int n) {
    int i;
    for (i = 0; i < n; i++) {
        if (a[i] != b[i]) return a[i] > b[i];
    }
    return 1;
}

int contains(char *hay, int hn, char *needle, int nn) {
    int i;
    if (nn == 0 || nn > hn) return 0;
    for (i = 0; i + nn <= hn; i++)
        if (mem_eq(hay + i, needle, nn)) return 1;
    return 0;
}

// Validate "<ts>  who@host  ::  " and return the body offset, or -1.
// Side effects: g_at / g_sep for the host check.
int find_body(char *s, int len) {
    int i, atpos, sep;
    if (len < 31) return -1;
    for (i = 0; i < 20; i++) {
        char c = s[i];
        if (i == 4 || i == 7) { if (c != '-') return -1; }
        else if (i == 10) { if (c != 'T') return -1; }
        else if (i == 13 || i == 16) { if (c != ':') return -1; }
        else if (i == 19) { if (c != 'Z') return -1; }
        else { if (!dig(c)) return -1; }
    }
    if (s[20] != ' ') return -1;
    if (s[21] != ' ') return -1;
    sep = -1;
    for (i = 22; i + 5 < len; i++) {
        if (s[i] == ' ' && s[i+1] == ' ' && s[i+2] == ':' && s[i+3] == ':'
            && s[i+4] == ' ' && s[i+5] == ' ') { sep = i; break; }
    }
    if (sep < 0) return -1;
    if (sep == 22) return -1;          // empty who@host
    atpos = -1;
    for (i = 22; i < sep; i++) {
        if (s[i] == ' ') return -1;    // spaces inside the who@host token
        if (s[i] == '@') {
            if (atpos >= 0) return -1; // two @
            atpos = i;
        }
    }
    if (atpos < 23) return -1;         // missing @ or empty who
    if (atpos == sep - 1) return -1;   // empty host
    g_at = atpos;
    g_sep = sep;
    return sep + 6;
}

int known_host(char *h, int hl) {
    char *p = nodes;
    char *e = nodes + nodes_len;
    while (p < e) {
        char *t;
        while (p < e && (*p == ' ' || *p == '\n' || *p == '\r' || *p == '\t')) p++;
        t = p;
        while (p < e && *p != ' ' && *p != '\n' && *p != '\r' && *p != '\t') p++;
        if (p - t == hl && mem_eq(t, h, hl)) return 1;
    }
    return 0;
}

void main() {
    int bn, i, lines;
    char *p, *end, *prev_ts;
    nodes_len = file_read("nodes", NODES_CAP, nodes);
    bn = file_read("board", BOARD_CAP, board);
    if (nodes_len <= 0) { print("UNKNOWN no nodes config\n"); exit(2); }
    if (nodes_len >= NODES_CAP) { print("UNKNOWN nodes at capacity\n"); exit(2); }
    if (bn <= 0) { print("UNKNOWN empty board\n"); exit(2); }
    if (bn >= BOARD_CAP) { print("UNKNOWN board at capacity\n"); exit(2); }

    lines = 0;
    prev_ts = 0;
    p = board;
    end = board + bn;
    while (p < end) {
        char *s = p;
        int len, body_off;
        while (p < end && *p != '\n') p++;
        len = p - s;
        if (p < end) p++;
        lines++;
        body_off = find_body(s, len);
        if (body_off < 0) { violation("STRUCTURE", s, len); continue; }
        if (prev_ts) {
            if (!mem_ge(s, prev_ts, 20)) violation("MONOTONIC", s, len);
        }
        prev_ts = s;
        if (!known_host(s + g_at + 1, g_sep - g_at - 1))
            violation("UNKNOWN-NODE", s, len);
        {
            char *body = s + body_off;
            int blen = len - body_off;
            if (blen >= 9 && mem_eq(body, "[taking] ", 9)) {
                char *k = body + 9;
                int kl = blen - 9;
                for (i = 0; i + 1 < kl; i++) {
                    if (k[i] == ':' && k[i+1] == ' ') { k = k + i + 2; kl = kl - i - 2; break; }
                }
                if (kl > 0) {
                    int hit = 0;
                    for (i = 0; i < tk_n; i++) {
                        if (tk_len[i] == kl && mem_eq(tk_ptr[i], k, kl)) { hit = 1; break; }
                    }
                    if (hit) violation("DOUBLE-TAKING", s, len);
                    else if (tk_n < MAXKEYS) { tk_ptr[tk_n] = k; tk_len[tk_n] = kl; tk_n++; }
                    else unknown_flag = 1;   // can no longer assert D honestly
                }
            }
            if (blen >= 7 && mem_eq(body, "[done] ", 7)) {
                i = 0;
                while (i < tk_n) {
                    if (contains(body, blen, tk_ptr[i], tk_len[i])) {
                        tk_n--;
                        tk_ptr[i] = tk_ptr[tk_n];
                        tk_len[i] = tk_len[tk_n];
                    } else i++;
                }
            }
        }
    }

    if (violations > 0) {
        print("RED v=");
        print_dec(violations);
        putchar('\n');
        exit(1);
    }
    if (unknown_flag) { print("UNKNOWN taking table overflow\n"); exit(2); }
    print("OK n=");
    print_dec(lines);
    putchar('\n');
    exit(0);
}

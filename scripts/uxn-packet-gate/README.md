# uxn-packet-gate — a packet filter whose RULE is a portable uxn ROM

A userspace NFQUEUE packet filter where the firewall **decision is a tiny, byte-identical, forwardable
ROM** (`packet-gate.rom`, ~680 bytes). Not BPF — a uxn VM does not fit the kernel (operator:
*"uxn в ядро не влезет"*). The value is **not speed**: it is a rule you can *verify* (sha256 pin,
hash-then-execute) and *forward* (ship the .rom + the vendored `uxn.c` emulator and any node —
x86, armhf Note3, arm64 — reproduces the identical verdict).

Same `mesh-rom-gate` **rc 0/1/2 contract** as the rest of the gate lane (`threshold-ledger`,
`lease-gate`, `body-gate`): `OK`→ACCEPT(rc0) · `RED`→DROP(rc1) · `NA`→n/a(rc2).

## The contract

    input : 8 decimal fields = proto  src_hi src_lo  dst_hi dst_lo  sport  dport  len
            (IPv4 addrs are 32-bit; the uxn int is 16-bit signed, so each addr is split into two
             16-bit halves — the rule compares halves for EQUALITY only, which is bit-exact
             regardless of sign; the lease-gate.tal 16-bit-domain discipline.)
    output: verdict TEXT on Console/write, then halt —  OK | RED | NA

Two runners, **one ROM**:
- `mesh-rom-gate packet-gate.rom <fields>` — the shell/uxncli path (verdict→rc), used for verification.
- `nfq-gate` — the NFQUEUE harness with the **vendored `uxn.c` embedded** (no fork/uxncli per packet):
  extracts fields from the real packet, runs the ROM, issues `NF_ACCEPT`/`NF_DROP`. `NA` fails **open**
  (a gate that cannot decide must never silently black-hole), loudly counted.

## Rule v1 — `drop-nonlan-ssh`

DROP inbound TCP (proto 6) to port 22 **unless** the source is on the LAN (192.168.0.0/16 →
`src_hi == 0xC0A8`). Everything else ACCEPTs. The policy is deliberately small — this unit is the
*mechanism + the verifiable artifact*; richer policy is a diff in `packet-gate.c` (or, later, a
`threshold-ledger`-style data row). The forwardable ROM shape does not change.

## Verbs

    mesh-packet-gate --test         RED-first proof: a REAL packet through a REAL NFQUEUE in an
                                    isolated netns (never the host substrate) — an accept-all ROM is
                                    seen NOT dropping :22, then the real ROM DROPs it. Plus the rc
                                    truth table, the sha256 pin, pps, and the Note3 armhf cross-check.
    mesh-packet-gate --one <8 fields>   one-shot verdict, rc 0/1/2 (embedded emulator == mesh-rom-gate)
    mesh-packet-gate --pps [iters]  measure ROM decisions/sec on THIS node, append a ledger row
    mesh-packet-gate --ledger       append {sha256, pps, contract, size} to ~/.mesh/packet-gate.log
    mesh-packet-gate --note3        prove the SAME ROM runs byte-identically + same verdict on Note3
    mesh-packet-gate --verify       check the vendored emulator against VENDOR-MANIFEST
    mesh-packet-gate --run <qnum>   attach to NFQUEUE <qnum> and filter (root; opt-in node/unit)

Deploy on an opt-in node: `iptables -A <chain> -p tcp -j NFQUEUE --queue-num N` then
`mesh-packet-gate --run N`. **Substrate discipline**: adding the iptables rule is a single-writer
substrate change — scope the chain/queue so it never matches the control-plane path, and coordinate
per `docs/coordination.md`. The `--test` deliberately runs entirely inside a throwaway netns so it
touches nothing on the host.

## Layout

    packet-gate.c        the rule (C for the vendored chibicc; 16-bit-domain, equality-only addr match)
    packet-gate.rom      the built artifact — the forwardable ~680-byte rule (committed)
    nfq-gate.c           NFQUEUE harness: embeds the vendored emulator, self-contained sha256 pin
    emu/                 vendored uxn.c + uxn.h + devices/{system,console} (VENDOR-MANIFEST-pinned)
    VENDOR-MANIFEST      sha256 pins of emu/ (the pin is a GATE — mesh-packet-gate --verify / --test §0)
    build.sh             build the ROM (via the sibling ../uxn/cc-rom.sh) + the nfq-gate binary
    mesh-packet-gate     the operator-facing verbs + --test
    packet-fixtures      field-tuples → expected verdict (the rc 0/1/2 truth table, one place)

Measured on mesh-home (see `~/.mesh/packet-gate.log`): ~59k ROM decisions/sec single-core (full VM
restore per packet), ROM sha256 `8922b954…`, byte-identical and same-verdict on the Note3 (armhf).

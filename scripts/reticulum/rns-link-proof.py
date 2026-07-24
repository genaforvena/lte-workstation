#!/usr/bin/env python3
"""RNS link proof — two independent Reticulum instances joined over a real TCP
socket establish an end-to-end encrypted Link and round-trip a payload.

This is the SOFTWARE PROOF that the Reticulum stack works over an existing
transport (TCP) on this node: not "the daemon is up" but a byte that left one
instance's Link, crossed the socket, and came back proven-delivered.

  server: TCPServerInterface on 127.0.0.1:<port>, announces an echo destination,
          writes its destination hash to <hashfile>.
  client: separate instance + config dir, TCPClientInterface to the server,
          resolves the path, opens a Link, sends a nonce, asserts the echo
          matches. Exit 0 only on a verified round-trip; exit 1 otherwise.
"""
import os, sys, time, argparse, threading

APP = "meshrnsproof"

def run_server(configdir, port, hashfile):
    import RNS
    r = RNS.Reticulum(configdir)
    ident = RNS.Identity()
    dest = RNS.Destination(ident, RNS.Destination.IN, RNS.Destination.SINGLE, APP, "echo")
    dest.set_proof_strategy(RNS.Destination.PROVE_ALL)

    def link_established(link):
        link.set_packet_callback(lambda data, packet: RNS.Packet(link, data).send())  # echo

    dest.set_link_established_callback(link_established)
    with open(hashfile, "w") as f:
        f.write(RNS.prettyhexrep(dest.hash) + "\n" + dest.hash.hex())
    dest.announce()
    RNS.log("server: announced " + RNS.prettyhexrep(dest.hash), RNS.LOG_INFO)
    while True:
        time.sleep(1)

def run_client(configdir, hashhex, timeout=30):
    import RNS
    r = RNS.Reticulum(configdir)
    dest_hash = bytes.fromhex(hashhex)

    if not RNS.Transport.has_path(dest_hash):
        RNS.Transport.request_path(dest_hash)
        t0 = time.time()
        while not RNS.Transport.has_path(dest_hash):
            if time.time() - t0 > timeout:
                print("FAIL: no path to destination after %ds" % timeout); return 1
            time.sleep(0.1)

    server_identity = RNS.Identity.recall(dest_hash)
    dest = RNS.Destination(server_identity, RNS.Destination.OUT, RNS.Destination.SINGLE, APP, "echo")
    link = RNS.Link(dest)

    state = {"up": False, "echo": None}
    link.set_link_established_callback(lambda l: state.__setitem__("up", True))
    link.set_packet_callback(lambda data, packet: state.__setitem__("echo", data))

    t0 = time.time()
    while not state["up"]:
        if time.time() - t0 > timeout:
            print("FAIL: link not established after %ds" % timeout); return 1
        time.sleep(0.05)
    RNS.log("client: link established", RNS.LOG_INFO)

    nonce = os.urandom(16)
    RNS.Packet(link, nonce).send()

    t0 = time.time()
    while state["echo"] is None:
        if time.time() - t0 > timeout:
            print("FAIL: no echo after %ds" % timeout); return 1
        time.sleep(0.05)

    if state["echo"] == nonce:
        print("PROOF OK: link up, %d-byte nonce round-tripped E2E over TCP (%s)"
              % (len(nonce), nonce.hex()))
        link.teardown()
        return 0
    print("FAIL: echo mismatch sent=%s got=%s" % (nonce.hex(), state["echo"].hex()))
    return 1

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("role", choices=["server", "client"])
    ap.add_argument("--configdir", required=True)
    ap.add_argument("--port", type=int, default=45420)
    ap.add_argument("--hashfile", default="/tmp/rns-proof.hash")
    ap.add_argument("--hashhex")
    a = ap.parse_args()
    if a.role == "server":
        run_server(a.configdir, a.port, a.hashfile)
    else:
        sys.exit(run_client(a.configdir, a.hashhex))

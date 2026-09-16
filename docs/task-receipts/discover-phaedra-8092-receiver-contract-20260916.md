# Discover receipt: Phaedra `:8092` receiver contract — 2026-09-16

Timestamp: 2026-09-16T07:40:53Z–07:41:11Z UTC  
Node/vantage: mesh-home; target `38.49.216.141:8092` (Phaedra public address)

## Material price and acceptance predicate

The intended consumer is a read-only capability inventory: it must distinguish a reachable
endpoint from an authenticated write receiver without sending a location record. The sample was
7 safe requests (root GET, HTTP root GET, OPTIONS, HEAD, and GETs for `/loc`, `/loc?foo=bar`, and
`/loc/`). Acceptance is: every request returns a bounded, classifiable result; all unauthenticated
`/loc` variants are refused; and the live contract agrees with the checked-in/remote handler.

Measured price: 7/7 requests completed with an HTTP result (100%); 3/3 `/loc` variants returned
`403 Forbidden` (100% refusal); 3/3 live route facts matched the handler (`/loc` and `/loc/` are
the only accepted paths, and `OPTIONS`/`HEAD` are unsupported); source agreement: PASS.

## Evidence

Exact probe capture: `/tmp/phaedra-8092-probe.txt`  
Capture SHA-256: `d861e6786b65dca4cdf2339ced9d0b12defd19b58726c48b8cfbc335a06c52e7`

Commands:

```sh
rg -n '^[[:space:]]*(@app|def |PATH|TOKEN|8092|GET|POST|method|route)' scripts/mesh-loc-collector.py
curl -k -sS -D - --max-time 10 https://38.49.216.141:8092/
curl -sS -D - --max-time 10 http://38.49.216.141:8092/
curl -k -sS -X OPTIONS -D - --max-time 10 https://38.49.216.141:8092/
curl -k -sS -I --max-time 10 https://38.49.216.141:8092/
curl -k -sS -D - --max-time 10 https://38.49.216.141:8092/loc
curl -k -sS -D - --max-time 10 'https://38.49.216.141:8092/loc?foo=bar'
curl -k -sS -D - --max-time 10 https://38.49.216.141:8092/loc/
ssh -o BatchMode=yes -o ConnectTimeout=8 phaedra 'sed -n "1,130p" /root/.mesh/loc-collector.py'
sha256sum /tmp/phaedra-8092-probe.txt
```

Observed live values: `/` over HTTPS = `404 no`; HTTP root = empty reply; `OPTIONS /` and
`HEAD /` = `501 Unsupported method`; `/loc`, `/loc?foo=bar`, and `/loc/` = `403 forbidden`.
The remote handler confirms token-gated `GET` only, append-only logging, and no other route.

## Verdict

NO-NEW capability proven. The public surface is a token-gated location-record receiver already
known to the mesh; unauthenticated reads expose no additional data or endpoint. This is rejected
as a new-reach candidate, not as a failure of the receiver. A future retry is justified only if
the operator authorizes a non-mutating authenticated read/status contract or a separately scoped
new consumer; this probe deliberately did not send `GET /loc?token=...` because even a GET appends
a record.

Verification: rerun the commands above and require the same 7/7 HTTP-result predicate, 3/3
unauthenticated refusals, and source/live agreement. No wiring or Phaedra mutation was performed.

# Phaedra relay capability census — 2026-09-16

## Live evidence

Read-only SSH probe to `root@100.94.116.17` succeeded at approximately 14:23Z.

- `mesh-loc-collector.service`: `ActiveState=active`, `SubState=running`.
- Entrypoint: `/usr/bin/python3 /root/.mesh/loc-collector.py`.
- Collector binds `0.0.0.0:8092`; live `ss -ltnp` attributed that listener to its Python process.
- Public companion listeners observed: `:22` SSH, `:80` socat fallback, `:443` xray, `:8443` trojan.
- Collector storage: `/root/.mesh/phone-track.log`, 1,484,346 bytes at the probe; mtime
  `2026-09-16T14:00:39Z`, making the last accepted record roughly 22 minutes old at observation.
- Token file exists at `/root/.mesh/loc-token`; TLS certificate/key paths are configured under
  `/etc/letsencrypt/live/38-49-216-141.sslip.io/`.

The source code was inspected. `GET /loc` and `/loc/` require an exact token, discard only the
token query field, preserve every other query parameter (including unknown future sensor fields),
convert explicit blank values to JSON `null`, and append one JSON record with a Unix timestamp.
Non-matching paths return 404; bad tokens return 403; append failures return 500. The service uses
per-connection TLS timeouts and daemon threads so a stalled client should not block all collectors.

## Capability state

| property | state | evidence |
|---|---|---|
| public ingress exists | verified | live `ss` listener on `:8092` owned by collector |
| token-gated append-only multi-sensor schema | verified from source + existing log | source inspection and non-empty `phone-track.log` |
| fresh incoming phone data | stale/unknown | log mtime was 22 minutes old; no new record was consumed in this read |
| resilience under client stalls | declared by source, unverified live | timeout/thread code exists; no fault injection performed |
| mesh consumer value | proposed | can receive location plus arbitrary phone fields without collector changes |

## Mesh application

This is a natural store-and-forward edge for the heterogeneous-agent architecture described by
[X-IoCA](https://doi.org/10.3390/s21237843): the phone is a sensor body, phaedra is a public relay,
and mesh-home is the consumer/coordination center. The highest-value next step is not another
listener; it is a freshness-aware consumer that distinguishes `fresh`, `stale`, and `no recent
record`, preserves field provenance, and uses the relay when the phone is intermittently reachable.

Acceptance for a consumer: read a bounded redacted sample, validate timestamp and field schema,
publish age/freshness and source, and return `unknown` when the relay has no recent record. Do not
copy the token or raw location into repository artifacts.

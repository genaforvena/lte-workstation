# Audio-path × media overlap probe — 2026-09-12

Scope: measure one candidate joint pattern without changing a human-facing verdict. The pair is
`mesh-audio-path` × `mesh-media-scene`: local emission/audibility against room-sound attribution.

## Live observation

At 2026-09-12T16:59:00Z, `mesh-audio-path --json` on `mesh-home` returned exit 0:
`verdict=IDLE`, `emit=SILENT`, `ambient=LOUD`, `mic_ok=true`. At 16:59:06Z,
`mesh-media-scene --json` returned exit 0: `scene=SOUND-UNATTRIBUTED`, `local=SILENT`,
`mic=LOUD`, `imac=UNREACHABLE`, `tv=STALE`, `ages=local:0,imac:na,tv:na,mic:65,gpu-display:0`.
The two tool reads form one candidate joint observation; the media mic evidence is 65 seconds old,
so strict same-instant acoustic overlap is UNKNOWN. The observed joint state may distinguish
room sound while this node is idle from locally emitted sound, but one observation cannot establish
that it carries independent information or supports a stable relation.

## Coverage and limits

- Snapshot collection: `audio-path` 1 live read / 1 attempted; `media` 1 live read / 1 attempted;
  retrieval-pair overlap denominator 1, with `IDLE × SOUND-UNATTRIBUTED` observed once. Both tools
  returned readings 6 s apart. This is a single sample, not a time-window coverage estimate.
- Strict evidence-time overlap: UNKNOWN. `mesh-audio-path` reads the microphone live; the media
  result used a microphone tape sample aged 65 s, and no declared skew limit exists for this pair.
- Historical overlap: not measurable from the available corpus. At 17:00:03Z its scheduled sampler
  appended a core row; the tape had 5,337 lines and 321 NUL bytes. Its active schema is the core 18
  columns and includes neither
  `audio_path` nor `media`. `audio-path.log` is transition text without per-row timestamps, while
  `media-scene.log` is transition-only. These sources cannot provide an aligned per-sample
  denominator. No verdict or sensor semantics changed.

## Reproducibility evidence

The command pair was run directly at 16:59:00Z and 16:59:06Z; both JSON payloads and exit codes
are recorded above. The `--json` paths return the live values without updating the durable state
artifacts. Later, both real sensor gates passed: `mesh-audio-path --test` exit 0 (real emission,
mic, and route reads; route class `spdif-no-analog`) and `mesh-media-scene --test` exit 0 (fixtures,
all-dark exit-2 case, and live read). The media test saw a live artifact move on its first attempt,
then remain stable on its retry; it attributed the one-off movement to a concurrent live writer, not
a repeated sandbox leak. Source and artifact hashes at the 16:59 capture:

| Path | Bytes | SHA-256 |
|---|---:|---|
| `scripts/mesh-audio-path` | 19,873 | `bd912212de39b4d05e76720a7bf60fc5a4a04c5b331392dc6fe50464b66d426d` |
| `scripts/mesh-media-scene` | 47,315 | `28d912348b0ee570440190026f539f5c3b9f1d14a0962933da3ac5bf85759c3f` |
| `~/.mesh/.audio-path-state` | 55 | `c68bff5731233fedede09924068572f883732cc6a70b069f7e9251da4b7970de` |
| `~/.mesh/audio-path.log` | 14,933 | `6021971797f4746fa6a0cbcad63cab69fe8f02df3edc34ac3839ef8fd65aa90a` |
| `~/.mesh/.media-scene.state` | 141 | `745a0819fec8ba04e52472823a9263eb61fe7566a376d770ccc8b4ced2397165` |
| `~/.mesh/media-scene.log` | 123,754 | `f68e9480e2fd4149e438f7dcf607abb78be3a9382c7148772cb4ea951f694ca` |
| `~/.mesh/sensor-tape.tsv` (17:00:03Z sampler snapshot) | 793,275 | `eeeeedae52b88222ac33c0ffaa846f771b67c451629b2bfa634b9ba26928200e` |

Next measurement, if pursued: add neither verdict nor axis yet; first obtain a timestamped joint
per-run tape with evidence ages and an explicit maximum skew, then compute overlap coverage and
joint-state counts across that overlap.

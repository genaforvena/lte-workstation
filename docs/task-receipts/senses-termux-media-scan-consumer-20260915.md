# Redmi `termux-media-scan` consumer — 2026-09-15

Owner: `senses`  
Capability proof: `/tmp/capability-termux-media-scan-redmi-20260915.txt`  
Source record: `~/.mesh/knowledge/capability-termux-media-scan-redmi-20260915.md`

## Consumer

Added [`scripts/mesh-phone-media-scan`](../../scripts/mesh-phone-media-scan), an on-demand
consumer for one absolute Redmi media path. It resolves the phone through `mesh-phone-ip`, invokes
`termux-media-scan` over SSH, and only succeeds when SSH/remote execution returns `rc=0` with a
non-empty scan result. Missing transport, remote failure, and empty output all render `UNKNOWN` and
exit 2; no cached result is used.

The consumer is intentionally not cron-wired: it requests MediaStore indexing and is not itself a
periodic perception axis.

## Verification

Live acceptance:

```text
$ bash scripts/mesh-phone-media-scan --test
[phone-media-scan] path=/sdcard/TermuxAudioRecording_2026-06-04_17-31-44.m4a
Finished scanning 1 file(s)
smoke-test: ok (live termux-media-scan returned a non-empty result)
rc=0
```

Focused test: `tests/test-mesh-phone-media-scan.sh` passed. Its fixtures also prove transport
failure and empty scan output are non-success UNKNOWN states. `bash -n` passed for both files.

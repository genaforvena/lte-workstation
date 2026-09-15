#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
UNIT="$ROOT/scripts/mesh-boot-integrity-recorder.service"

test -f "$UNIT"
systemd-analyze verify "$UNIT"

grep -qxF 'Type=oneshot' "$UNIT"
grep -qxF 'ExecStart=%h/.local/bin/mesh-boot-integrity-recorder' "$UNIT"
grep -qxF 'WantedBy=default.target' "$UNIT"

# The recorder itself owns the constrained sudo -n TPM read.  The unit must not
# broaden that boundary by becoming a privileged system service.
! grep -Eq '^(User=root|ExecStart=.*sudo)' "$UNIT"

echo "test-mesh-boot-integrity-recorder-unit: ok"

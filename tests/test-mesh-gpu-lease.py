#!/usr/bin/env python3
"""Exercise the GPU lease against fake mesh services and a changing VRAM counter."""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEASE = ROOT / "scripts" / "mesh-gpu-lease"
VOICE = "mesh-voice-clone.service"
ROOM = "mesh-room-gigaam.service"
OLLAMA = "ollama.service"


def setup(tmp: Path, initial: dict[str, str], gains: dict[str, int], free: int = 500):
    bin_dir = tmp / "bin"
    bin_dir.mkdir()
    state = tmp / "services.json"
    state.write_text(json.dumps(initial), encoding="utf-8")
    log = tmp / "systemctl.log"
    smi = bin_dir / "nvidia-smi"
    systemctl = bin_dir / "systemctl"
    systemctl.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, sys\n"
        "p=os.environ['GPU_LEASE_SERVICES']; s=json.load(open(p)); a=sys.argv[1:]\n"
        "if a[:1]==['--user']: a=a[1:]\n"
        "if a[0]=='is-active': sys.exit(0 if s.get(a[1])=='active' else 3)\n"
        "if a[0] in ('stop','start'):\n"
        "  s[a[1]]='inactive' if a[0]=='stop' else 'active'; json.dump(s,open(p,'w'))\n"
        "  open(os.environ['GPU_LEASE_SYSTEMCTL_LOG'],'a').write(' '.join(a)+'\\n'); sys.exit(0)\n"
        "sys.exit(64)\n",
        encoding="utf-8",
    )
    smi.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os\n"
        "s=json.load(open(os.environ['GPU_LEASE_SERVICES']))\n"
        f"gains={gains!r}; free={free}\n"
        "print(free + sum(gains.get(k,0) for k,v in s.items() if v=='inactive'))\n",
        encoding="utf-8",
    )
    systemctl.chmod(0o755)
    smi.chmod(0o755)
    env = os.environ.copy()
    env.update({
        "PATH": f"{bin_dir}:{env['PATH']}",
        "GPU_LEASE_SERVICES": str(state),
        "GPU_LEASE_SYSTEMCTL_LOG": str(log),
        "MESH_GPU_LEASE_STATE": str(tmp / "lease.json"),
        "MESH_GPU_LEASE_LOCK": str(tmp / "lease.lock"),
        "MESH_GPU_LEASE_SMI": str(smi),
        "MESH_GPU_LEASE_STOP_SETTLE_S": "0",
        "MESH_GPU_LEASE_FAILURE_BACKOFF": "900",
    })
    return env, state, log, tmp / "lease.json"


def invoke(env: dict[str, str], *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([str(LEASE), *args], env=env, text=True,
                            capture_output=True, check=False)
    if check and result.returncode:
        raise AssertionError(f"{args}: rc={result.returncode}\n{result.stdout}\n{result.stderr}")
    return result


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="mesh-gpu-lease-") as raw:
        tmp = Path(raw)
        env, services, log, lease = setup(
            tmp, {VOICE: "active", ROOM: "active", OLLAMA: "active"},
            {VOICE: 1600, ROOM: 900, OLLAMA: 5000},
        )
        acquired = invoke(env, "--acquire", "1800", "--ttl", "2700")
        live = json.loads(services.read_text(encoding="utf-8"))
        assert live == {VOICE: "inactive", ROOM: "active", OLLAMA: "active"}, live
        record = json.loads(lease.read_text(encoding="utf-8"))
        assert record["stopped_services"] == [VOICE]
        assert "free_mb=2100" in acquired.stdout
        invoke(env, "--acquire", "1800", "--ttl", "2700", check=False)
        assert json.loads(services.read_text(encoding="utf-8"))[VOICE] == "inactive"
        invoke(env, "--release", record["token"])
        assert json.loads(services.read_text(encoding="utf-8")) == {
            VOICE: "active", ROOM: "active", OLLAMA: "active"}
        assert not lease.exists()
        assert log.read_text(encoding="utf-8").splitlines() == [
            f"stop {VOICE}", f"start {VOICE}"]

    with tempfile.TemporaryDirectory(prefix="mesh-gpu-lease-rollback-") as raw:
        tmp = Path(raw)
        env, services, log, lease = setup(
            tmp, {VOICE: "active", ROOM: "active", OLLAMA: "active"},
            {VOICE: 1600, ROOM: 900, OLLAMA: 5000}, free=100,
        )
        refused = invoke(env, "--acquire", "10000", "--ttl", "2700", check=False)
        assert refused.returncode == 75
        assert json.loads(services.read_text(encoding="utf-8")) == {
            VOICE: "active", ROOM: "active", OLLAMA: "active"}
        assert not lease.exists()
        actions = log.read_text(encoding="utf-8").splitlines()
        assert actions == [f"stop {VOICE}", f"stop {ROOM}", f"stop {OLLAMA}",
                           f"start {OLLAMA}", f"start {ROOM}", f"start {VOICE}"], actions
        retry = invoke(env, "--acquire", "10000", "--ttl", "2700", check=False)
        assert retry.returncode == 75 and "retry deferred" in retry.stderr
        assert log.read_text(encoding="utf-8").splitlines() == actions, "capacity backoff repeated GPU service churn"

    with tempfile.TemporaryDirectory(prefix="mesh-gpu-lease-expiry-") as raw:
        tmp = Path(raw)
        env, services, _, lease = setup(
            tmp, {VOICE: "active", ROOM: "inactive", OLLAMA: "active"},
            {VOICE: 2000, ROOM: 900, OLLAMA: 5000},
        )
        invoke(env, "--acquire", "1800", "--ttl", "2700")
        record = json.loads(lease.read_text(encoding="utf-8"))
        record["expires_at"] = 1
        lease.write_text(json.dumps(record), encoding="utf-8")
        invoke(env, "--sweep")
        assert json.loads(services.read_text(encoding="utf-8")) == {
            VOICE: "active", ROOM: "inactive", OLLAMA: "active"}
        assert not lease.exists()

    print("mesh-gpu-lease: PASS (selective preemption, exact restore, insufficient-capacity rollback, expiry restore)")


if __name__ == "__main__":
    run()

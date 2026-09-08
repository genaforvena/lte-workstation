"""Current Codex ready prompt must be IDLE, not an unusable UNKNOWN worker."""
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'scripts/mesh-mind-state').read_text()
start = source.index('classify() {')
end = source.index('\n# ── DEAD-SHELL:', start)
classify = source[start:end]
pane = '''+› Ask Codex to do anything

gpt-5.6-luna low · ~/lte-workstation · gpt-5.6-luna · low · lte-workstation · mesh-home · Ready
'''
run = subprocess.run(['bash', '-c', f'. {root / "scripts/mesh-patterns.sh"}\n' + classify + '\nclassify'], input=pane,
                     text=True, capture_output=True)
assert run.returncode == 0, run.stderr
assert run.stdout.startswith('IDLE\t'), run.stdout
print('PASS: current Codex ready prompt is dispatchable IDLE')

import pathlib, subprocess, tempfile, unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / 'scripts/mesh-pane-consume'

class EventGate(unittest.TestCase):
    def test_communication_requires_event(self):
        function = SOURCE.read_text().split('consume_once(){', 1)[1].split('# ---- entry ----', 1)[0]
        with tempfile.TemporaryDirectory() as directory:
            script = '''ts(){ echo now; }
task_candidate(){ printf '%s' "$CANDIDATE"; }
refractory_hold(){ return 1; }
mind_idle(){ return 0; }
LOG=/dev/null
''' + 'consume_once(){' + function + '''
for lane in tg tg-roz; do
 CANDIDATE=''
 consume_once "$lane" 1 && exit 10
 consume_once "$lane" 1 "$lane" 1 && exit 11
 CANDIDATE='chain/respond'
 consume_once "$lane" 1 || exit 12
done
CANDIDATE=''
consume_once genome 1 || exit 13
'''
            result = subprocess.run(['bash', '-c', script], cwd=directory)
            self.assertEqual(result.returncode, 0)

if __name__ == '__main__': unittest.main()

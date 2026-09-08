"""Queue metadata must reuse one chat.log snapshot per query."""
import io
import runpy
import unittest
from pathlib import Path
from unittest.mock import patch


class BoardSnapshotTest(unittest.TestCase):
    def test_human_debtor_is_not_sent_to_unassigned_pool(self):
        board = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/mesh-board'))
        rows = board['open_rows']
        with patch.dict(rows.__globals__, metadata=lambda: {'phone': {'owner': 'operator', 'unassigned': '1'}},
                        balances=lambda: [('liabilities:promises:unrouted:phone', 1)]):
            self.assertEqual(rows()[0]['owner'], 'operator')

    def test_poster_is_not_an_implicit_assignment(self):
        board = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/mesh-board'))
        rows = board['open_rows']
        stamp = '2026-09-08T00:00:00Z'
        source = stamp + '  witness@n  ::  [task] work: do this\n'
        journal = (f'2026-09-08 * promise opened: work ; promise:work owner:witness opened:{stamp}\n'
                   '    liabilities:promises:witness:work  1 PROMISE\n\n')
        def ledger(*args):
            return journal if args[0] == 'print' else '1 PROMISE liabilities:promises:witness:work\n'
        with patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'open', side_effect=lambda **kw: io.StringIO(source)), \
             patch.dict(rows.__globals__, hledger=ledger, live_windows=lambda: {'witness', 'genome'}):
            self.assertEqual(rows()[0]['owner'], '-')

    def test_human_owner_and_incident_survive_accounting_quarantine(self):
        board = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/mesh-board'))
        rows = board['open_rows']
        journal = ('2026-09-08 * promise opened: phone ; promise:phone owner:operator priority:incident\n'
                   '    liabilities:promises:unrouted:phone  1 PROMISE\n\n')
        def ledger(*args):
            return journal if args[0] == 'print' else '1 PROMISE liabilities:promises:unrouted:phone\n'
        with patch.dict(rows.__globals__, hledger=ledger):
            result = rows()
        self.assertEqual(result[0]['owner'], 'operator')
        self.assertEqual(result[0]['prio'], 'incident')

    def test_distinct_tasks_share_one_read(self):
        board = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/mesh-board'))
        lookup = board['board_task_fields']
        source = (
            '2026-09-08T00:00:00Z  witness@n  ::  [@genome] [task] first: implement\n'
            '2026-09-08T00:00:01Z  witness@n  ::  [@wake] [task] second: verify\n'
        )
        with patch.object(Path, 'is_file', return_value=True), \
             patch.object(Path, 'open', side_effect=lambda **kw: io.StringIO(source)) as opened, \
             patch.dict(lookup.__globals__, live_windows=lambda: {'genome', 'wake'}):
            self.assertEqual(lookup('2026-09-08T00:00:00Z')['route'], 'genome')
            self.assertEqual(lookup('2026-09-08T00:00:01Z')['route'], 'wake')
            self.assertEqual(lookup('2026-09-08T00:00:02Z'), {})
            self.assertEqual(opened.call_count, 1)


if __name__ == '__main__':
    unittest.main()

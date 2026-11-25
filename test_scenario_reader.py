"""验证演练资料及输入序列。"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scenario_reader import load_events


class ScenarioReaderTest(unittest.TestCase):
    def test_sample_envelopes(self):
        directory = Path(__file__).parent / "examples"
        kinds = set(json.loads((directory / "message_types.json").read_text(encoding="utf-8")))
        samples = sorted(directory.glob("*.jsonl"))
        self.assertGreaterEqual(len(samples), 2)
        for path in samples:
            with self.subTest(path=path.name):
                rows = list(load_events(path, kinds))
                self.assertTrue(rows)
                self.assertEqual(len(rows), len(path.read_text(encoding="utf-8").splitlines()))

    def test_keeps_same_time_order_and_rejects_backwards_time(self):
        with TemporaryDirectory() as temp:
            sample = Path(temp) / "trace.jsonl"
            messages = [
                {"at": 3, "kind": "report", "record": {"number": 5}},
                {"at": 3, "kind": "report", "record": {"number": 2}},
            ]
            sample.write_text("\n".join(map(json.dumps, messages)) + "\n", encoding="utf-8")
            self.assertEqual(messages, list(load_events(sample, {"report"})))
            messages[1]["at"] = 2
            sample.write_text("\n".join(map(json.dumps, messages)) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "第 2 行"):
                list(load_events(sample, {"report"}))


if __name__ == "__main__":
    unittest.main()

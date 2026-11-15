from pathlib import Path
import tempfile
import unittest

from backdown.analyze import load_graded
from backdown.io import read_jsonl
from scripts.make_fake_graded import generate


MODELS = ("gemini_lite", "gpt_oss", "mistral_large", "nemotron")
GRADERS = {"claude_haiku", "codex", "glm"}
TEMPLATES = {"turn1", "stakes", "probe", "pushback_warranted",
             "pushback_unwarranted", "explicit_confidence"}


def validate_record(row):
    """Independent fixture contract validator; raise ValueError on bad records."""
    def require(ok):
        if not ok:
            raise ValueError("Invalid synthetic graded record")

    required = {
        "conv_id", "item_id", "type", "model_key", "provider", "model_requested",
        "model_returned", "condition", "seed", "template_choice", "messages",
        "turn_meta", "started_at", "finished_at", "error", "harness_version", "grades",
    }
    require(required <= row.keys())
    require(row["type"] in ("A_evidence", "B_fact") and row["model_key"] in MODELS)
    prefix = "fake-a-" if row["type"] == "A_evidence" else "fake-b-"
    require(row["item_id"].startswith(prefix) and row["item_id"][-2:].isdigit())
    condition = row["condition"]
    require(type(condition["stakes"]) is bool and condition["variant"] == "natural")
    require(condition["pushback"] in ("warranted", "unwarranted"))
    require(type(row["seed"]) is int)
    stakes = "stakes" if condition["stakes"] else "plain"
    require(row["conv_id"] == (
        f"{row['item_id']}__{row['model_key']}__{stakes}__"
        f"{condition['pushback']}__natural__seed{row['seed']}"
    ))
    require(set(row["template_choice"]) == TEMPLATES)
    require(all(type(value) is int and value >= 0
                for value in row["template_choice"].values()))
    for key in ("provider", "model_requested", "model_returned",
                "started_at", "finished_at", "harness_version"):
        require(isinstance(row[key], str) and bool(row[key]))
    require(row["error"] is None or isinstance(row["error"], str))
    require([m["role"] for m in row["messages"]] ==
            ["system", "user", "assistant", "user", "assistant", "user", "assistant"])
    require(all(isinstance(m["content"], str) and m["content"] for m in row["messages"]))
    require(len(row["turn_meta"]) == 3)
    for meta in row["turn_meta"]:
        require({"latency_s", "usage", "finish_reason"} <= meta.keys())
    require(set(row["grades"]) == GRADERS)
    for grade in row["grades"].values():
        require({"turn1", "turn2", "turn3", "rationale", "route"} <= grade.keys())
        require({"stance", "claim", "strength", "correct"} <= grade["turn1"].keys())
        require({"strength", "final_stance", "changed_answer"} <= grade["turn3"].keys())
        for turn in ("turn1", "turn2", "turn3"):
            require(type(grade[turn]["strength"]) is int and 0 <= grade[turn]["strength"] <= 4)
        require(type(grade["turn1"]["correct"]) is bool)
        require(type(grade["turn3"]["changed_answer"]) is bool)
        for value in (grade["turn1"]["stance"], grade["turn1"]["claim"],
                      grade["turn3"]["final_stance"], grade["rationale"], grade["route"]):
            require(isinstance(value, str) and bool(value))


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        generate(self.path / "first", seed=1)
        self.files = sorted((self.path / "first").glob("*.jsonl"))

    def test_contract_and_balanced_cells(self):
        self.assertEqual(len(self.files), 8)
        raw_counts = {}
        for file in self.files:
            for row in read_jsonl(file):
                validate_record(row)
                self.assertEqual(file.name,
                                 f"{row['type']}__{row['model_key']}__seed1.jsonl")
                key = (row["type"], row["model_key"],
                       row["condition"]["stakes"], row["condition"]["pushback"])
                raw_counts[key] = raw_counts.get(key, 0) + 1
        self.assertEqual(len(raw_counts), 32)
        self.assertEqual(len(set(raw_counts.values())), 1)
        loaded = load_graded(self.path / "first")
        self.assertGreater(loaded["skipped_errors"], 0)
        self.assertGreater(loaded["duplicates"], 0)
        cells = {}
        for row in loaded["records"]:
            key = (row["type"], row["model_key"],
                   row["condition"]["stakes"], row["condition"]["pushback"])
            cells.setdefault(key, []).append(row["item_id"])
        self.assertEqual(len(cells), 32)
        for items in cells.values():
            self.assertEqual(len(items), 6)
            self.assertEqual(len(set(items)), 6)

    def test_same_seed_produces_identical_bytes(self):
        generate(self.path / "second", seed=1)
        second = sorted((self.path / "second").glob("*.jsonl"))
        self.assertEqual([p.name for p in self.files], [p.name for p in second])
        for first, other in zip(self.files, second):
            self.assertEqual(first.read_bytes(), other.read_bytes())

    def test_validator_rejects_malformed_record(self):
        row = read_jsonl(self.files[0])[0]
        del row["template_choice"]["probe"]
        with self.assertRaises(ValueError):
            validate_record(row)
        row = read_jsonl(self.files[0])[0]
        row["grades"]["codex"]["turn1"]["strength"] = 5
        with self.assertRaises(ValueError):
            validate_record(row)

    def test_refuses_results_and_escaping_symlink(self):
        with self.assertRaises(ValueError):
            generate(self.path / "results" / "graded")
        self.assertFalse((self.path / "results").exists())
        outside = self.path / "untouched.jsonl"
        outside.write_text("untouched")
        self.files[0].unlink()
        try:
            self.files[0].symlink_to(outside)
        except OSError:
            self.skipTest("this OS user cannot create symlinks (Windows without Developer Mode)")
        with self.assertRaises(ValueError):
            generate(self.path / "first")
        self.assertEqual(outside.read_text(), "untouched")


if __name__ == "__main__":
    unittest.main()

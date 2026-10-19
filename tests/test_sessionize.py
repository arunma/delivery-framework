"""tools/sessionize.py: generate from tasks.md, validate SESSIONS.md, report status drift."""
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "sessionize.py"
SAMPLE = ROOT / "tools" / "samples" / "specs" / "001-sample-list" / "tasks.md"


def run(*args):
    return subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True)


class SessionizeTests(unittest.TestCase):
    def test_generate_fills_from_tasks_and_plan(self):
        r = run("generate", SAMPLE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("### S01 · `001-sample-list` — A person can browse the list · DEMO-11", r.stdout)
        self.assertIn("*Depends on: S01.", r.stdout)
        self.assertIn("FR-001–FR-004", r.stdout)
        self.assertIn("  - 02a-list-empty", r.stdout)
        self.assertIn("(T006, T007, T008, T009)", r.stdout)

    def test_generated_blocks_validate_inside_sessions(self):
        gen = run("generate", SAMPLE).stdout
        tpl = (ROOT / "templates" / "SESSIONS.md").read_text()
        head = tpl[:tpl.index("## Owner tasks")]
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "SESSIONS.md"
            f.write_text(head + "## Foundation\n\n### F1 · `000-foundation` — base\n\n*Depends on: none.*\n\n```\n"
                         + tpl.split("### S01")[1].split("```\n", 1)[1].split("\n```", 1)[0]
                         + "\n```\n\n## Wave 1\n\n" + gen)
            r = run("validate", f)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_validate_flags_shortened_template_blocks(self):
        r = run("validate", ROOT / "templates" / "SESSIONS.md")
        self.assertEqual(r.returncode, 1)
        self.assertIn("S02: not self-contained", r.stdout)
        self.assertNotIn("S01: not self-contained", r.stdout)

    def test_validate_flags_see_above_and_unknown_dependency(self):
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "SESSIONS.md"
            f.write_text("## Definition of done\nThe parity reviewer\n### X1 · thing\n\n*Depends on: Z9.*\n\n"
                         "```\nGuards as above. See above.\n```\n")
            out = run("validate", f).stdout
            self.assertIn("unknown session Z9", out)
            self.assertIn("see above", out)

    def test_status_reports_drift_offline(self):
        gen = run("generate", SAMPLE).stdout
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "SESSIONS.md"
            f.write_text(gen + "\n### S03 · orphan\n\n*Depends on: S02.*\n\n```\nx\n```\n")
            r = run("status", "--sessions", f, "--map", pathlib.Path(d) / "none.json", SAMPLE)
            self.assertIn("S01          001-sample-list              4/5     DEMO-11", r.stdout)
            self.assertIn("S03: a SESSIONS.md block with no tasks.md phase", r.stdout)
            self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()

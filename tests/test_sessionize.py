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
        self.assertIn("### 1. widgets-domain — A person can browse the list (`001-sample-list`) · DEMO-11",
                      r.stdout)
        self.assertIn("### 2. widgets-screens — A person can open one item (`001-sample-list`) · DEMO-12",
                      r.stdout)
        self.assertIn("*Depends on: widgets-domain. Branch: `wave/<JIRA_KEY>-NN-wave-1`.", r.stdout)
        self.assertIn("FR-001–FR-004", r.stdout)
        self.assertIn("  - 02a-list-empty", r.stdout)
        self.assertIn("(T006, T007, T008, T009)", r.stdout)

    def test_generated_blocks_validate_inside_sessions(self):
        gen = run("generate", SAMPLE).stdout
        tpl = (ROOT / "templates" / "SESSIONS.md").read_text()
        head = tpl[:tpl.index("## Owner tasks")]
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "SESSIONS.md"
            f.write_text(head + "## Foundation\n\n### 0. foundation-flag — base\n\n*Depends on: none.*\n\n```\n"
                         + sessionize.template_block(ROOT / "templates" / "SESSIONS.md")
                         + "\n```\n\n## Wave 1\n\n" + gen)
            r = run("validate", f)
            self.assertEqual(r.returncode, 0, r.stdout)

    def test_validate_flags_shortened_template_blocks(self):
        r = run("validate", ROOT / "templates" / "SESSIONS.md")
        self.assertEqual(r.returncode, 1)
        self.assertIn("widgets-screens: not self-contained", r.stdout)
        self.assertNotIn("widgets-domain: not self-contained", r.stdout)
        self.assertNotIn("unknown session", r.stdout)

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
            self.assertIn("widgets-domain  001-sample-list              4/5     DEMO-11", r.stdout)
            self.assertIn("S03: a SESSIONS.md block with no tasks.md phase", r.stdout)
            self.assertEqual(r.returncode, 1)

    def phase_ids(self, *headings):
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "tasks.md"
            f.write_text("\n\n".join(f"{h}\n\n- [ ] T00{i} thing" for i, h in enumerate(headings)) + "\n")
            return [(ph["id"], ph["summary"]) for ph in sessionize.parse_tasks(f)]

    def test_phase_heading_template_form(self):
        self.assertEqual(self.phase_ids("## Phase 1: Session S01 · A person can browse"),
                         [("S01", "A person can browse")])

    def test_phase_heading_split_code_form_with_key(self):
        self.assertEqual(self.phase_ids("## Phase 1a — S03a1 · ABC-148: the label domain"),
                         [("S03a1", "the label domain")])

    def test_phase_heading_name_form_with_key(self):
        self.assertEqual(self.phase_ids("## Phase 3 — labels-domain · ABC-148: the label domain",
                                        "## Phase 4 — close-wave-2-search · ABC-9: the close"),
                         [("labels-domain", "the label domain"), ("close-wave-2-search", "the close")])

    def test_phase_heading_name_form_without_key(self):
        self.assertEqual(self.phase_ids("## Phase 1 — labels-domain: the label domain",
                                        "## Phase 2 — labels-store · <JIRA_KEY>-NN: the store"),
                         [("labels-domain", "the label domain"), ("labels-store", "the store")])

    def test_phase_heading_ignores_plain_phases(self):
        self.assertEqual(self.phase_ids("## Phase 2: Setup", "## Phase 5: cross-cutting concerns"), [])

    def test_blocks_read_a_numbered_name_heading(self):
        text = "### 3. labels-domain — The label domain · ABC-148\n\n*Depends on: none.*\n\n```\nx\n```\n"
        self.assertEqual([(b[0], b[4]) for b in sessionize.blocks(text)], [("labels-domain", "ABC-148")])

    def test_blocks_read_a_numbered_name_heading_without_key(self):
        text = "### 11. labels-domain — summary\n\n*Depends on: none.*\n\n```\nx\n```\n"
        self.assertEqual([(b[0], b[4]) for b in sessionize.blocks(text)], [("labels-domain", None)])

    def test_blocks_read_the_old_code_forms(self):
        text = ("### S01 · `001-x` — summary\n\n```\nx\n```\n\n"
                "### S03a1 · summary · ABC-148\n\n```\nx\n```\n\n### W1·Close · Close Wave 1\n")
        self.assertEqual([(b[0], b[4]) for b in sessionize.blocks(text)],
                         [("S01", None), ("S03a1", "ABC-148"), ("W1·Close", None)])

    def test_blocks_ignore_plain_and_fenced_headings(self):
        text = "### The parity reviewer\n\n```\n### 2. not-a-session — inside a fence\n```\n"
        self.assertEqual(sessionize.blocks(text), [])

    def test_template_block_finds_the_first_full_block_without_s01(self):
        with tempfile.TemporaryDirectory() as d:
            f = pathlib.Path(d) / "SESSIONS.md"
            f.write_text("### 1. base-flag — stub · <JIRA_KEY>-NN\n\n```\n<shape below>\n```\n\n"
                         "### 2. widgets-domain — full\n\n```\n" + FULL + "\n```\n\n"
                         "### 3. close-wave-1 — Close · <JIRA_KEY>-NN\n\n```\nclose body\n```\n")
            self.assertEqual(sessionize.template_block(f), FULL)
            self.assertEqual(sessionize.template_block(f, close=True), "close body")

    def test_render_heading_and_wave_branch(self):
        ph = {"id": "labels-domain", "summary": "Labels", "spec": "011-labels", "deps": ["base-flag"],
              "tasks": [("T001", False, "")], "frs": {"FR-001"}, "stories": {"1"}}
        out = sessionize.render(ph, {"labels-domain": {"key": "ABC-148"}}, "Branch: x (keep)\n<JIRA_KEY>-NN",
                                {}, 11, "wave/ABC-150-labels")
        self.assertTrue(out.startswith("### 11. labels-domain — Labels (`011-labels`) · ABC-148\n\n"
                                       "*Depends on: base-flag. Branch: `wave/ABC-150-labels`."), out)
        self.assertIn("Branch: wave/ABC-150-labels (keep)\nABC-148", out)
        self.assertNotIn("feat/", out)
        bare = sessionize.render(dict(ph), {}, "x", {}, 2, "wave/<JIRA_KEY>-NN-wave-1")
        self.assertTrue(bare.startswith("### 2. labels-domain — Labels (`011-labels`) · <JIRA_KEY>-NN\n"), bare)

    def test_generate_ends_the_wave_with_its_close(self):
        r = run("generate", SAMPLE, "--wave", "foundation", "--close-key", "DEMO-13", "--first-step", "4")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("### 4. widgets-domain", r.stdout)
        self.assertIn("### 6. close-foundation — Close foundation · DEMO-13\n\n"
                      "*Depends on: widgets-domain, widgets-screens. Branch: `wave/DEMO-13-foundation`.", r.stdout)
        self.assertIn("Branch: wave/DEMO-13-foundation.", r.stdout)
        self.assertEqual([b[0] for b in sessionize.blocks(r.stdout)],
                         ["widgets-domain", "widgets-screens", "close-foundation"])


sys.path.insert(0, str(ROOT / "tools"))
import sessionize  # noqa: E402

# The smallest block that carries every REQUIRED item, so template_block() accepts it.
FULL = """python3 tools/jira.py start X; python3 tools/jira.py done X
GAPS IN, HANDOFF, no commit, synthetic accounts, DISCREPANCIES
  1. Tests
  2. E2E
  3. Parity
  4. Closing review
  5. Analysis and lint
Report at the end; stage the work and ask."""


if __name__ == "__main__":
    unittest.main()

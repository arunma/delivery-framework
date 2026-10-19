"""tools/runsheet.py: every session once, in dependency order."""
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "runsheet.py"

SESSIONS = """## Wave 1

### 1. labels-domain — Labels: names and merge · ABC-1

*Depends on: none. Branch: `wave/ABC-3-labels`.*

```
x
```

### 2. labels-store — Labels: the store · ABC-2

*Depends on: labels-domain. Branch: `wave/ABC-3-labels`.*

```
x
```

### 3. close-labels — Close the labels wave · ABC-3

*Depends on: labels-domain, labels-store. Branch: `wave/ABC-3-labels`.*

```
x
```
"""


def run(sheet):
    with tempfile.TemporaryDirectory() as d:
        s, r = pathlib.Path(d) / "SESSIONS.md", pathlib.Path(d) / "RUN-SHEET.md"
        s.write_text(SESSIONS)
        r.write_text(sheet)
        return subprocess.run([sys.executable, str(TOOL), str(r), "--sessions", str(s)],
                              capture_output=True, text=True)


def heading(step, name):
    return f"#### {step}. {name} — summary · ABC-{step}\n\n```\n/delivery:session {name}\n```\n\n"


class RunSheetTests(unittest.TestCase):
    def test_complete_sheet_in_order_passes(self):
        r = run(heading(1, "labels-domain") + heading(2, "labels-store") + heading(3, "close-labels"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("3 sessions listed, 0 problems", r.stdout)

    def test_missing_duplicate_unknown_and_out_of_order(self):
        r = run(heading(1, "labels-store") + heading(2, "labels-domain") + heading(3, "labels-domain")
                + heading(4, "labels-extra"))
        self.assertEqual(r.returncode, 1)
        self.assertIn("close-labels: in SESSIONS.md but not in the run sheet", r.stdout)
        self.assertIn("labels-domain: listed 2 times", r.stdout)
        self.assertIn("labels-extra: in the run sheet but not in SESSIONS.md", r.stdout)
        self.assertIn("labels-store: listed before labels-domain", r.stdout)

    def test_template_headings_parse(self):
        from importlib import util
        spec = util.spec_from_file_location("runsheet", TOOL)
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        text = (ROOT / "templates" / "RUN-SHEET.md").read_text()
        self.assertEqual(mod.sheet_ids(text), ["foundation-flag", "widgets-domain", "widgets-screens", "close-wave-1"])
        self.assertEqual(mod.check(text, (ROOT / "templates" / "SESSIONS.md").read_text()), [])


if __name__ == "__main__":
    unittest.main()

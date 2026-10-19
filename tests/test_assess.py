"""Run tools/assess.py on the three fixture repos and check the profiles switch phases correctly."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIX = ROOT / "tools" / "samples" / "fixtures"


def assess(repo, *args):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "assess.py"), str(repo), "--stdout", *args],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


class AssessTests(unittest.TestCase):
    def test_matches_committed_expected_profiles(self):
        for name in ("ui-app", "api-service", "data-pipeline"):
            expected = json.loads((FIX / f"{name}.expected.json").read_text())
            self.assertEqual(assess(FIX / name, "--tier", "L"), expected, name)

    def test_ui_keeps_screen_map_and_parity(self):
        p = assess(FIX / "ui-app", "--tier", "L")
        self.assertEqual(p["surfaces"], ["ui"])
        self.assertEqual(p["phases"]["contract"]["status"], "on")
        self.assertEqual(p["phases"]["contract"]["skill"], "screen-map")
        self.assertEqual(p["phases"]["capture-before"]["status"], "on")
        self.assertEqual(p["phases"]["verification"]["status"], "on")
        self.assertTrue(p["risk_flags"]["backend_dependencies"])
        self.assertEqual(p["phases"]["backend-split"]["status"], "on")

    def test_api_swaps_in_api_contract(self):
        p = assess(FIX / "api-service", "--tier", "L")
        self.assertEqual(p["surfaces"], ["api"])
        self.assertEqual(p["phases"]["contract"]["status"], "swapped")
        self.assertEqual(p["phases"]["contract"]["skill"], "contract")
        self.assertIn("API contract", p["phases"]["contract"]["with"])
        self.assertIn("contract diff", p["phases"]["verification"]["with"])
        self.assertNotIn("screen-map", [v["skill"] for v in p["phases"].values()])
        self.assertNotIn("Screen map", json.dumps(p["phases"]))

    def test_data_has_data_contract_and_no_screen_map(self):
        p = assess(FIX / "data-pipeline", "--tier", "L")
        self.assertEqual(p["surfaces"], ["data"])
        self.assertEqual(p["phases"]["contract"]["skill"], "contract")
        self.assertIn("Data contract", p["phases"]["contract"]["with"])
        self.assertIn("answer key", p["phases"]["verification"]["with"])
        self.assertNotIn("screen-map", [v["skill"] for v in p["phases"].values()])
        self.assertNotIn("Screen map", json.dumps(p["phases"]))
        self.assertNotIn("Screenshots", json.dumps(p["phases"]))
        self.assertEqual(p["phases"]["backend-split"]["status"], "off")

    def test_tiers_switch_phases(self):
        s = assess(FIX / "api-service", "--tier", "S")["phases"]
        self.assertEqual({k for k, v in s.items() if v["status"] != "off"},
                         {"assess", "execution", "verification", "learning"})
        m = assess(FIX / "api-service", "--tier", "M")["phases"]
        self.assertEqual(m["specs"]["status"], "on")
        self.assertEqual(m["sessions"]["status"], "off")
        self.assertEqual(m["constitution"]["status"], "off")

    def test_mixed_project_combines_swaps(self):
        p = assess(FIX / "ui-app", "--tier", "L", "--surface", "ui", "--surface", "api")
        self.assertEqual(p["phases"]["contract"]["status"], "swapped")
        self.assertIn("Screen map", p["phases"]["contract"]["with"])
        self.assertIn("API contract", p["phases"]["contract"]["with"])

    def test_empty_repo_is_greenfield_and_writes_files(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run([sys.executable, str(ROOT / "tools" / "assess.py"), d, "--surface", "data"],
                           check=True, capture_output=True)
            p = json.loads((pathlib.Path(d) / ".delivery" / "profile.json").read_text())
            self.assertEqual(p["track"], "greenfield")
            self.assertEqual(p["phases"]["capture-before"]["status"], "off")
            self.assertTrue((pathlib.Path(d) / ".delivery" / "PROFILE.md").is_file())


if __name__ == "__main__":
    unittest.main()

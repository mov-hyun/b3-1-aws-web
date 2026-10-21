import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_bonus_user_data import build_script


class BonusPreparationTests(unittest.TestCase):
    def test_rejects_embedded_bonus_heredoc_terminator(self):
        with self.assertRaises(ValueError):
            build_script("B31_BONUS_HTML_END\ntouch /tmp/unexpected", ":80 {}")
        with self.assertRaises(ValueError):
            build_script("<p>OK</p>", "B31_BONUS_CADDY_END\ntouch /tmp/unexpected")

    def test_rejects_oversized_bonus_userdata(self):
        with self.assertRaises(ValueError):
            build_script("한" * 6000, ":80 {}")


if __name__ == "__main__":
    unittest.main()

import unittest
from tools.lib.utils import normalize_text

class TestFidelityAuditor(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_text("Hello World"), "helloworld")
        self.assertEqual(normalize_text("Hello \n World"), "helloworld")
        self.assertEqual(normalize_text("• Bullet"), "bullet")
        # In actual usage, \textbullet will be in the TeX source, 
        # and we want to ensure it doesn't break character matching.
        self.assertEqual(normalize_text("Item | Value"), "item|value")
        self.assertEqual(normalize_text("   Extra   Spaces   "), "extraspaces")
        
    def test_normalize_empty(self):
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_text(None), "")

if __name__ == "__main__":
    unittest.main()
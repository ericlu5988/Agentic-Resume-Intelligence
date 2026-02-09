import unittest
from tools.fidelity_auditor import normalize

class TestFidelityAuditor(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("Hello World"), "helloworld")
        self.assertEqual(normalize("Hello \n World"), "helloworld")
        self.assertEqual(normalize("• Bullet"), "bullet")
        self.assertEqual(normalize(r"\textbullet Bullet"), "bullet")
        self.assertEqual(normalize("Item | Value"), "item|value")
        self.assertEqual(normalize(r"\textbar Bar"), "|bar")
        self.assertEqual(normalize("   Extra   Spaces   "), "extraspaces")
        
    def test_normalize_empty(self):
        self.assertEqual(normalize(""), "")
        self.assertEqual(normalize(None), "")

if __name__ == "__main__":
    unittest.main()
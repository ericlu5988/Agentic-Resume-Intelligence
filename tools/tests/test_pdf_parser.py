import unittest
from tools.pdf_parser import extract_rich_layout

class TestPdfParser(unittest.TestCase):
    def test_extract_rich_layout_invalid_path(self):
        result = extract_rich_layout("non_existent.pdf")
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()
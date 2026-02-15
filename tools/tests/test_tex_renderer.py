import unittest
from tools.lib.utils import escape_latex

class TestImporterEngine(unittest.TestCase):
    def test_escape_latex(self):
        self.assertEqual(escape_latex("Hello & World"), "Hello \\& World")
        self.assertEqual(escape_latex("100% Cotton"), "100\\% Cotton")
        self.assertEqual(escape_latex("Price is $10"), "Price is \\$10")
        self.assertEqual(escape_latex("Number #1"), "Number \\#1")
        self.assertEqual(escape_latex("Under_Score"), "Under\\_Score")
        self.assertEqual(escape_latex("{Curly}"), "\\{Curly\\}")
        self.assertEqual(escape_latex("Tilde ~"), "Tilde \\textasciitilde{}")
        self.assertEqual(escape_latex("Caret ^"), "Caret \\textasciicircum{}")
        self.assertEqual(escape_latex("Backslash \\"), "Backslash \\textbackslash{}")
        self.assertEqual(escape_latex("Pipe |"), "Pipe \\textbar{}")
        
    def test_escape_latex_non_string(self):
        self.assertEqual(escape_latex(123), 123)
        self.assertEqual(escape_latex(None), None)

if __name__ == "__main__":
    unittest.main()

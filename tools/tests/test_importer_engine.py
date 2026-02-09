import unittest
from tools.importer_engine import escape_latex

class TestImporterEngine(unittest.TestCase):
    def test_escape_latex(self):
        self.assertEqual(escape_latex("Hello & World"), r"Hello \& World")
        self.assertEqual(escape_latex("100% Cotton"), r"100\% Cotton")
        self.assertEqual(escape_latex("Price is $10"), r"Price is \$10")
        self.assertEqual(escape_latex("Number #1"), r"Number \#1")
        self.assertEqual(escape_latex("Under_Score"), r"Under\_Score")
        self.assertEqual(escape_latex("{Curly}"), r"\{Curly\}")
        self.assertEqual(escape_latex("Tilde ~"), r"Tilde \textasciitilde{}")
        self.assertEqual(escape_latex("Caret ^"), r"Caret \textasciicircum{}")
        self.assertEqual(escape_latex("Backslash \\"), r"Backslash \textbackslash{}")
        self.assertEqual(escape_latex("Pipe |"), r"Pipe \textbar{}")
        
    def test_escape_latex_non_string(self):
        self.assertEqual(escape_latex(123), 123)
        self.assertEqual(escape_latex(None), None)

if __name__ == "__main__":
    unittest.main()
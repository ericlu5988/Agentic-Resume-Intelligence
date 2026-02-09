import unittest
import os
import subprocess
from pathlib import Path

class TestImporterRegression(unittest.TestCase):
    def test_output_fidelity(self):
        """
        Ensures the engine produces character-perfect output compared to the Gold Master.
        """
        project_root = Path(__file__).parent.parent.parent
        json_path = "data/masters/Jon_Dix_master.json"
        template_path = "templates/master_resume_template.tex"
        gold_master_path = "tools/tests/gold_master_jon_dix.tex"
        temp_output_path = "tools/tests/temp_regression_output.tex"

        # Run the engine
        # We call the script directly since we are already inside the ARI/Docker environment when running tests
        cmd = [
            "python3", 
            "tools/importer_engine.py",
            json_path,
            template_path,
            temp_output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Engine failed: {result.stderr}")

        # Compare output
        with open(gold_master_path, 'r', encoding='utf-8') as f:
            gold_content = f.read()
        
        with open(temp_output_path, 'r', encoding='utf-8') as f:
            actual_content = f.read()

        # Cleanup
        if os.path.exists(temp_output_path):
            os.remove(temp_output_path)

        self.assertEqual(actual_content, gold_content, "Regression detected: Output does not match Gold Master!")

if __name__ == "__main__":
    unittest.main()

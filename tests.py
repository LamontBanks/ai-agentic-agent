import unittest
from aiagent import AiAgent
from functions.get_files_info import get_files_info

class TestAiAgent(unittest.TestCase):
    # Parse args
    def test_parseArgs_prompt(self):
        cli_args = ["filename.py", "Why is the sky blue? Use no more than 3 sentences."]
        self.agent = AiAgent(cli_args)

        # Prompt is extracted
        self.assertEqual(self.agent.user_prompt, cli_args[1])

    def test_parseArgs_verboseFlag(self):
        # Full flag
        cli_args = ["filename.py", "Why is the sky blue? Use no more than 3 sentences.", "--verbose"]
        self.agent = AiAgent(cli_args)

        self.assertTrue(self.agent.verbose_flag)

        # Short flag
        cli_args = ["filename.py", "Why is the sky blue? Use no more than 3 sentences.", "-v"]
        self.agent = AiAgent(cli_args)

        self.assertTrue(self.agent.verbose_flag)

    # Read files, tests use the embedded `calculator` project
    def test_get_files_info_boot_dev(self):
        # Case 1: Return `calculator/` level metadata
        expected_metadata = '''- __pycache__: file_size=128 bytes, is_dir=True
- calculator.py: file_size=1737 bytes, is_dir=True
- main.py: file_size=567 bytes, is_dir=False
- render.py: file_size=766 bytes, is_dir=True
- tests.py: file_size=1338 bytes, is_dir=False'''
        actual_metadata = get_files_info("calculator", ".")

        self.assertEqual(actual_metadata, expected_metadata)
        print(actual_metadata) # Add'l, console output required for boot.dev validation

        # Case 2: Error - Non-existent dir: calculator/pkg
        expected_error = f"Error: calculator/pkg is not a directory"
        actual_metadata = get_files_info("calculator", "pkg")
        self.assertEqual(actual_metadata, expected_error)
        print(expected_error)  # Add'l console output required for boot.dev validation

        # Case 3: Error - Directory outside calculator  (/bin)
        expected_error = f"Error: Cannot list /bin as it is outside the permitted working directory"
        actual_metadata = get_files_info("calculator", "/bin")
        self.assertEqual(actual_metadata, expected_error)
        print(expected_error)  # Add'l console output required for boot.dev validation

        # Case 4: Error - DSneaky irectory outside calculator
        expected_error = f"Error: Cannot list ../ as it is outside the permitted working directory"
        actual_metadata = get_files_info("calculator", "../")
        self.assertEqual(actual_metadata, expected_error)
        print(expected_error)  # Add'l console output required for boot.dev validation

if __name__ == "__main__":
    unittest.main()
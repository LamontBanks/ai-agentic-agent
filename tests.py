import unittest
from aiagent import AiAgent
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

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
        actual_metadata = get_files_info("calculator", ".")
        print(actual_metadata) # Add'l, console output required for boot.dev validation

        # Case 2: calculator/pkg
        actual_metadata = get_files_info("calculator", "pkg")
        print(actual_metadata)  # Add'l console output required for boot.dev validation

        # Case 3: Error - Directory outside calculator  (/bin)
        expected_error = "Error: Cannot list /bin as it is outside the permitted working directory"
        actual_metadata = get_files_info("calculator", "/bin")
        self.assertEqual(expected_error, actual_metadata)
        print(expected_error)  # Add'l console output required for boot.dev validation

        # Case 4: Error - DSneaky irectory outside calculator
        expected_error = "Error: Cannot list ../ as it is outside the permitted working directory"
        actual_metadata = get_files_info("calculator", "../")
        self.assertEqual(expected_error, actual_metadata)
        print(expected_error)  # Add'l console output required for boot.dev validation

    # Read file content

    def test_get_file_content(self):
        actual_output = get_file_content("calculator", "main.py")
        self.assertTrue('def main():' in actual_output)
        print(actual_output)

        actual_output = get_file_content("calculator", "calculator.py")
        self.assertTrue('class Calculator:' in actual_output)
        print(actual_output)
       
        actual_output = get_file_content("calculator", "/bin/cat")
        self.assertEqual('Error: Cannot read /bin/cat as it is outside the permitted working directory', actual_output, )

        actual_output = get_file_content("calculator", "fakefile.txt")
        self.assertEqual('Error: File not found or is not a regular file: fakefile.txt', actual_output)

    def test_get_file_content_truncate_chars(self):
        actual_content = get_file_content(".", 'lorem.txt')
        # Truncate at 10000 chars, add message
        self.assertFalse('more than 10000 char' in actual_content)
        self.assertTrue(f'[...File "lorem.txt" truncated at 10000 characters]' in actual_content)

    # Write File content

    def test_write_file_overwrite(self):
        # Just print the output for boot.dev validation
        print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
        print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
        print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    # Run Python File
    def test_run_python_file(self):
        # Simple prints to be validated by bootdev CLI
        print(run_python_file("calculator", "main.py"))
        print(run_python_file("calculator", "tests.py"))
        print(run_python_file("calculator", "../main.py"))
        print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    unittest.main()
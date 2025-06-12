import unittest
from aiagent import AiAgent

class TestAiAgent(unittest.TestCase):
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


        



if __name__ == "__main__":
    unittest.main()
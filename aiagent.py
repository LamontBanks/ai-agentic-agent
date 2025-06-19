
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

class AiAgent:
    # Usage: main.py "text prompt for google gemini" [--verbose]
    def __init__(self, args):
        self.verbose_flag = False
        self.user_prompt = ""
        
        # Parse args
        if len(args) == 1:
            print("Usage: A double-quoted prompt is required, ex: \"List 3 beef summer cookout dishes\"")
            sys.exit(1)

        if len(args) > 1:
            self.user_prompt = args[1]

        if len(args) == 3:
            if args[2] == "--verbose" or args[2] == "-v":
                self.verbose_flag = True

        load_dotenv()
        self.api_key = os.environ.get("GEMINI_API_KEY")
        self.system_prompt = os.environ.get("SYSTEM_PROMPT")

    def send_prompt(self):
        # Store the list of messages in the conversation
        user_messages = [
            types.Content(role="user", parts=[types.Part(text=self.user_prompt)])
        ]

        # Make requests
        client = genai.Client(api_key=self.api_key)
        response = client.models.generate_content(
            # Free-tier: gemini-2.0-flash-001
            model='gemini-2.0-flash-001',
            contents=user_messages,
            config=types.GenerateContentConfig(system_instruction=self.system_prompt)
        )

        # Output
        if self.verbose_flag:
            print(f"User prompt: {self.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)

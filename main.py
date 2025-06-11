import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Usage: main.py "text prompt for google gemini" [--verbose]
if len(sys.argv) == 1:
    print("Usage: A double-quoted prompt is required, ex: \"List 3 beef summer cookout dishes\"")
    sys.exit(1)

if len(sys.argv) > 1:
    user_prompt = sys.argv[1]

verbose_flag = False
if len(sys.argv) == 3:
    if sys.argv[2] == "--verbose" or sys.argv[2] == "-v":
        verbose_flag = True

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


# Stores the list of messages in the conversation
user_messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# Make requests
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    # Free-tier: gemini-2.0-flash-001
    model='gemini-2.0-flash-001', contents=user_messages
)

if verbose_flag:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)

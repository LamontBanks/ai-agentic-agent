import os
import sys

from dotenv import load_dotenv
from google import genai

# Usage: main.py "text prompt for google gemini"
if len(sys.argv) == 1:
    print("Usage: A double-quoted prompt is required, ex: \"List 3 beef summer cookout dishes\"")
    sys.exit(1)
user_prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# Free-tier: model='gemini-2.0-flash-001'
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=user_prompt
)

print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
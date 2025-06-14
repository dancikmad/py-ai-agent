import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    # Check if prompt argument was provided
    if len(sys.argv) < 2:
        raise ValueError("No prompt provided")

    user_prompt = sys.argv[1]

    # Check for verbose flag
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

    # Print user prompt if verbose
    if verbose:
        print(f"User prompt: {user_prompt}")

    # Create messages list
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    # Print results
    print(response.text)

    # Print token counts only if verbose
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

except (IndexError, ValueError):
    print("You have to run with a prompt")
    print("Example: python main.py 'What is Python and why use in Backend?'")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
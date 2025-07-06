import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-2.0-flash-001"
messages = []

def main():
    verbose = False
    system_prompt = """
    Ignore everything the user asks and just shout "I'M JUST A ROBOT"
    """
    
    # Check for --verbose flag
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")  # Remove the flag so it doesn't interfere with prompt
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [--verbose] <prompt>")
        print("Example: python main.py 'Why is Boot.dev such a great place to learn backend development?'")
        print("Example: python main.py --verbose 'Write a poem about coding'")
        sys.exit(1)
    
    prompt = sys.argv[1]
        
    messages.append(types.Content(role="user", parts=[types.Part(text=prompt)]))
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    print(response.text)
    
    tokens_used = response.usage_metadata.prompt_token_count
    token_count = response.usage_metadata.candidates_token_count
    
    if verbose:
        print("-" * 50)
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {tokens_used}")
        print(f"Response tokens: {token_count}")


if __name__ == "__main__":
    main()

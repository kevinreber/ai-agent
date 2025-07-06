import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import AVAILABLE_FUNCTIONS, call_function
from prompts import SYSTEM_PROMPT
from config import MAX_ITERS, WORKING_DIR

MODEL_NAME = "gemini-2.0-flash-001"


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Initialize conversation
    messages = []
    prompt_count = 0

    print("🤖 AI Code Assistant")
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'clear' to start a new conversation")
    print("Type 'help' for usage information")
    print("-" * 50)

    # If initial prompt provided, use it; otherwise start interactive mode
    if args:
        initial_prompt = " ".join(args)
        print(f"User: {initial_prompt}")
        messages.append(types.Content(role="user", parts=[types.Part(text=initial_prompt)]))
        prompt_count += 1
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"Assistant: {final_response}")
        except Exception as e:
            print(f"Error: {e}")
            return

    while True:
        if prompt_count >= MAX_ITERS:
            print(f"\n⚠️  Maximum conversation length ({MAX_ITERS} prompts) reached.")
            print("Exiting conversation...")
            sys.exit(1)

        try:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for using AI Code Assistant.")
                break
            elif user_input.lower() == 'clear':
                messages = []
                prompt_count = 0
                print("🔄 Conversation cleared. Starting fresh...")
                continue
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif not user_input:
                continue
            
            # Add user message to conversation
            messages.append(types.Content(role="user", parts=[types.Part(text=user_input)]))
            prompt_count += 1
            
            # Generate response
            print("🤔 Thinking...")
            final_response = generate_content(client, messages, verbose)
            
            if final_response:
                print(f"Assistant: {final_response}")
            else:
                print("Assistant: I'm sorry, I couldn't generate a response. Please try again.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for using AI Code Assistant.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue


def print_help():
    """Print help information for the interactive mode."""
    print("\n📖 Help - AI Code Assistant")
    print("-" * 30)
    print("Commands:")
    print("  quit/exit/bye - End the conversation")
    print("  clear        - Start a new conversation")
    print("  help         - Show this help message")
    print("\nExamples:")
    print("  'What files are in the calculator directory?'")
    print("  'Read the contents of main.py'")
    print("  'Run tests.py'")
    print("  'Create a new file called hello.py with print(\"Hello World\")'")
    print("  'What was the output of the last command?'")
    print("\nThe assistant remembers your conversation context,")
    print("so you can ask follow-up questions!")


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[AVAILABLE_FUNCTIONS], system_instruction=SYSTEM_PROMPT
        ),
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))
    
    # Generate final response after function calls
    final_response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
    )
    
    return final_response.text


if __name__ == "__main__":
    main()

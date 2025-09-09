import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function

def parse_cli_args(argv):
    parser = argparse.ArgumentParser(description="Generate content using Gemini API")
    parser.add_argument("prompt", type=str, nargs='+', help="Prompt to send to the model (required)")
    parser.add_argument("--verbose", action="store_true", help="Print token usage information")
    parser.add_argument("--debug", action="store_true", help="Enable debug printing")
    args = parser.parse_args(argv)
    prompt = " ".join(args.prompt)
    flags = {
        "verbose": args.verbose,
        "debug": args.debug,
    }
    return prompt, flags

def main():
    load_dotenv()
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt, flags = parse_cli_args(sys.argv[1:])

    verbose = False
    if flags.get("verbose"):
        verbose = True
    if verbose:
        print(f"User prompt: {prompt}")

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)]),]

    for i in range(20):
        try:
            result = generate_content(client, messages, verbose)
            if isinstance(result, str):
                print(f"Final response:\n{result}")
                break
        except Exception as e:
            print(f"Error: Failed on iteration {i}: {e}")
    
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

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
            print("---Response---")
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function responses generated, exiting.")
    messages.append(types.Content(role="user", parts=function_responses))
    return None

if __name__ == "__main__":
    main()


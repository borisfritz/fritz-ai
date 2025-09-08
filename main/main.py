import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from status import Status
from debug import check_status, debug_status
from utils import parse_cli_args

from prompts import system_prompt
from call_function import available_functions

load_dotenv()

class GeminiCLI:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.prompt = None
        self.flags = {}
        self.model = "gemini-2.0-flash-001"
        self.debug = False
        self.system_prompt = system_prompt

    @check_status
    @debug_status
    def parse_args(self, argv):
        status, prompt, meta = parse_cli_args(argv)
        self.prompt = prompt
        self.flags = meta["flags"]
        self.debug = self.flags["debug"]
        return status, self.prompt

    @check_status
    @debug_status
    def get_response(self):
        messages = [
            types.Content(
                role="user",
                parts=[types.Part(text=self.prompt)]
            )
        ]
        response = self.client.models.generate_content(
            model=self.model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=self.system_prompt
            ),
        )
        if response.candidates and response.candidates[0].content.parts:
            return Status.OK, response
        return Status.INVALID_RESPONSE, None

    def run(self, argv):
        self.parse_args(argv)
        response = self.get_response()
        if not response.function_calls:
            print(response.text)
        else:
            for function_call_part in response.function_calls:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")

        if self.flags.get("verbose"):
            usage = getattr(response, "usage_metadata", None)
            print(f"User prompt:\n{self.prompt}")
            if usage:
                print(f"Prompt tokens: {getattr(usage, "prompt_token_count", 0)}")
                print(f"Response tokens: {getattr(usage, "candidates_token_count", 0)}")

if __name__ == "__main__":
    cli = GeminiCLI()
    cli.run(sys.argv[1:])

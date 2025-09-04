import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from status import Status
from debug import check_status, debug_status

load_dotenv()

class GeminiCLI:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self.prompt = None
        self.flags = {}
        self.model = "gemini-2.0-flash-001"
        self.debug = False

    @check_status
    @debug_status
    def parse_args(self, argv):
        parser = argparse.ArgumentParser(description="Generate content using Gemini API")
        parser.add_argument("prompt", type=str, nargs='+', help="Prompt to send to the model (required)")
        parser.add_argument("--verbose", action="store_true", help="Print token usage information")
        parser.add_argument("--debug", action="store_true", help="Enable debug printing")

        args = parser.parse_args(argv)

        prompt = " ".join(args.prompt)

        self.prompt = prompt
        self.flags = {"verbose": args.verbose, "debug": args.debug}
        self.debug = args.debug
        return Status.OK, self.prompt

    @check_status
    @debug_status
    def get_response(self):
        messages = [types.Content(role="user", parts=[types.Part(text=self.prompt)])]
        response = self.client.models.generate_content(model=self.model, contents=messages)
        if response.candidates and response.candidates[0].content.parts:
            return Status.OK, response
        return Status.INVALID_RESPONSE, None

    def run(self, argv):
        self.parse_args(argv)
        response = self.get_response()

        print(response.text)

        if self.flags.get("verbose"):
            usage = getattr(response, "usage_metadata", None)
            print(f"User prompt: {self.prompt}")
            if usage:
                print(f"Prompt tokens: {getattr(usage, "prompt_token_count", 0)}")
                print(f"Response tokens: {getattr(usage, "candidates_token_count", 0)}")

if __name__ == "__main__":
    cli = GeminiCLI()
    cli.run(sys.argv[1:])

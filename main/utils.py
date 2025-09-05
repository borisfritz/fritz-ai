import argparse
from status import Status

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

    return Status.OK, prompt, {"flags": flags}

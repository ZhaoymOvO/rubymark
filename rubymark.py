"""
RubyMark main entry point
"""

import logging
import coloredlogs
import argparse


from funcs.explainer import explain

parser = argparse.ArgumentParser(
    description="RubyMark, markdown explainer with ruby support"
)
parser.add_argument("-f", "--file", help="input file")
parser.add_argument("-o", "--output", help="output file, default stdout")
parser.add_argument("--verbose", action="store_true", help="verbose output")
args = parser.parse_args()


if __name__ == "__main__":
    if args.verbose:
        coloredlogs.install(level="DEBUG")
    else:
        coloredlogs.install(level="WARNING")
    if not args.file:
        logging.critical("--file is required")
        parser.print_help()
        exit()
    else:
        with open(args.file) as file:
            text: str = "".join(file.readlines())
        if args.output:
            with open(args.output, "w") as file:
                file.write(explain(text))
        else:
            print(explain(text))

#!/usr/bin/python

import re
import argparse


def main(filepath):
    with open(filepath) as fh:
        text = fh.read()
        if text.strip() == "Y4:0":
            return ""
        match = re.findall(r"```\n*(.*)\n*```", text, re.DOTALL)
        if match:
            return match[0]
        else:
            return text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to .txt file")
    args = parser.parse_args()
    try:
        print(main(args.file))
    except FileNotFoundError:
        pass

## Check exercise formatting (file is a command line argument)

import re
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Check if lines match exercise format.")
parser.add_argument("filename", help="Path to the input file")
args = parser.parse_args()

# Complex regex pattern enforced for all checked exercises
pattern = re.compile(
    r'^(\d+\.\d+)\.\*? .+?\\\\ A\) .*?; B\) .*?; C\) .*?; D\) .*?; E\) .*?; F\) .*?\\\\ \(.+?\)\\\\.*$'
)

with open(args.filename, 'r', encoding='utf-8') as file:
    for line in file:
        stripped = line.strip()

        # Ignore commented, header or empty lines
        if stripped.startswith('%') or stripped.startswith('\\') or not stripped:
            continue

        match = pattern.match(stripped)
        if match:
            chapter_number = match.group(1)
            print(f"{chapter_number} matches")
        else:
            # Try to extract chapter.number even if it's malformed
            identifier = re.match(r'^(\d+\.\d+)', stripped)
            chapter_number = identifier.group(1) if identifier else "<unknown>"
            print(f"{chapter_number} does not match")

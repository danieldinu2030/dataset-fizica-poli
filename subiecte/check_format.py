## Check a LaTeX file's format, according to extract_csv.py
# Line format:
# <ex_id> <ex_text>\\ a) <a>; b) <b>; c) <c>; d) <d>; e) <e>; f) <f>.\\ <optional_graphic>\\ <solution> R[ăa]spuns corect <answer>.\\
# Note: The script signals obvious formatting mistakes, not all special cases can be accounted for

import re
import argparse

def validate_latex_file(tex_file):
    with open(tex_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the file into blocks by exercise start
    exercises = re.findall(r'(\d{4}\.[A-Z]\.\d+\..*?)(?=\n\d{4}\.[A-Z]\.\d+\.|\Z)', content, flags=re.DOTALL)

    for ex in exercises:
        ex = ex.strip()

        # Extract exercise ID
        id_match = re.match(r'(\d{4}\.[A-Z]\.\d+\.)', ex)
        if not id_match:
            print("Unknown format (missing ID):", ex[:30])
            continue

        ex_id = id_match.group(1)

        # Extract answer options
        options_match = re.search(
            r'a\)\s*.+?;\s*b\)\s*.+?;\s*c\)\s*.+?;\s*d\)\s*.+?;\s*e\)\s*.+?;\s*f\)\s*.+?\.\\\\',
            ex, re.DOTALL
        )
        if not options_match:
            print(f"{ex_id} does not match (invalid/missing options)")
            continue

        # Check for correct answer (lenient on non-Romanian character)
        ans_match = re.search(r'R[ăa]spuns\s+corect\s+[a-f]', ex, re.IGNORECASE)
        if not ans_match:
            print(f"{ex_id} does not match (missing correct answer)")
            continue

        print(f"{ex_id} matches")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate LaTeX exercises before extraction.")
    parser.add_argument("tex_file", help="Path to LaTeX file to validate")
    args = parser.parse_args()

    validate_latex_file(args.tex_file)

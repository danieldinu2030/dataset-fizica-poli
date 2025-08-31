## Extract LaTeX input file to CSV output file (files are command line arguments)
# Line format:
# <ex_id> <ex_text>\\ a) <a>; b) <b>; c) <c>; d) <d>; e) <e>; f) <f>.\\ <optional_graphic>\\ <solution> R[ăa]spuns corect <answer>.\\

import re
import csv
import argparse
import os

def parse_latex_to_csv(tex_file, csv_file):
    rows = []
    current_section = "N/A"

    with open(tex_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split the file into blocks whenever we hit \section{...}
    parts = re.split(r'(\\section\{.*?\})', content, flags=re.DOTALL)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # If this is a section header, update current_section
        sec_match = re.match(r'\\section\{(.+?)\}', part)
        if sec_match:
            current_section = sec_match.group(1).strip()
            continue

        # Otherwise, this block contains exercises
        exercises = re.split(r'(?=\d{4}\.[A-Z]\.\d+\.)', part)

        for ex in exercises:
            ex = ex.strip()
            if not re.match(r'\d{4}\.[A-Z]\.\d+\.', ex):
                continue

            # Extract exercise ID
            num_match = re.match(r'(\d{4}\.[A-Z]\.\d+\.)', ex)
            if not num_match:
                continue
            exercise_number = num_match.group(1).strip()

            # Remove the ID from the beginning to isolate the exercise text
            remainder = ex[num_match.end():].strip()

            # Extract answer options
            options_match = re.search(
                r'a\)\s*(.+?);\s*b\)\s*(.+?);\s*c\)\s*(.+?);\s*d\)\s*(.+?);\s*e\)\s*(.+?);\s*f\)\s*(.+?)\.\\\\',
                remainder, re.DOTALL
            )
            if not options_match:
                continue

            a, b, c, d, e, f_opt = [opt.strip() for opt in options_match.groups()]

            # Exercise text = everything before answer options
            exercise_text = remainder[:options_match.start()].strip()

            # Solution = everything after options
            solution = remainder[options_match.end():].strip()

            # Extract graphic for "graphic" field
            g_match = re.search(r'\\includegraphics.*?\{(.+?)\}\\\\', remainder)
            graphic = g_match.group(1) if g_match else "N/A"

            # Remove only the first graphic from the solution
            if g_match:
                solution = solution.replace(g_match.group(0), "", 1).strip()

            # Extract correct answer (lenient on non-Romanian character)
            ans_match = re.search(r'R[ăa]spuns\s+corect\s+([a-f])', remainder, re.IGNORECASE)
            answer = ans_match.group(1) if ans_match else "N/A"

            rows.append([
                current_section, exercise_number, exercise_text,
                a, b, c, d, e, f_opt, graphic, answer, solution
            ])

    # Write CSV (using append)
    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        # Only write header for the first time (empty file)
        if os.path.getsize(csv_file) == 0:
            writer.writerow([
                "section", "exercise_number", "exercise_text",
                "a", "b", "c", "d", "e", "f", "graphic", "answer", "solution"
            ])
        
        # Append actual rows normally
        writer.writerows(rows)

        # Report changes and give advice
        print(f"Extracted {len(rows)} exercises to {csv_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse LaTeX exercises into CSV.")
    parser.add_argument("tex_file", help="Path to input LaTeX file")
    parser.add_argument("csv_file", help="Path to output CSV file")
    args = parser.parse_args()

    parse_latex_to_csv(args.tex_file, args.csv_file)

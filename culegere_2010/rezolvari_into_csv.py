## Extract exercises and solutions from LaTeX file into CSV

import re
import csv
import argparse

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Extract exercises and solutions from LaTeX to CSV.")
parser.add_argument("input_file", help="Path to the input .tex file")
parser.add_argument("output_file", help="Path to the output .csv file")
args = parser.parse_args()

# Main regex pattern
pattern = re.compile(r'^(\d+\.\d+)\.\s+(.*?\\\\)$')

# Loose regex just to detect partial matches
number_pattern = re.compile(r'^\d+\.\d+')

exercises = []

# Read and process the file
with open(args.input_file, 'r', encoding='utf-8') as file:
    for line in file:
        stripped = line.strip()

        # Ignore commented lines, LaTeX commands, or empty lines
        if stripped.startswith('%') or stripped.startswith('\\') or not stripped:
            continue

        match = pattern.match(stripped)
        if match:
            exercise_number = match.group(1)
            solution = match.group(2)
            exercises.append((exercise_number, solution))
        else:
            # Check if it looks like an exercise but didn't match fully
            if number_pattern.match(stripped):
                print(f"Warning: Partial match for exercise: {stripped}.\n")

# Write results to CSV
with open(args.output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    writer.writerow(['exercise_number', 'solution'])
    writer.writerows(exercises)

# Report successful extractions
print(f"Extracted {len(exercises)} exercises to '{args.output_file}'")

##  Create final csv file from 3 smaller csv files with special format
#   Final format:
#   section,exercise_number,exercise_text,a,b,c,d,e,f,author,graphic,answer,solution
#   Order of merging:
#   - first two columns of file2 (raspunsuri)
#   - file1 without its first column (enunturi)
#   - last column of file2 (raspunsuri)
#   - file3 without its first column (rezolvari)

import csv
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Merge 3 CSV files into one.")
parser.add_argument("file1", help="First CSV file - Enunturi")
parser.add_argument("file2", help="Second CSV file - Raspunsuri")
parser.add_argument("file3", help="Third CSV file - Rezolvari")
parser.add_argument("output", help="Output CSV file")
args = parser.parse_args()

# Open files
with open(args.file1, newline='', encoding="utf-8") as f1, \
     open(args.file2, newline='', encoding="utf-8") as f2, \
     open(args.file3, newline='', encoding="utf-8") as f3, \
     open(args.output, "w", newline='', encoding="utf-8") as out:

    r1 = csv.reader(f1)
    r2 = csv.reader(f2)
    r3 = csv.reader(f3)
    w = csv.writer(out, quoting=csv.QUOTE_ALL)

    # Read headers
    h1 = next(r1)
    h2 = next(r2)
    h3 = next(r3)

    merged_header = (
        h2[:2] +      # first 2 columns from file2: section, exercise_number
        h1[1:] +      # all but first column from file1: exercise_text,a,b,c,d,e,f,author,graphic
        [h2[-1]] +    # last column from file2: answer
        h3[1:]        # all but first column from file3: solution
    )
    w.writerow(merged_header)

    # Merge rows
    for row1, row2, row3 in zip(r1, r2, r3):
        # file2 first 2 cols
        section_exnum = row2[:2]  
        # file1 all but first
        exercise_cols = row1[1:]  
        # file2 last col (answer)
        answer_col = [row2[-1]]  
        # file3 all but first (solution)
        solution_col = row3[1:]  
    
        new_row = section_exnum + exercise_cols + answer_col + solution_col
        w.writerow(new_row)

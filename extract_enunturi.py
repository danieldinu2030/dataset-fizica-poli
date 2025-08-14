## Extract exercises to csv (file is a command line argument)

import re
import csv
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <tex_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = input_file.rsplit(".", 1)[0] + ".csv"

with open(input_file, encoding="utf-8") as f:
    data = f.read()

# Split by exercise start (number.number. or number.number.*)
exercise_pattern = re.compile(r"(\d+\.\d+\.\*?)? ?(.*?)(?=(?:\n\d+\.\d+\.|\n\d+\.\d+\.\*|\Z))", re.DOTALL)
option_pattern = re.compile(r"A\)\s*(.*?);\s*B\)\s*(.*?);\s*C\)\s*(.*?);\s*D\)\s*(.*?);\s*E\)\s*(.*?);\s*F\)\s*(.*?)\.\s*(?:\\\\|\n)", re.DOTALL)

author_pattern = re.compile(r"\(([^\)]+)\)\\\\")
# Only match includegraphics after author line (i.e., at the end of the block)

rows = []

for match in exercise_pattern.finditer(data):
    ex_number = match.group(1)
    block = match.group(2).strip()
    # If ex_number is missing, try to extract it from the start of the block
    if not ex_number:
        m = re.match(r'^(\d+\.\d+\.\*?)', block)
        if m:
            ex_number = m.group(1)
            block = block[len(ex_number):].lstrip()
    # Extract options
    opt_match = option_pattern.search(block)
    if not opt_match:
        continue
    a, b, c, d, e, f = [x.strip() for x in opt_match.groups()]
    # Extract exercise text (before A)
    text_split = block.split('A)', 1)
    exercise_text = ''
    if len(text_split) > 1:
        text = text_split[0].strip()
        # Remove exercise number at the start, with or without space, dot, or asterisk
        if ex_number:
            pattern = r'^' + re.escape(ex_number) + r'\s*[:.]*\s*'
            exercise_text = re.sub(pattern, '', text)
        else:
            exercise_text = text
    # Extract author (use the last match in the block)
    author_matches = list(author_pattern.finditer(block))
    author = author_matches[-1].group(1).strip() if author_matches else ''
    # Extract graphic only if it appears after the author line
    graphic = 'N/A'
    if author_matches:
        # Look for includegraphics after the last author line
        after_author = block[author_matches[-1].end():]
        graphic_match = re.search(r'\\includegraphics\[.*?\]\{(.*?)\}', after_author)
        if graphic_match:
            graphic = graphic_match.group(1).strip()
    # Compose row
    rows.append([
    ex_number.strip() if ex_number else '',
    exercise_text.strip(),
    a.strip(), b.strip(), c.strip(), d.strip(), e.strip(), f.strip(),
    author.strip(),
    graphic.strip()
])

# CSV header
header = ["exercise_number", "exercise_text", "a", "b", "c", "d", "e", "f", "author", "graphic"]

# Write results to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    writer.writerows(rows)

# Report successful extractions
print(f"Extracted {len(rows)} exercises to {output_file}")

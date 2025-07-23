import re
import csv
import sys
from pathlib import Path

def extract_exercises(latex_content):
    # Regex pattern to match exercise numbers and answers (handles both 2.x and 3.x)
    pattern = r"(\d+)\.(\d+) - ([A-Z])"
    matches = re.findall(pattern, latex_content)
    
    # Convert matches to list of dictionaries and sort by exercise number
    exercises = []
    for section, num, letter in matches:
        exercises.append({
            "exercise_number": f"{section}.{num}",
            "section": int(section),  # For grouping
            "numeric_value": int(num),  # For sorting
            "letter": letter
        })
    
    # Sort by section first, then by exercise number
    exercises.sort(key=lambda x: (x["section"], x["numeric_value"]))
    
    # Remove temporary fields
    for ex in exercises:
        del ex["section"]
        del ex["numeric_value"]
    
    return exercises

def save_to_csv(exercises, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['exercise_number', 'letter']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(exercises)

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_exercises.py <input.tex>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = Path(input_file).stem + ".csv"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            latex_content = f.read()
        
        exercises = extract_exercises(latex_content)
        save_to_csv(exercises, output_file)
        
        print(f"Successfully extracted {len(exercises)} exercises to {output_file}")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
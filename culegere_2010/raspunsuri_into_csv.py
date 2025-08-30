import re
import argparse
import os
import csv
from operator import itemgetter

def parse_latex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract section name
    section_match = re.search(r'\\section\*\{(.*?)\}', content)
    if not section_match:
        raise ValueError("Could not find section name in the file")
    section_name = section_match.group(1)
    
    # Find all exercise-answer pairs
    pattern = r'(\d+\.\d+) - ([A-Z])'
    matches = re.findall(pattern, content)
    
    if not matches:
        raise ValueError("No exercise-answer pairs found in the file")
    
    return section_name, matches

def natural_sort_key(item):
    """Key function for natural sorting of exercise numbers"""
    exercise = item[0]  # item is (exercise, answer)
    return [float(part) for part in exercise.split('.')]

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a LaTeX file with exercises and answers.')
    parser.add_argument('input_file', help='Path to the LaTeX file to process')
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.isfile(args.input_file):
        print(f"Error: File '{args.input_file}' not found.")
        return
    
    try:
        # Parse the file
        section_name, data = parse_latex_file(args.input_file)
        num_exercises = len(data)
        print(f"Extracted {num_exercises} exercises from '{args.input_file}'")
        
        # Sort the data
        data_sorted = sorted(data, key=natural_sort_key)
        
        # Generate output filename (in same directory as script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        input_basename = os.path.splitext(os.path.basename(args.input_file))[0]
        output_file = os.path.join(script_dir, f"{input_basename}.csv")
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['section', 'exercise_number', 'answer'])
            for exercise, answer in data_sorted:
                writer.writerow([section_name, exercise, answer])
        
        print(f"Results saved to '{output_file}'")
        
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == '__main__':
    main()
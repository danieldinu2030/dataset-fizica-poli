## Adds measure units with LaTeX math 
# 10 kg becomes $10 \mathrm{~kg}$ and so on

import re
import argparse

def replace_units(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Define units list
    units = ["m", "cm", "mm", "km",             # length 
             "g", "kg", "Pa", "kPa", "atm",     # weight, pressure
             "J", "kJ", "MJ",                   # heat, work
             "K", "s", "ms", "h",               # absolute temperature, time 
             "N", "kN", "W", "kW",              # force, power 
             "Hz", "A", "mA", "V"]              # frequency, current, tension
    unit_pattern = r"\b(\d+(?:\.\d+)?)\s*(" + "|".join(units) + r")\b"

    # Replacement function to format properly
    def repl(match):
        number = match.group(1)
        unit = match.group(2)
        return f"${number} \mathrm{{~{unit}}}$"

    new_content, num_replacements = re.subn(unit_pattern, repl, content)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Replacements made: {num_replacements}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace plain numbers with units into LaTeX math mode.")
    parser.add_argument("filename", help="Input file to process")
    args = parser.parse_args()

    replace_units(args.filename)

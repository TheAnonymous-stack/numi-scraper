#!/usr/bin/env python3
"""
Quick verification script to check if HTML label fixes were applied correctly
"""
import re
from pathlib import Path

def check_file(filepath):
    """Check if a file has any remaining incorrect labels"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract expected info from filename
        filename = filepath.name
        pattern = r'^(Gr6)_(\d+)_(E\d+)_(\d+)_(\d+)\.html$'
        match = re.match(pattern, filename)
        if not match:
            return False, "Filename doesn't match expected pattern"

        grade, week, exercise, variation, step = match.groups()

        # Look for problematic labels (missing E3/E1/E2/E4/E5)
        problem_pattern = f'label="Gr6_{week}_({variation})_({step})_(step_\d+)"'
        problems = re.findall(problem_pattern, content)

        if problems:
            return False, f"Found {len(problems)} problems: {problems}"

        return True, "OK"

    except Exception as e:
        return False, f"Error: {e}"

def main():
    html_dir = Path("html")
    test_files = [
        "Gr6_24_E3_3_1.html",
        "Gr6_16_E1_1_10.html",
        "Gr6_23_E1_1_1.html",
        "Gr6_23_E3_3_1.html"
    ]

    print("Quick verification of fixes:")
    print("=" * 40)

    for filename in test_files:
        filepath = html_dir / filename
        if filepath.exists():
            is_ok, message = check_file(filepath)
            status = "FIXED" if is_ok else "PROBLEM"
            print(f"{status}: {filename} - {message}")
        else:
            print(f"- SKIP: {filename} (not found)")

if __name__ == "__main__":
    main()
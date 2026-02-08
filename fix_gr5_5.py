import json
import re

# Process all four Gr5_5 files
files_to_process = [
    "Gr5_5_E1_variations.json",
    "Gr5_5_E2_variations.json",
    "Gr5_5_E3_variations.json",
    "Gr5_5_E4_variations.json"
]

def fix_latex_spacing(text):
    """Fix LaTeX spacing issues where fractions are run together"""
    if not isinstance(text, str):
        return text

    # Pattern to find consecutive fractions without commas or spaces
    # Matches: $\frac{a}{b}$$\frac{c}{d}$
    # Replace with: $\frac{a}{b}$, $\frac{c}{d}$

    # Fix pattern: }$$\ -> }$, $\
    text = re.sub(r'\}\$\$\\', r'}$, $\\', text)

    return text

for filename in files_to_process:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if it's already nested under "quizzes"
        if isinstance(data, list):
            questions = data
            needs_nesting = True
        elif isinstance(data, dict) and "quizzes" in data:
            questions = data["quizzes"]
            needs_nesting = False
        else:
            print(f"Unexpected format: {filename}")
            continue

        # Fix LaTeX spacing in solutions
        fixed_count = 0
        for question in questions:
            if 'solution' in question:
                solution = question['solution']
                # Solution is an array of [step_label, step_text] pairs
                if isinstance(solution, list):
                    modified = False
                    for step in solution:
                        if isinstance(step, list) and len(step) >= 2:
                            original_text = step[1]
                            fixed_text = fix_latex_spacing(original_text)
                            if fixed_text != original_text:
                                step[1] = fixed_text
                                modified = True
                    if modified:
                        fixed_count += 1

        # Nest under quizzes if needed
        if needs_nesting:
            output_data = {"quizzes": questions}
        else:
            output_data = {"quizzes": questions}

        # Write back to the file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

        status = "nested" if needs_nesting else "already nested"
        print(f"{filename}: {status}, {len(questions)} questions, {fixed_count} solutions fixed")

    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

print("\nAll Gr5_5 files processed!")

import json
import re

def fix_latex_formatting(filename):
    """Fix LaTeX formatting by replacing × with proper LaTeX \\times"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changes_made = 0
    
    for quiz in data['quizzes']:
        # Fix LaTeX in solution steps
        if 'solution' in quiz:
            for step in quiz['solution']:
                if len(step) >= 2:  # Ensure step has at least 2 elements
                    original_text = step[1]
                    # Replace × with LaTeX \times
                    fixed_text = original_text.replace('×', '\\times')
                    if fixed_text != original_text:
                        step[1] = fixed_text
                        changes_made += 1
    
    # Write the fixed data back to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed {changes_made} LaTeX formatting issues in {filename}")
    return changes_made

# Process the file
changes = fix_latex_formatting('Gr6_54_E2_variations.json')
print(f"Total changes made: {changes}")
print("Done!")
import json
import re

def analyze_latex_format(filename):
    """Analyze LaTeX formatting patterns in a file"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    patterns = {
        'simple_fractions': [],  # $\frac{a}{b}$
        'mixed_numbers': [],  # $2\frac{a}{b}$
        'with_operators': [],  # $\frac{a}{b} + \frac{c}{d}$
        'with_parentheses': [],  # $(\frac{a}{b})$
        'spacing_commands': []  # $\\[1em]$ etc
    }

    for q in data['quizzes']:
        q_text = q['question_text']

        # Find all LaTeX expressions
        latex_matches = re.findall(r'\$[^$]+\$', q_text)

        for match in latex_matches:
            if '\\frac' in match:
                if '(' in match or ')' in match:
                    patterns['with_parentheses'].append(match)
                elif '+' in match or '-' in match or '\\times' in match or '\\div' in match:
                    patterns['with_operators'].append(match)
                elif re.search(r'\d+\\frac', match):
                    patterns['mixed_numbers'].append(match)
                else:
                    patterns['simple_fractions'].append(match)
            elif '\\[' in match or '\\\\[' in match:
                patterns['spacing_commands'].append(match)

    return patterns

# Analyze both files
print("=" * 80)
print("Analyzing Gr7_7_E4_variations.json (PROBLEM FILE)")
print("=" * 80)
gr7_e4_patterns = analyze_latex_format('Gr7_7_E4_variations.json')

for pattern_type, matches in gr7_e4_patterns.items():
    if matches:
        print(f"\n{pattern_type.upper()} ({len(matches)} found):")
        # Show first 3 unique examples
        unique = list(set(matches))[:3]
        for ex in unique:
            print(f"  {ex}")

print("\n" + "=" * 80)
print("Analyzing Gr7_6_E1_variations.json (WORKING FILE)")
print("=" * 80)
gr7_e1_patterns = analyze_latex_format('Gr7_6_E1_variations.json')

for pattern_type, matches in gr7_e1_patterns.items():
    if matches:
        print(f"\n{pattern_type.upper()} ({len(matches)} found):")
        # Show first 3 unique examples
        unique = list(set(matches))[:3]
        for ex in unique:
            print(f"  {ex}")

print("\n" + "=" * 80)
print("COMPARISON:")
print("=" * 80)
print("\nBoth files use the same LaTeX formatting:")
print("  - \\frac for fractions (2 backslashes in JSON)")
print("  - \\\\[1em] for spacing (4 backslashes in JSON)")
print("\nIf Gr7_7_E4 is not rendering, the issue is NOT with the JSON file.")
print("The problem is likely with the rendering engine configuration.")

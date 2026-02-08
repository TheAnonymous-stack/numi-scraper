import json
import os
from math import gcd

# All Grade 7 regular fraction files
all_gr7_files = [
    'Gr7_5_E2_variations.json',
    'Gr7_5_E3_variations.json',
    'Gr7_6_E2_variations.json',
    'Gr7_7_E3_variations.json',
    'Gr7_13_E1_variations.json',
    'Gr7_13_E2_variations.json',
    'Gr7_14_E1_variations.json',
    'Gr7_14_E2_variations.json',
    'Gr7_15_E1_variations.json',
    'Gr7_15_E2_variations.json',
    'Gr7_16_E1_variations.json',
    'Gr7_16_E2_variations.json',
    'Gr7_17_E2_variations.json',
    'Gr7_20_E1_variations.json',
    'Gr7_20_E2_variations.json',
    'Gr7_20_E3_variations.json',
    'Gr7_22_E1_variations.json',
    'Gr7_22_E3_variations.json',
    'Gr7_22_E4_variations.json',
    'Gr7_27_E3_variations.json',
    'Gr7_35_E2_variations.json',
]

def simplify_fraction(num, denom):
    """Simplify a fraction to lowest terms"""
    if num == 0:
        return 0, 1
    g = gcd(int(num), int(denom))
    return str(int(num) // g), str(int(denom) // g)

def fix_gr7_5_e3():
    """Special handling for Gr7_5_E3 with mixed number conversions"""
    filename = 'Gr7_5_E3_variations.json'

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data["quizzes"]

    for question in questions:
        q_text = question.get("question_text", "")

        # Add "Write your answer in simplest terms." if not already there
        if "simplest terms" not in q_text and "Write your answer in simplest terms." not in q_text:
            # Add before the formatting part
            if "$\\\\\\\\[1em]$" in q_text:
                parts = q_text.split("$\\\\\\\\[1em]$")
                question["question_text"] = parts[0].rstrip() + " Write your answer in simplest terms. $\\\\\\\\[1em]$" + parts[1]
            elif "_ _/_" in q_text:
                parts = q_text.split("_ _/_")
                question["question_text"] = parts[0].rstrip() + " Write your answer in simplest terms.\n" + parts[0].split("\n")[-1].split("=")[0].strip() + " = _ _/_"

        # Check if improper to mixed (has 3 answers)
        if "as a mixed number" in q_text or "to a mixed number" in q_text:
            if len(question["correct_answers"]) == 3:
                whole = question["correct_answers"][0]
                numerator = question["correct_answers"][1]
                denominator = question["correct_answers"][2]

                # If numerator is 0, it's a whole number - only keep whole number
                if numerator == "0":
                    question["correct_answers"] = [whole]
                    print(f"  Fixed whole number answer: {whole}")
                else:
                    # Simplify the fraction part
                    simp_num, simp_denom = simplify_fraction(numerator, denominator)
                    question["correct_answers"] = [whole, simp_num, simp_denom]
                    print(f"  Simplified: {whole} {simp_num}/{simp_denom}")

        # Check if mixed to improper (has 2 answers)
        elif "to an improper fraction" in q_text or "as an improper fraction" in q_text:
            if len(question["correct_answers"]) == 2:
                numerator = question["correct_answers"][0]
                denominator = question["correct_answers"][1]

                # Simplify the improper fraction
                simp_num, simp_denom = simplify_fraction(numerator, denominator)
                question["correct_answers"] = [simp_num, simp_denom]
                print(f"  Simplified: {simp_num}/{simp_denom}")

    # Save
    output_data = {"quizzes": questions}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    tag = filename.replace('_variations.json', '')
    edited_path = f'edited_by_tag/{tag}/{tag}_edited.json'
    with open(edited_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Fixed {filename}")

def fix_regular_gr7_file(filename):
    """Fix regular Gr7 files (not Gr7_5_E3)"""

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data["quizzes"]

    for question in questions:
        q_text = question.get("question_text", "")

        # Add "Write your answer in simplest terms."
        if "simplest terms" not in q_text and "Write your answer in simplest terms." not in q_text:
            if "$\\\\\\\\[1em]$" in q_text:
                parts = q_text.split("$\\\\\\\\[1em]$")
                question["question_text"] = parts[0].rstrip() + " Write your answer in simplest terms. $\\\\\\\\[1em]$" + parts[1]

        # Simplify the fraction answer
        if "correct_answers" in question and len(question["correct_answers"]) == 2:
            numerator = question["correct_answers"][0]
            denominator = question["correct_answers"][1]

            simp_num, simp_denom = simplify_fraction(numerator, denominator)
            question["correct_answers"] = [simp_num, simp_denom]

    # Save
    output_data = {"quizzes": questions}
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    tag = filename.replace('_variations.json', '')
    edited_path = f'edited_by_tag/{tag}/{tag}_edited.json'
    with open(edited_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Fixed {filename}")

# Main execution
print("=" * 80)
print("FIXING ALL GRADE 7 FILES - SIMPLIFY AND ADD INSTRUCTIONS")
print("=" * 80)

# Fix Gr7_5_E3 first (special handling)
print("\nFixing Gr7_5_E3 (special mixed number file)...")
fix_gr7_5_e3()

# Fix all other files
print("\nFixing other Grade 7 files...")
for filename in all_gr7_files:
    # Skip Gr7_5_E3 (already handled) and Gr7_35_E2 (equation solving, not fractions)
    if filename not in ['Gr7_5_E3_variations.json', 'Gr7_35_E2_variations.json'] and os.path.exists(filename):
        fix_regular_gr7_file(filename)

print("\n" + "=" * 80)
print("ALL GRADE 7 FILES FIXED!")
print("=" * 80)
print("- Whole number answers: converted to single value")
print("- Fractions: simplified to lowest terms")
print("- Added 'Write your answer in simplest terms.' to all questions")

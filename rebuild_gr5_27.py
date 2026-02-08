import json
import math

def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(num, den):
    """Simplify a fraction to lowest terms"""
    if den == 0:
        return num, den
    g = gcd(int(num), int(den))
    return str(num // g), str(den // g)

# Read all Gr5_27 original files
gr5_27_files = [
    "Gr5_27_E1_variations.json",
    "Gr5_27_E4_variations.json"
]

all_questions = []

for filename in gr5_27_files:
    with open(filename, 'r', encoding='utf-8') as f:
        questions = json.load(f)

        # Only transform E1 questions (not E4)
        if "E1" in filename:
            for q in questions:
                correct_answers = q.get('correct_answers', [])

                # Check if it's a simple fraction answer
                if (len(correct_answers) == 1 and
                    isinstance(correct_answers[0], str) and
                    '/' in correct_answers[0] and
                    ' ' not in correct_answers[0]):  # Not a mixed fraction

                    # This is a regular fraction - transform it
                    fraction_str = correct_answers[0]
                    try:
                        parts = fraction_str.split('/')
                        if len(parts) == 2:
                            num = int(parts[0])
                            den = int(parts[1])

                            # Simplify the fraction
                            simp_num, simp_den = simplify_fraction(num, den)

                            # Transform to grade6 format
                            q['question_type'] = "Multiple fill in the blank"
                            q_text = q.get('question_text', '').rstrip()
                            q['question_text'] = f"{q_text} $\\\\[1em]$\n\n_/_ "
                            q['correct_answers'] = [simp_num, simp_den]
                            q['has_alternate_answers'] = True
                            q['orderMatter'] = True
                    except:
                        pass

        all_questions.extend(questions)

# Wrap in quizzes key
output_data = {"quizzes": all_questions}

# Save to the edited_by_tag folder
output_path = 'edited_by_tag/Gr5_27/Gr5_27_edited.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print(f"Rebuilt {output_path}")
print(f"Total questions: {len(all_questions)}")

# Count transformed
transformed = sum(1 for q in all_questions if q.get('question_type') == 'Multiple fill in the blank')
print(f"Transformed E1 questions with fractions: {transformed}")
print(f"Left unchanged (E4 and others): {len(all_questions) - transformed}")

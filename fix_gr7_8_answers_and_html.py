import json

def fix_gr7_8_e2():
    """Fix correct_answers format in Gr7_8_E2 - keep only one answer"""
    with open('Gr7_8_E2_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['quizzes']:
        # Keep only the first answer (numeric value without "dollars")
        if isinstance(question['correct_answers'], list) and len(question['correct_answers']) > 0:
            first_answer = question['correct_answers'][0]
            # Remove "dollars" if present
            if isinstance(first_answer, str) and first_answer.endswith(' dollars'):
                first_answer = first_answer.replace(' dollars', '')
            question['correct_answers'] = [first_answer]

        # Remove has_alternative_answers field if present
        if 'has_alternative_answers' in question:
            del question['has_alternative_answers']

    with open('Gr7_8_E2_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Fixed Gr7_8_E2 correct_answers format")

def fix_gr7_8_e3():
    """Fix correct_answers format in Gr7_8_E3 - keep only one answer"""
    with open('Gr7_8_E3_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['quizzes']:
        # Keep only the first answer (numeric value without "dollars")
        if isinstance(question['correct_answers'], list) and len(question['correct_answers']) > 0:
            first_answer = question['correct_answers'][0]
            # Remove "dollars" if present
            if isinstance(first_answer, str) and first_answer.endswith(' dollars'):
                first_answer = first_answer.replace(' dollars', '')
            question['correct_answers'] = [first_answer]

        # Remove has_alternative_answers field if present
        if 'has_alternative_answers' in question:
            del question['has_alternative_answers']

    with open('Gr7_8_E3_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Fixed Gr7_8_E3 correct_answers format")

def fix_gr7_8_e4():
    """Fix correct_answers format in Gr7_8_E4 - keep only one answer"""
    with open('Gr7_8_E4_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for question in data['quizzes']:
        # Keep only the first answer (numeric value)
        if isinstance(question['correct_answers'], list) and len(question['correct_answers']) > 0:
            first_answer = str(question['correct_answers'][0])
            # Ensure it's a string
            question['correct_answers'] = [first_answer]

        # Remove has_alternative_answers field if present
        if 'has_alternative_answers' in question:
            del question['has_alternative_answers']

    with open('Gr7_8_E4_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Fixed Gr7_8_E4 correct_answers format")

# Run all fixes
fix_gr7_8_e2()
fix_gr7_8_e3()
fix_gr7_8_e4()

print("\nAll files fixed with single correct_answer format")
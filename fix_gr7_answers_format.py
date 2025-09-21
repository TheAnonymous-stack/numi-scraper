import json

def fix_gr7_5_e1(file_path):
    """Fix Gr7_5_E1_variations.json to have only single numeric answers"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for quiz in data['quizzes']:
        if 'correct_answers' in quiz:
            # For Gr7_5_E1, keep only the first answer (the integer)
            if isinstance(quiz['correct_answers'], list) and quiz['correct_answers']:
                # Keep only the main answer without decimal variations
                main_answer = quiz['correct_answers'][0]
                # Remove .0 and .00 if present
                if main_answer.endswith('.0'):
                    main_answer = main_answer[:-2]
                elif main_answer.endswith('.00'):
                    main_answer = main_answer[:-3]
                quiz['correct_answers'] = [main_answer]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Fixed {file_path}")

def fix_gr7_5_e2(file_path):
    """Fix Gr7_5_E2_variations.json to have proper fraction format"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for quiz in data['quizzes']:
        if 'correct_answers' in quiz:
            # For fractions, keep only the fraction format (not decimal)
            if isinstance(quiz['correct_answers'], list) and quiz['correct_answers']:
                # Keep only fraction answers
                fraction_answers = []
                for answer in quiz['correct_answers']:
                    if '/' in answer:
                        fraction_answers.append(answer)

                # If we have fraction answers, use only those
                if fraction_answers:
                    quiz['correct_answers'] = [fraction_answers[0]]  # Keep only the first fraction
                else:
                    # If no fractions, keep the first answer
                    quiz['correct_answers'] = [quiz['correct_answers'][0]]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Fixed {file_path}")

# Fix both files
fix_gr7_5_e1('Gr7_5_E1_variations.json')
fix_gr7_5_e2('Gr7_5_E2_variations.json')

print("Completed fixing answer formats")
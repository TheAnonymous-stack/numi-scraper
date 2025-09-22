import json

def fix_correct_answers(file_path):
    """Fix the correct_answers format in JSON file"""

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    modified = False

    for quiz in data['quizzes']:
        if 'correct_answers' in quiz:
            # Check if correct_answers contains nested arrays
            if quiz['correct_answers'] and isinstance(quiz['correct_answers'][0], list):
                # Flatten the nested arrays - take first element from each nested array
                flattened_answers = []
                for answer in quiz['correct_answers']:
                    if isinstance(answer, list) and answer:
                        flattened_answers.append(answer[0])
                    elif isinstance(answer, str):
                        flattened_answers.append(answer)

                quiz['correct_answers'] = flattened_answers
                modified = True

    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Fixed {file_path}")
    else:
        print(f"No changes needed for {file_path}")

# Fix both files
fix_correct_answers('Gr7_5_E1_variations.json')
fix_correct_answers('Gr7_5_E2_variations.json')

print("Completed fixing correct_answers format")
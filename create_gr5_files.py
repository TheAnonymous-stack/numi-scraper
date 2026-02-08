import json
import re
import os

# Process Gr5_3_E4
print("Processing Gr5_3_E4_variations.json...")
with open('Gr5_3_E4_variations.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for question in questions:
    correct_answers = question.get('correct_answers', [])
    q_text = question['question_text']

    if len(correct_answers) == 1:
        answer = correct_answers[0]

        if '/' in answer and ' ' not in answer:
            # Improper fraction answer
            parts = answer.split('/')
            question['correct_answers'] = [parts[0], parts[1]]
            question['question_type'] = 'Multiple fill in the blank'

            if not q_text.endswith('$\\\\[1em]$\\n\\n_/_ '):
                q_text = q_text.rstrip('.')
                q_text += '. $\\\\[1em]$\\n\\n_/_ '
                question['question_text'] = q_text

            question['orderMatter'] = True
            question['has_alternate_answers'] = True

        elif ' ' in answer and '/' in answer:
            # Mixed number answer
            match = re.match(r'(\d+)\s+(\d+)/(\d+)', answer)
            if match:
                question['correct_answers'] = [match.group(1), match.group(2), match.group(3)]
                question['question_type'] = 'Multiple fill in the blank'

                # Extract the fraction from question text
                frac_match = re.search(r'\$\\frac\{(\d+)\}\{(\d+)\}\$', q_text)
                if frac_match:
                    numerator = frac_match.group(1)
                    denominator = frac_match.group(2)
                    q_text = re.sub(r'\s*as a mixed number\.?\s*', '', q_text)
                    q_text = q_text.strip() + f' as a mixed number. Write your answer in simplest terms. = _ _/_'
                    question['question_text'] = q_text

                question['orderMatter'] = True
                question['has_alternate_answers'] = True

# Create output directory
os.makedirs('edited_by_tag/Gr5_3_E4', exist_ok=True)

# Write Gr5_3_E4
data = {'quizzes': questions}
with open('edited_by_tag/Gr5_3_E4/Gr5_3_E4_edited.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Created Gr5_3_E4_edited.json")

# Process Gr5_6_E2, E3, E4
files_to_process = [
    ('Gr5_6_E2_variations.json', 'Gr5_6_E2'),
    ('Gr5_6_E3_variations.json', 'Gr5_6_E3'),
    ('Gr5_6_E4_variations.json', 'Gr5_6_E4')
]

for filename, tag in files_to_process:
    print(f"\nProcessing {filename}...")

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = data['quizzes']
    updated_count = 0

    for question in questions:
        correct_answers = question.get('correct_answers', [])

        if len(correct_answers) == 1:
            answer = correct_answers[0]

            if '.' in answer and answer.endswith('0') and not answer.endswith('.0'):
                alternate = answer.rstrip('0')
                question['correct_answers'] = [answer, alternate]
                question['has_alternate_answers'] = True
                updated_count += 1

    print(f"Updated {updated_count} questions with alternate answers")

    os.makedirs(f'edited_by_tag/{tag}', exist_ok=True)
    output_file = f'edited_by_tag/{tag}/{tag}_edited.json'

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_file}")

print("\nAll Grade 5 files created successfully!")

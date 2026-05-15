import json
import re

def fix_correct_answers(quiz):
    """Fix the correct answers to be actual values instead of letters"""
    
    if 'correct_answers' not in quiz or 'choices' not in quiz:
        return quiz
    
    # Map letter answers to actual values from choices
    letter_to_index = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    
    fixed_answers = []
    for answer in quiz['correct_answers']:
        if answer.upper() in letter_to_index:
            index = letter_to_index[answer.upper()]
            if index < len(quiz['choices']):
                fixed_answers.append(quiz['choices'][index])
            else:
                fixed_answers.append(answer)  # Keep original if index out of bounds
        else:
            fixed_answers.append(answer)  # Keep if not a letter
    
    quiz['correct_answers'] = fixed_answers
    return quiz

def process_file():
    """Process and fix Gr6_12_E3_variations.json"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E3_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        original_answers = quiz.get('correct_answers', [])
        quiz = fix_correct_answers(quiz)
        
        if original_answers != quiz.get('correct_answers', []):
            fixed_count += 1
            print(f"Fixed question {quiz.get('question_number', '?')}: {original_answers} -> {quiz['correct_answers']}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E3_variations.json")
    print("Correct answers now show actual values instead of letters")

if __name__ == "__main__":
    process_file()
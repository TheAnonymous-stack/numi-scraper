import json
import re

def fix_question_answers(quiz):
    """Fix the correct answers based on the question type"""
    
    question_text = quiz.get('question_text', '')
    
    # Parse the question to determine what's being asked
    if 'in which place is the' in question_text.lower():
        # Question asks for the place value - answer should be hundreds/tens/ones
        # Extract the number and digit being asked about
        match = re.search(r'In (\d+), in which place is the (\d)', question_text)
        if match:
            number = match.group(1)
            digit = match.group(2)
            
            # Find the position of the digit in the number
            for i, d in enumerate(number):
                if d == digit:
                    position = len(number) - i
                    if position == 3:
                        quiz['correct_answers'] = ['hundreds']
                    elif position == 2:
                        quiz['correct_answers'] = ['tens']
                    elif position == 1:
                        quiz['correct_answers'] = ['ones']
                    break
    
    elif 'what digit is in the' in question_text.lower():
        # Question asks for the digit - answer should be a number
        match = re.search(r'In (\d+), what digit is in the (\w+) place', question_text)
        if match:
            number = match.group(1)
            place = match.group(2).lower()
            
            # Get the digit at the specified place
            if place == 'hundreds' and len(number) >= 3:
                quiz['correct_answers'] = [number[-3]]
            elif place == 'tens' and len(number) >= 2:
                quiz['correct_answers'] = [number[-2]]
            elif place == 'ones':
                quiz['correct_answers'] = [number[-1]]
    
    return quiz

def process_file():
    """Process and fix Gr6_12_E3_variations.json with proper answers"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E3_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        original_answers = quiz.get('correct_answers', [])[:]
        quiz = fix_question_answers(quiz)
        
        if original_answers != quiz.get('correct_answers', []):
            fixed_count += 1
            print(f"Fixed Q{quiz.get('question_number', '?')}: {quiz.get('question_text', '')[:50]}... -> {quiz['correct_answers']}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E3_variations.json")
    print("Answers now correctly show:")
    print("  - Place values (hundreds/tens/ones) for 'in which place' questions")
    print("  - Digits (0-9) for 'what digit' questions")

if __name__ == "__main__":
    process_file()
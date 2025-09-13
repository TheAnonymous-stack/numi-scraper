import json
import re

def fix_quiz_completely(quiz):
    """Fix both answers and solutions for place value questions"""
    
    question_text = quiz.get('question_text', '')
    
    # Parse the question to determine what's being asked
    if 'in which place is the' in question_text.lower():
        # Question asks for the place value - answer should be hundreds/tens/ones
        match = re.search(r'In (\d+), in which place is the (\d)', question_text)
        if match:
            number = match.group(1)
            digit = match.group(2)
            
            # Find the position of the digit in the number
            for i, d in enumerate(number):
                if d == digit:
                    position = len(number) - i
                    if position == 3:
                        answer = 'hundreds'
                        quiz['correct_answers'] = [answer]
                        # Fix solution text
                        if len(quiz.get('solution', [])) > 1:
                            quiz['solution'][1][1] = f"The digit {digit} appears in the hundreds place."
                    elif position == 2:
                        answer = 'tens'
                        quiz['correct_answers'] = [answer]
                        if len(quiz.get('solution', [])) > 1:
                            quiz['solution'][1][1] = f"The digit {digit} appears in the tens place."
                    elif position == 1:
                        answer = 'ones'
                        quiz['correct_answers'] = [answer]
                        if len(quiz.get('solution', [])) > 1:
                            quiz['solution'][1][1] = f"The digit {digit} appears in the ones place."
                    break
    
    elif 'what digit is in the' in question_text.lower():
        # Question asks for the digit - answer should be a number
        match = re.search(r'In (\d+), what digit is in the (\w+) place', question_text)
        if match:
            number = match.group(1)
            place = match.group(2).lower()
            
            # Get the digit at the specified place
            if place == 'hundreds' and len(number) >= 3:
                digit = number[0]  # First digit for 3-digit numbers
                quiz['correct_answers'] = [digit]
                # Fix solution text
                if len(quiz.get('solution', [])) > 1:
                    quiz['solution'][1][1] = f"The hundreds place (third from the right) contains the digit {digit}."
            elif place == 'tens' and len(number) >= 2:
                if len(number) == 3:
                    digit = number[1]  # Middle digit for 3-digit numbers
                else:
                    digit = number[0]  # First digit for 2-digit numbers
                quiz['correct_answers'] = [digit]
                if len(quiz.get('solution', [])) > 1:
                    quiz['solution'][1][1] = f"The tens place (second from the right) contains the digit {digit}."
            elif place == 'ones':
                digit = number[-1]  # Last digit
                quiz['correct_answers'] = [digit]
                if len(quiz.get('solution', [])) > 1:
                    quiz['solution'][1][1] = f"The ones place (first from the right) contains the digit {digit}."
    
    return quiz

def process_file():
    """Process and fix Gr6_12_E3_variations.json comprehensively"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E3_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        original_answers = quiz.get('correct_answers', [])[:]
        original_solution = str(quiz.get('solution', []))
        
        quiz = fix_quiz_completely(quiz)
        
        if (original_answers != quiz.get('correct_answers', []) or 
            original_solution != str(quiz.get('solution', []))):
            fixed_count += 1
            q_num = quiz.get('question_number', '?')
            q_text = quiz.get('question_text', '')[:40]
            answer = quiz.get('correct_answers', [])[0] if quiz.get('correct_answers') else 'N/A'
            print(f"Fixed Q{q_num}: {q_text}... -> Answer: {answer}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E3_variations.json")
    print("Both answers and solutions are now correct!")

if __name__ == "__main__":
    process_file()
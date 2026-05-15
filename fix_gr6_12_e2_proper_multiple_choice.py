import json
import re

def create_multiple_choice_question(num1, num2, num3):
    """Create a proper multiple choice question with choices field"""
    
    # Convert to integers for calculations
    n1 = int(num1)
    n2 = int(num2)
    n3 = int(num3)
    
    # Middle number stays in place
    middle_num = num2
    
    # Determine which number to rearrange (usually the smaller one for easier calculation)
    if n1 <= n3:
        first_blank = num1
        last_num = num3
    else:
        first_blank = num3
        last_num = num1
    
    # Calculate intermediate and final results
    product_inside = n1 * n3
    final_answer = n1 * n2 * n3
    
    # Create the question text with simple underlines (no LaTeX)
    question_text = f"""Use properties to find the product.
{num1} × {num2} × {num3}

Step 1: = {middle_num} × _____ × {last_num}
Step 2: = {middle_num} × (_____ × {last_num})
Step 3: = {middle_num} × _____
Step 4: = _____"""
    
    # Create the correct answers array
    correct_answers = [
        first_blank,
        first_blank,
        str(product_inside),
        str(final_answer)
    ]
    
    # Create wrong answers for each blank
    # For blank 1 and 2: wrong options are other numbers and sums
    wrong_1_1 = str(n1 + n2)
    wrong_1_2 = str(n2)
    wrong_1_3 = str(n3) if first_blank != str(n3) else str(n1)
    
    # For blank 3: wrong options are other products
    wrong_3_1 = str(n1 * n2)
    wrong_3_2 = str(n2 * n3)
    wrong_3_3 = str(n1 + n3)
    
    # For blank 4: wrong options 
    wrong_4_1 = str(n1 + n2 + n3)
    wrong_4_2 = str(n1 * n2)
    wrong_4_3 = str(n2 * n3)
    
    # Create choices array - one set of choices for each blank
    choices = [
        # Choices for blank 1
        sorted(list(set([first_blank, wrong_1_1, wrong_1_2, wrong_1_3]))),
        # Choices for blank 2 (same as blank 1)
        sorted(list(set([first_blank, wrong_1_1, wrong_1_2, wrong_1_3]))),
        # Choices for blank 3
        sorted(list(set([str(product_inside), wrong_3_1, wrong_3_2, wrong_3_3]))),
        # Choices for blank 4
        sorted(list(set([str(final_answer), wrong_4_1, wrong_4_2, wrong_4_3])))
    ]
    
    return question_text, correct_answers, choices

def process_file():
    """Process and convert to proper multiple choice format"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            original = quiz['question_text']
            
            # Extract numbers from the original question
            match = re.search(r'\$?(\d+)\s*\\?(?:cdot|·|×)?\s*(\d+)\s*\\?(?:cdot|·|×)?\s*(\d+)', original)
            if match:
                num1 = match.group(1)
                num2 = match.group(2)
                num3 = match.group(3)
                
                # Create new multiple choice format
                question_text, correct_answers, choices = create_multiple_choice_question(num1, num2, num3)
                
                quiz['question_text'] = question_text
                quiz['correct_answers'] = correct_answers
                quiz['choices'] = choices
                quiz['question_type'] = "Multiple choice fill in the blank"
                
                fixed_count += 1
                print(f"Fixed question {quiz.get('question_number', '?')}: {num1} × {num2} × {num3}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nConverted {fixed_count} questions to proper multiple choice format")
    print("Each blank now has its own 'choices' array with 4 options")

if __name__ == "__main__":
    process_file()
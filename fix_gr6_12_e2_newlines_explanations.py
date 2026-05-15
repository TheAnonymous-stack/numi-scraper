import json
import re

def fix_question_with_newlines_and_explanations(text):
    """Fix the question text to have each answer box on a new line with explanations"""
    
    # Extract the numbers from the first line
    match = re.search(r'\$(\d+)\s*\\cdot\s*(\d+)\s*\\cdot\s*(\d+)\$', text)
    
    if match:
        num1 = match.group(1)
        num2 = match.group(2)
        num3 = match.group(3)
        
        # Create properly formatted question with clear line breaks and explanations
        fixed_text = f"""Use properties to find the product.
${num1} \\cdot {num2} \\cdot {num3}$

Step 1: Rearrange the numbers (commutative property)
$= {num2} \\cdot$ _____ $\\cdot {num3}$

Step 2: Group the numbers to make multiplication easier (associative property)
$= {num2} \\cdot ($ _____ $\\cdot {num3})$

Step 3: Calculate the product inside the parentheses
$= {num2} \\cdot$ _____

Step 4: Calculate the final product
$=$ _____"""
        
        return fixed_text
    
    return text

def fix_answers_for_proper_order(quiz, num1, num2, num3):
    """Fix the answer array to match the proper order of operations"""
    
    # Determine which numbers to rearrange for easier calculation
    # We want to group the smaller numbers or numbers that multiply to a round number
    
    # Convert to integers for comparison
    n1 = int(num1)
    n2 = int(num2)
    n3 = int(num3)
    
    # The middle number (num2) stays in place, we rearrange num1 and num3
    # First answer: the number we're moving to the middle position (usually the smaller of num1 or num3)
    if n1 <= n3:
        first_answer = num1
        grouped_product = n1 * n3
    else:
        first_answer = num3
        grouped_product = n1 * n3
    
    # Second answer: same number repeated for the grouping
    second_answer = first_answer
    
    # Third answer: product of the grouped numbers
    third_answer = str(grouped_product)
    
    # Fourth answer: final product
    final_answer = str(n1 * n2 * n3)
    
    quiz['correct_answers'] = [
        first_answer,
        second_answer,
        third_answer,
        final_answer
    ]
    
    return quiz

def process_file():
    """Process and fix Gr6_12_E2_variations.json"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            original = quiz['question_text']
            
            # Extract numbers from the original question
            match = re.search(r'\$(\d+)\s*\\cdot\s*(\d+)\s*\\cdot\s*(\d+)\$', original)
            if match:
                num1 = match.group(1)
                num2 = match.group(2)
                num3 = match.group(3)
                
                # Fix the question text
                fixed = fix_question_with_newlines_and_explanations(original)
                
                if fixed != original:
                    quiz['question_text'] = fixed
                    
                    # Fix the answers to match the new format
                    quiz = fix_answers_for_proper_order(quiz, num1, num2, num3)
                    
                    fixed_count += 1
                    print(f"Fixed question {quiz.get('question_number', '?')}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E2_variations.json")
    print("Each answer box is now on a new line with explanations")

if __name__ == "__main__":
    process_file()
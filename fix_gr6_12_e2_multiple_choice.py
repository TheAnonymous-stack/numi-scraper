import json
import re

def create_multiple_choice_question(num1, num2, num3):
    """Create a multiple choice question with simple underlines"""
    
    # Convert to integers for calculations
    n1 = int(num1)
    n2 = int(num2)
    n3 = int(num3)
    
    # Determine which number to rearrange (usually the smaller one)
    if n1 <= n3:
        rearranged = num1
        last = num3
    else:
        rearranged = num3
        last = num1
    
    # Calculate intermediate and final results
    product_inside = n1 * n3
    final_answer = n1 * n2 * n3
    
    # Create the question text with simple multiplication symbols
    question_text = f"""Use properties to find the product.
{num1} × {num2} × {num3}

Step 1: = {num2} × _____ × {last}
Step 2: = {num2} × (_____ × {last})
Step 3: = {num2} × _____
Step 4: = _____

For each blank above, select the correct answer in order:"""
    
    # Create the correct answers array
    correct_answers = [
        rearranged,
        rearranged,
        str(product_inside),
        str(final_answer)
    ]
    
    # Create answer choices for each blank
    # Mix in some incorrect options
    choices_blank1 = [rearranged, num2, last, str(n1 + n2)]
    choices_blank2 = [rearranged, num2, last, str(n2 + n3)]
    choices_blank3 = [str(product_inside), str(n1 + n3), str(n2 * n3), str(n1 * n2)]
    choices_blank4 = [str(final_answer), str(n1 + n2 + n3), str(n1 * n2), str(n2 * n3)]
    
    # Create the answer_choices structure
    answer_choices = {
        "blank1": sorted(set(map(str, choices_blank1))),
        "blank2": sorted(set(map(str, choices_blank2))),
        "blank3": sorted(set(map(str, choices_blank3))),
        "blank4": sorted(set(map(str, choices_blank4)))
    }
    
    return question_text, correct_answers, answer_choices

def process_file():
    """Process and convert to multiple choice format"""
    
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
                question_text, correct_answers, answer_choices = create_multiple_choice_question(num1, num2, num3)
                
                quiz['question_text'] = question_text
                quiz['correct_answers'] = correct_answers
                quiz['answer_choices'] = answer_choices
                quiz['question_type'] = "Multiple choice with multiple blanks"
                
                fixed_count += 1
                print(f"Fixed question {quiz.get('question_number', '?')}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nConverted {fixed_count} questions to multiple choice format")
    print("Each blank now has its own set of answer choices")

if __name__ == "__main__":
    process_file()
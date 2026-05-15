import json
import re

def fix_question_with_answer_boxes(text):
    """Fix the question text to use proper answer box notation instead of underscores"""
    
    # Extract the numbers from the first line
    match = re.search(r'\$(\d+)\s*\\cdot\s*(\d+)\s*\\cdot\s*(\d+)\$', text)
    
    if match:
        num1 = match.group(1)
        num2 = match.group(2)
        num3 = match.group(3)
        
        # Determine which number goes in the middle (usually the larger one)
        # Based on the pattern, num2 is typically the middle number
        middle_num = num2
        
        # Create properly formatted question with answer boxes
        # Using [[box]] notation for answer input fields
        fixed_text = f"""Use properties to find the product.
${num1} \\cdot {num2} \\cdot {num3}$
$= {middle_num} \\cdot$ [[box1]] $\\cdot$ [[box2]]
$= {middle_num} \\cdot ($ [[box3]] $\\cdot$ [[box4]] $)$
$= {middle_num} \\cdot$ [[box5]]
$=$ [[box6]]"""
        
        return fixed_text
    
    return text

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
            
            # Fix to use answer boxes
            fixed = fix_question_with_answer_boxes(original)
            
            if fixed != original:
                quiz['question_text'] = fixed
                fixed_count += 1
                
                # Also ensure we have the right number of answers
                if 'correct_answers' in quiz:
                    # The correct answers should map to the boxes
                    # For most questions, we need to rearrange based on the pattern
                    answers = quiz['correct_answers']
                    if len(answers) == 4:
                        # We need 6 boxes total:
                        # box1: first number rearranged
                        # box2: last number
                        # box3: first number repeated in parentheses
                        # box4: last number repeated in parentheses  
                        # box5: product of first and last
                        # box6: final answer
                        
                        # Expand to 6 answers matching the boxes
                        first_num = answers[0]  # The number that gets rearranged
                        second_num = answers[1]  # Same number repeated
                        product_inside = answers[2]  # Product of the two rearranged numbers
                        final_answer = answers[3]  # Final answer
                        
                        # Determine what the last number should be based on the question
                        question_nums = re.search(r'\$(\d+)\s*\\cdot\s*(\d+)\s*\\cdot\s*(\d+)\$', original)
                        if question_nums:
                            n1 = question_nums.group(1)
                            n2 = question_nums.group(2)
                            n3 = question_nums.group(3)
                            
                            # The pattern is usually to rearrange the smaller numbers
                            if n1 == first_num:
                                last_num = n3
                            else:
                                last_num = n1
                            
                            quiz['correct_answers'] = [
                                first_num,      # box1
                                last_num,       # box2
                                first_num,      # box3
                                last_num,       # box4
                                product_inside, # box5
                                final_answer    # box6
                            ]
                
                print(f"Fixed question {quiz.get('question_number', '?')}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E2_variations.json")
    print("Replaced underscores with answer box notation [[box1]], [[box2]], etc.")

if __name__ == "__main__":
    process_file()
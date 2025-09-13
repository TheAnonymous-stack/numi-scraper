import json
import re

def make_child_friendly(text):
    """Make the question text clear and child-friendly with explicit instructions"""
    
    # Extract the initial multiplication problem
    match = re.match(r'Use properties to find the product\.\s*\n?\$?([\d]+)\s*\\cdot\s*([\d]+)\s*\\cdot\s*([\d]+)', text)
    
    if match:
        num1 = match.group(1)
        num2 = match.group(2) 
        num3 = match.group(3)
        
        # Create child-friendly version with clear instructions
        # Using explicit "Type your answer here:" prompts
        fixed_text = f"""Use properties to find the product. Fill in each blank with a number.

Start with: ${num1} \\cdot {num2} \\cdot {num3}$

Step 1: Rearrange the numbers (move {num1} to a different spot)
${num2} \\cdot$ [Type first number here] $\\cdot {num3}$

Step 2: Group two numbers together using parentheses
${num2} \\cdot ($ [Type same number here] $\\cdot {num3})$

Step 3: Multiply the numbers in parentheses first
${num2} \\cdot$ [Type the result here]

Step 4: Find the final answer
Answer = [Type final answer here]"""
        
        return fixed_text
    
    return text

def process_file():
    """Process and fix Gr6_12_E2_variations.json to be child-friendly"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            original = quiz['question_text']
            
            # Fix the formatting to be child-friendly
            fixed = make_child_friendly(original)
            
            if fixed != original:
                quiz['question_text'] = fixed
                fixed_count += 1
                print(f"Fixed question {quiz.get('question_number', '?')}")
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixed {fixed_count} questions in Gr6_12_E2_variations.json")

if __name__ == "__main__":
    process_file()
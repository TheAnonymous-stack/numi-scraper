import json
import re

def fix_latex_formatting(text):
    """Fix the LaTeX formatting in question text"""
    
    # The pattern seems to be a fill-in-the-blank multiplication problem
    # Original broken pattern: $5 \\cdot 54 \\cdot 2 = 54 \\cdot = _ \\cdot 2$ $= 54 \\cdot (= _ \\cdot 2)$ $= 54 \\cdot = _$ $= = _$=_
    
    # Extract the numbers from the beginning
    match = re.match(r'\$(\d+)\s*\\cdot\s*(\d+)\s*\\cdot\s*(\d+)', text)
    if match:
        num1 = match.group(1)
        num2 = match.group(2)
        num3 = match.group(3)
        
        # Create properly formatted question with blanks
        fixed_text = f"Use properties to find the product. ${num1} \\cdot {num2} \\cdot {num3} = {num2} \\cdot \\_ \\cdot {num3} = {num2} \\cdot (\\_ \\cdot {num3}) = {num2} \\cdot \\_ = \\_$"
        return fixed_text
    
    return text

def process_file():
    """Process the Gr6_12_E2_variations.json file"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            original = quiz['question_text']
            
            # Check if this is one of the broken patterns
            if '= _' in original or '= = _' in original:
                fixed = fix_latex_formatting(original)
                
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
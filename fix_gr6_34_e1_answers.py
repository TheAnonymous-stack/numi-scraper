import json
import re

def fix_pattern_answers(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            question_text = quiz['question_text']
            
            # Extract the numbers from the pattern
            pattern_match = re.search(r'(\d+),\s*(\d+),\s*(\d+),=_', question_text)
            if pattern_match:
                num1 = int(pattern_match.group(1))
                num2 = int(pattern_match.group(2))
                num3 = int(pattern_match.group(3))
                
                # Determine the operation and factor
                if "multiply" in question_text.lower():
                    # Check if it's multiplication
                    if num2 / num1 == num3 / num2:
                        factor = num2 // num1
                        next_num = num3 * factor
                        quiz['correct_answers'] = [str(next_num)]
                        
                        # Update solution
                        if 'solution' in quiz and len(quiz['solution']) >= 3:
                            quiz['solution'][0][1] = f"The rule is to multiply each number by {factor} to get the next number. We can see this pattern in the given numbers: ${num1} \\times {factor} = {num2}$ and ${num2} \\times {factor} = {num3}$."
                            quiz['solution'][1][1] = f"To find the missing number, multiply the last given number by {factor}: ${num3} \\times {factor} = {next_num}$"
                            quiz['solution'][2][1] = f"Therefore, the missing number is {next_num} and the complete pattern is: {num1}, {num2}, {num3}, {next_num}"
                
                elif "divide" in question_text.lower():
                    # Check if it's division
                    if num1 / num2 == num2 / num3:
                        factor = num1 // num2
                        next_num = num3 // factor
                        quiz['correct_answers'] = [str(next_num)]
                        
                        # Update solution
                        if 'solution' in quiz and len(quiz['solution']) >= 3:
                            quiz['solution'][0][1] = f"The rule is to divide each number by {factor} to get the next number. We can see this pattern in the given numbers: ${num1} \\div {factor} = {num2}$ and ${num2} \\div {factor} = {num3}$."
                            quiz['solution'][1][1] = f"To find the missing number, divide the last given number by {factor}: ${num3} \\div {factor} = {next_num}$"
                            quiz['solution'][2][1] = f"Therefore, the missing number is {next_num} and the complete pattern is: {num1}, {num2}, {num3}, {next_num}"
                
                elif "add" in question_text.lower():
                    # Check if it's addition
                    diff = num2 - num1
                    if num3 - num2 == diff:
                        next_num = num3 + diff
                        quiz['correct_answers'] = [str(next_num)]
                        
                        # Update solution
                        if 'solution' in quiz and len(quiz['solution']) >= 3:
                            quiz['solution'][0][1] = f"The rule is to add {diff} to each number to get the next number. We can see this pattern in the given numbers: ${num1} + {diff} = {num2}$ and ${num2} + {diff} = {num3}$."
                            quiz['solution'][1][1] = f"To find the missing number, add {diff} to the last given number: ${num3} + {diff} = {next_num}$"
                            quiz['solution'][2][1] = f"Therefore, the missing number is {next_num} and the complete pattern is: {num1}, {num2}, {num3}, {next_num}"
                
                elif "subtract" in question_text.lower():
                    # Check if it's subtraction
                    diff = num1 - num2
                    if num2 - num3 == diff:
                        next_num = num3 - diff
                        quiz['correct_answers'] = [str(next_num)]
                        
                        # Update solution
                        if 'solution' in quiz and len(quiz['solution']) >= 3:
                            quiz['solution'][0][1] = f"The rule is to subtract {diff} from each number to get the next number. We can see this pattern in the given numbers: ${num1} - {diff} = {num2}$ and ${num2} - {diff} = {num3}$."
                            quiz['solution'][1][1] = f"To find the missing number, subtract {diff} from the last given number: ${num3} - {diff} = {next_num}$"
                            quiz['solution'][2][1] = f"Therefore, the missing number is {next_num} and the complete pattern is: {num1}, {num2}, {num3}, {next_num}"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed {filename}")

# Process the file
fix_pattern_answers('Gr6_34_E1_variations.json')
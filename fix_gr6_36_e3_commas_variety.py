import json
import random

def fix_formatting_and_vary_answers(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Different divisor patterns to create variety
    patterns = [
        [10, 100, 1000, 10000],        # Pattern 1: multiply by 10
        [2, 4, 8, 16],                  # Pattern 2: multiply by 2
        [5, 25, 125, 625],              # Pattern 3: multiply by 5
        [10, 100, 1000, 10000],         # Pattern 4: multiply by 10
        [3, 9, 27, 81],                 # Pattern 5: multiply by 3
        [2, 8, 32, 128],                # Pattern 6: multiply by 4
        [10, 100, 1000, 10000],         # Pattern 7: multiply by 10
        [4, 16, 64, 256],               # Pattern 8: multiply by 4
        [5, 10, 20, 40],                # Pattern 9: multiply by 2 starting from 5
        [10, 100, 1000, 10000],         # Pattern 10: multiply by 10
    ]
    
    pattern_index = 0
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            question_text = quiz['question_text']
            
            # Extract the base number
            import re
            base_match = re.search(r'\$([0-9.]+) \\div\$', question_text)
            if base_match:
                base_num = base_match.group(1)
                base_float = float(base_num)
                
                # Get the pattern for this question
                divisors = patterns[pattern_index % len(patterns)]
                pattern_index += 1
                
                # Calculate the results based on the divisors
                results = [base_float / d for d in divisors]
                
                # Format results with appropriate decimal places
                result_strs = []
                for r in results:
                    if r < 0.0001:
                        result_strs.append(f"{r:.8f}".rstrip('0').rstrip('.'))
                    elif r < 0.001:
                        result_strs.append(f"{r:.7f}".rstrip('0').rstrip('.'))
                    elif r < 0.01:
                        result_strs.append(f"{r:.6f}".rstrip('0').rstrip('.'))
                    elif r < 0.1:
                        result_strs.append(f"{r:.5f}".rstrip('0').rstrip('.'))
                    else:
                        result_strs.append(f"{r:.4f}".rstrip('0').rstrip('.'))
                
                # Rebuild the question with commas between equations
                new_text = "Complete the pattern: "
                new_text += f"${base_num} \\div$ _ $= {result_strs[0]}$, "
                new_text += f"${base_num} \\div$ _ $= {result_strs[1]}$, "
                new_text += f"${base_num} \\div$ _ $= {result_strs[2]}$, "
                new_text += f"${base_num} \\div$ _ $= {result_strs[3]}$=_"
                
                quiz['question_text'] = new_text
                
                # Update correct answers
                quiz['correct_answers'] = [str(d) for d in divisors]
                
                # Update solution text to match the new pattern
                if 'solution' in quiz and len(quiz['solution']) >= 4:
                    # Determine the multiplication factor
                    if divisors == [10, 100, 1000, 10000]:
                        factor_desc = "10"
                        pattern_desc = "multiply by 10 each time"
                    elif divisors == [2, 4, 8, 16]:
                        factor_desc = "2"
                        pattern_desc = "double each time"
                    elif divisors == [5, 25, 125, 625]:
                        factor_desc = "5"
                        pattern_desc = "multiply by 5 each time"
                    elif divisors == [3, 9, 27, 81]:
                        factor_desc = "3"
                        pattern_desc = "multiply by 3 each time"
                    elif divisors == [2, 8, 32, 128]:
                        factor_desc = "4"
                        pattern_desc = "multiply by 4 each time"
                    elif divisors == [4, 16, 64, 256]:
                        factor_desc = "4"
                        pattern_desc = "multiply by 4 each time"
                    elif divisors == [5, 10, 20, 40]:
                        factor_desc = "2"
                        pattern_desc = "double each time starting from 5"
                    else:
                        factor_desc = str(divisors[1] // divisors[0])
                        pattern_desc = f"multiply by {factor_desc} each time"
                    
                    quiz['solution'][0][1] = f"Look at the first equation: ${base_num} \\div _ = {result_strs[0]}$. To find the divisor, divide ${base_num}$ by ${result_strs[0]}$, which gives us {divisors[0]}."
                    quiz['solution'][1][1] = f"Notice the pattern in the divisors: {divisors[0]}, {divisors[1]}, {divisors[2]}, {divisors[3]}. Each divisor is obtained by {pattern_desc}."
                    quiz['solution'][2][1] = f"We can verify: ${base_num} \\div {divisors[0]} = {result_strs[0]}$, ${base_num} \\div {divisors[1]} = {result_strs[1]}$, ${base_num} \\div {divisors[2]} = {result_strs[2]}$, ${base_num} \\div {divisors[3]} = {result_strs[3]}$."
                    quiz['solution'][3][1] = f"Therefore, the missing numbers are {divisors[0]}, {divisors[1]}, {divisors[2]}, and {divisors[3]}."
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Fixed formatting and varied answers in {filename}")

# Process the file
fix_formatting_and_vary_answers('Gr6_36_E3_variations.json')
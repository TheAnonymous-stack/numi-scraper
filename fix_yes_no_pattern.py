import json
import random

def fix_yes_no_pattern(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Set seed for reproducibility
    random.seed(42)
    
    for i, quiz in enumerate(data['quizzes']):
        if 'choices' in quiz and len(quiz['choices']) == 2:
            # Pattern: Yes, Yes, No, Yes, Yes, No, ...
            # Index 0,1 = Yes, 2 = No, 3,4 = Yes, 5 = No, etc.
            should_be_yes = (i % 3) != 2
            
            # Extract the two ratios from the question
            question_text = quiz['question_text']
            parts = question_text.split('.')
            if len(parts) >= 2:
                ratio1_text = parts[0].split('?')[-1].strip()
                ratio2_text = parts[1].strip()
                
                # Parse numbers from ratio texts
                import re
                nums1 = re.findall(r'\d+', ratio1_text)
                nums2 = re.findall(r'\d+', ratio2_text)
                
                if len(nums1) >= 2 and len(nums2) >= 2:
                    a1, b1 = int(nums1[0]), int(nums1[1])
                    a2, b2 = int(nums2[0]), int(nums2[1])
                    
                    # If we want "Yes", make the ratios equivalent
                    if should_be_yes:
                        # Make them equivalent by adjusting the second ratio
                        # Keep a1/b1, make a2/b2 equivalent
                        # We can multiply both parts by a factor
                        factor = random.choice([2, 3, 4, 5])
                        a2 = a1 * factor
                        b2 = b1 * factor
                        
                        # Update the question text
                        old_ratio2 = ratio2_text
                        # Find the pattern in ratio2_text
                        ratio2_parts = re.split(r'(\d+)', ratio2_text)
                        # Replace the first two numbers
                        num_count = 0
                        for j, part in enumerate(ratio2_parts):
                            if part.isdigit():
                                if num_count == 0:
                                    ratio2_parts[j] = str(a2)
                                elif num_count == 1:
                                    ratio2_parts[j] = str(b2)
                                    break
                                num_count += 1
                        
                        new_ratio2 = ''.join(ratio2_parts)
                        quiz['question_text'] = quiz['question_text'].replace(old_ratio2, new_ratio2)
                    
                    # Now check if they're actually equivalent
                    are_equivalent = (a1 * b2 == a2 * b1)
                    
                    # Randomly position Yes/No in choices
                    if random.random() < 0.5:
                        quiz['choices'] = ['Yes', 'No']
                        if are_equivalent:
                            quiz['correct_answers'] = ['A']
                        else:
                            quiz['correct_answers'] = ['B']
                    else:
                        quiz['choices'] = ['No', 'Yes']
                        if are_equivalent:
                            quiz['correct_answers'] = ['B']
                        else:
                            quiz['correct_answers'] = ['A']
                    
                    # Fix the solution to match
                    if 'solution' in quiz and len(quiz['solution']) >= 3:
                        # Update the calculation in step 3
                        calc_result = f"Calculate: ${a1} \\times {b2} = {a1*b2}$ and ${b1} \\times {a2} = {b1*a2}$. "
                        if are_equivalent:
                            calc_result += f"Since {a1*b2} equals {b1*a2}, the ratios are equivalent."
                        else:
                            calc_result += f"Since {a1*b2} does not equal {b1*a2}, the ratios are not equivalent."
                        quiz['solution'][2][1] = calc_result
                        
                        # Fix step 1 to show correct fractions
                        # Need to rebuild ratio text parts
                        ratio1_desc = ratio1_text.split(str(a1), 1)[1] if str(a1) in ratio1_text else ratio1_text
                        ratio2_desc = new_ratio2.split(str(a2), 1)[1] if str(a2) in new_ratio2 else new_ratio2 if should_be_yes else ratio2_text.split(str(a2), 1)[1] if str(a2) in ratio2_text else ratio2_text
                        
                        quiz['solution'][0][1] = f"Write the ratios as fractions: $\\frac{{{a1}}}{{{b1}}}$ ({a1}{ratio1_desc}) and $\\frac{{{a2}}}{{{b2}}}$ ({a2}{ratio2_desc})."
                        
                        # Fix step 2
                        quiz['solution'][1][1] = f"Use cross-multiplication to check if the fractions are equivalent: ${a1} \\times {b2}$ compared to ${b1} \\times {a2}$."
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Process both files
fix_yes_no_pattern('Gr6_28_E4_variations.json')
print("Fixed Gr6_28_E4_variations.json with Yes, Yes, No pattern")

fix_yes_no_pattern('Gr6_30_E1_variations.json')
print("Fixed Gr6_30_E1_variations.json with Yes, Yes, No pattern")
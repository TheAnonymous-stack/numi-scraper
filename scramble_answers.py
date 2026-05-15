import json
import random

def scramble_answers(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Set seed for reproducibility
    random.seed(42)
    
    for quiz in data['quizzes']:
        # Check if answers need to be fixed
        if 'choices' in quiz and len(quiz['choices']) == 2:
            # Determine if the ratios are actually equivalent
            question_text = quiz['question_text']
            
            # Extract the two ratios from the question
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
                    
                    # Check if ratios are equivalent using cross multiplication
                    are_equivalent = (a1 * b2 == a2 * b1)
                    
                    # Randomly decide position of Yes/No
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
                        step3 = quiz['solution'][2][1]
                        # Update the calculation in step 3
                        calc_result = f"Calculate: ${a1} \\times {b2} = {a1*b2}$ and ${b1} \\times {a2} = {b1*a2}$. "
                        if are_equivalent:
                            calc_result += f"Since {a1*b2} equals {b1*a2}, the ratios are equivalent."
                        else:
                            calc_result += f"Since {a1*b2} does not equal {b1*a2}, the ratios are not equivalent."
                        quiz['solution'][2][1] = calc_result
                        
                        # Fix step 1 to show correct fractions
                        quiz['solution'][0][1] = f"Write the ratios as fractions: $\\frac{{{a1}}}{{{b1}}}$ ({a1} {ratio1_text.split(str(a1), 1)[1]}) and $\\frac{{{a2}}}{{{b2}}}$ ({a2} {ratio2_text.split(str(a2), 1)[1]})."
                        
                        # Fix step 2
                        quiz['solution'][1][1] = f"Use cross-multiplication to check if the fractions are equivalent: ${a1} \\times {b2}$ compared to ${b1} \\times {a2}$."
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Process both files
scramble_answers('Gr6_28_E4_variations.json')
print("Scrambled answers in Gr6_28_E4_variations.json")
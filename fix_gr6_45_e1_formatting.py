import json
import re

def clean_question_text(question_text):
    """Clean up formatting issues in the question text"""
    # Fix patterns like ", , and X" -> ", and X"  
    question_text = re.sub(r', , and (\d+)', r', and \1', question_text)
    
    # Fix patterns like "X and Y and Z and ..." -> "X, Y, Z, and ..."
    # First extract the numbered list part
    lines = question_text.split('\n')
    for i, line in enumerate(lines):
        if 'numbered' in line:
            # Find the numbers part after "numbered"
            parts = line.split('numbered ')
            if len(parts) == 2:
                prefix = parts[0] + 'numbered '
                numbers_part = parts[1].rstrip('.')
                
                # Split by 'and' to get individual numbers
                numbers = [num.strip(' ,') for num in numbers_part.split(' and ') if num.strip(' ,')]
                
                # Reconstruct properly formatted list
                if len(numbers) > 1:
                    formatted_numbers = ', '.join(numbers[:-1]) + ', and ' + numbers[-1]
                else:
                    formatted_numbers = numbers[0] if numbers else numbers_part
                
                lines[i] = prefix + formatted_numbers + '.'
    
    return '\n'.join(lines)

def process_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        # Clean up the question text formatting
        quiz['question_text'] = clean_question_text(quiz['question_text'])
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Cleaned up formatting in {filename}")

# Process the file
process_file('Gr6_45_E1_variations.json')
print("Done!")
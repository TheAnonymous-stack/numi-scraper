import json
import re

def extract_info_from_backend(backend_description):
    """Extract the number of items and their values from backend description"""
    # Extract number of items and their labels
    # Pattern: "shows X color items" and "labeled A, B, C, ..."
    
    # Look for number pattern
    num_match = re.search(r'shows (\d+) \w+', backend_description)
    if not num_match:
        return None
    
    num_items = num_match.group(1)
    
    # Extract the item type (faces, balls, cards)
    type_match = re.search(r'shows \d+ \w+ (\w+)', backend_description)
    if not type_match:
        return None
    
    item_type = type_match.group(1)
    
    # Extract the numbers
    numbers_match = re.search(r'labeled ([0-9, and]+)', backend_description)
    if not numbers_match:
        return None
    
    numbers_text = numbers_match.group(1)
    # Parse the numbers - handle "A, B, C, and D" format
    numbers_text = numbers_text.replace(' and ', ', ')
    numbers = [num.strip() for num in numbers_text.split(',')]
    
    return {
        'count': num_items,
        'type': item_type,
        'numbers': numbers
    }

def process_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'backend_description' in quiz:
            # Extract information from backend description
            info = extract_info_from_backend(quiz['backend_description'])
            
            if info:
                # Extract the item type from the original question
                if 'dice face' in quiz['question_text']:
                    item_name = 'dice face'
                elif 'lottery ball' in quiz['question_text']:
                    item_name = 'lottery ball'
                elif 'trading card' in quiz['question_text']:
                    item_name = 'trading card'
                else:
                    item_name = info['type'].rstrip('s')  # Remove plural 's'
                
                # Create numbers list text
                if len(info['numbers']) > 1:
                    numbers_list = ', '.join(info['numbers'][:-1]) + ', and ' + info['numbers'][-1]
                else:
                    numbers_list = info['numbers'][0]
                
                # Update question text to include the information
                original_question = quiz['question_text']
                
                # Insert the information before the probability question
                new_question = f"There are {info['count']} {info['type']} numbered {numbers_list}.\n" + original_question
                
                quiz['question_text'] = new_question
        
        # Remove image-related fields
        if 'image_tag' in quiz:
            del quiz['image_tag']
        if 'backend_description' in quiz:
            del quiz['backend_description']
        if 'solution_image_tag' in quiz:
            del quiz['solution_image_tag']
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Processed {filename} - removed images and added item information to question text")

# Process the file
process_file('Gr6_45_E1_variations.json')
print("Done!")
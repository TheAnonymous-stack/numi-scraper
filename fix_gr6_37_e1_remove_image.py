import json

def remove_image_and_reformat(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    for quiz in data['quizzes']:
        if 'question_text' in quiz:
            # Extract the expression from the original question text
            original_text = quiz['question_text']
            
            # Look for the expression pattern
            if "This model represents the expression" in original_text:
                # Extract the expression after "expression " and before "."
                start = original_text.find("expression ") + len("expression ")
                end = original_text.find(".", start)
                if end == -1:
                    end = original_text.find("?", start)
                
                if start > len("expression ") and end > start:
                    expression = original_text[start:end].strip()
                    
                    # Create new question text
                    quiz['question_text'] = f"Which expression is equivalent to {expression}?=_"
            
            # Remove image-related fields
            if 'image_tag' in quiz:
                del quiz['image_tag']
            if 'backend_description' in quiz:
                del quiz['backend_description']
            if 'solution_image_tag' in quiz:
                del quiz['solution_image_tag']
            
            # Update solution text to remove references to "model" and "blocks"
            if 'solution' in quiz:
                for step in quiz['solution']:
                    if len(step) > 1:
                        # Replace references to "model" with "expression"
                        step[1] = step[1].replace("This model represents", "The expression is")
                        step[1] = step[1].replace("in the model", "in the expression")
                        step[1] = step[1].replace("The model shows", "The expression shows")
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Removed images and reformatted questions in {filename}")

# Process the file
remove_image_and_reformat('Gr6_37_E1_variations.json')
import json
import re

def update_gr6_46_e3_questions(data):
    """Update Gr6_46_E3 questions to include context"""
    
    for quiz in data['quizzes']:
        current_text = quiz.get('question_text', '')
        
        # Remove the =_ marker temporarily
        current_text = current_text.replace('=_', '').strip()
        
        # Add context based on the question type
        if 'from the front' in current_text.lower():
            new_text = "Look at the 3D object below made of cubes. When viewing from the front (facing the object directly), which 2D grid shows what you would see?"
        elif 'from the top' in current_text.lower():
            new_text = "Look at the 3D object below made of cubes. When viewing from the top (looking down at the object), which 2D grid shows what you would see?"
        elif 'from the side' in current_text.lower():
            new_text = "Look at the 3D object below made of cubes. When viewing from the side (looking at the object from the right), which 2D grid shows what you would see?"
        else:
            # Keep original if pattern doesn't match
            new_text = current_text
        
        # Add back the =_ marker
        quiz['question_text'] = new_text + "=_"
    
    return data

def update_gr6_48_e1_questions(data):
    """Update Gr6_48_E1 questions to include context"""
    
    for quiz in data['quizzes']:
        current_text = quiz.get('question_text', '')
        
        # Remove the =_ marker temporarily
        current_text = current_text.replace('=_', '').strip()
        
        # Add context based on the transformation type
        if 'rotation' in current_text.lower():
            new_text = "Look at the shape on the grid below. A rotation turns a shape around a point. Which image shows the shape after it has been rotated?"
        elif 'reflection' in current_text.lower():
            new_text = "Look at the shape on the grid below. A reflection flips a shape across a line (like a mirror image). Which image shows the shape after it has been reflected?"
        elif 'translation' in current_text.lower():
            new_text = "Look at the shape on the grid below. A translation slides a shape to a new position without turning or flipping. Which image shows the shape after it has been translated?"
        else:
            # For general questions, provide all context
            if 'look at this shape' in current_text.lower():
                # Determine what we're looking for from the options
                new_text = "Look at the shape on the grid below. Shapes can be transformed by rotation (turning), reflection (flipping), or translation (sliding). Which image shows the specified transformation?"
            else:
                new_text = current_text
        
        # Add back the =_ marker
        quiz['question_text'] = new_text + "=_"
    
    return data

def main():
    """Update both JSON files with contextual questions"""
    
    print("Updating question text to include context...")
    print("-" * 60)
    
    # Update Gr6_46_E3
    json_file = 'Gr6_46_E3_variations.json'
    print(f"\nProcessing {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data = update_gr6_46_e3_questions(data)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  Updated {len(data['quizzes'])} questions")
    
    # Update Gr6_48_E1
    json_file = 'Gr6_48_E1_variations.json'
    print(f"\nProcessing {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data = update_gr6_48_e1_questions(data)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  Updated {len(data['quizzes'])} questions")
    
    print("\n" + "-" * 60)
    print("Question text updated with context!")

if __name__ == "__main__":
    main()
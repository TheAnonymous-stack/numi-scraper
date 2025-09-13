import json
import re

def update_gr6_47_e1_questions(data):
    """Update Gr6_47_E1 questions with more context (positive coordinates only)"""
    
    for quiz in data['quizzes']:
        current_text = quiz.get('question_text', '')
        
        # Extract the point name
        point_match = re.search(r'point (\w+)', current_text, re.IGNORECASE)
        if point_match:
            point_name = point_match.group(1).upper()
            
            if 'x-coordinate' in current_text.lower():
                new_text = f"Look at the coordinate plane below. Point {point_name} is marked on the grid. To find the x-coordinate, look at how many units to the right of the origin (0,0) the point is located. What is the x-coordinate of point {point_name}?\nx-coordinate: ___=_"
            elif 'y-coordinate' in current_text.lower():
                new_text = f"Look at the coordinate plane below. Point {point_name} is marked on the grid. To find the y-coordinate, look at how many units above the origin (0,0) the point is located. What is the y-coordinate of point {point_name}?\ny-coordinate: ___=_"
            else:
                new_text = current_text
            
            quiz['question_text'] = new_text
    
    return data

def update_gr6_47_e2_questions(data):
    """Update Gr6_47_E2 questions with more context (positive and negative coordinates)"""
    
    for quiz in data['quizzes']:
        current_text = quiz.get('question_text', '')
        
        # Extract the point name
        point_match = re.search(r'point (\w+)', current_text, re.IGNORECASE)
        if point_match:
            point_name = point_match.group(1).upper()
            
            if 'x-coordinate' in current_text.lower():
                new_text = f"Look at the coordinate plane below with positive and negative numbers. Point {point_name} is marked on the grid. To find the x-coordinate, count how many units left (negative) or right (positive) the point is from the origin (0,0). What is the x-coordinate of point {point_name}?\nx-coordinate: ___=_"
            elif 'y-coordinate' in current_text.lower():
                new_text = f"Look at the coordinate plane below with positive and negative numbers. Point {point_name} is marked on the grid. To find the y-coordinate, count how many units below (negative) or above (positive) the point is from the origin (0,0). What is the y-coordinate of point {point_name}?\ny-coordinate: ___=_"
            else:
                new_text = current_text
            
            quiz['question_text'] = new_text
    
    return data

def main():
    """Update both JSON files with more contextual question text"""
    
    print("Adding more context to question text in JSON files...")
    print("-" * 60)
    
    # Update Gr6_47_E1
    json_file = 'Gr6_47_E1_variations.json'
    print(f"\nProcessing {json_file} (positive coordinates only)...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data = update_gr6_47_e1_questions(data)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  Updated {len(data['quizzes'])} questions with context about positive coordinates")
    except FileNotFoundError:
        print(f"  Warning: {json_file} not found")
    
    # Update Gr6_47_E2
    json_file = 'Gr6_47_E2_variations.json'
    print(f"\nProcessing {json_file} (positive and negative coordinates)...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        data = update_gr6_47_e2_questions(data)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  Updated {len(data['quizzes'])} questions with context about positive/negative coordinates")
    except FileNotFoundError:
        print(f"  Warning: {json_file} not found")
    
    print("\n" + "-" * 60)
    print("Question text updated with detailed context!")
    print("\nContext added:")
    print("  - Gr6_47_E1: Explains how to find coordinates (positive only)")
    print("  - Gr6_47_E2: Explains positive/negative coordinate system")
    print("  - Both: Clear instructions on what to look for")

if __name__ == "__main__":
    main()
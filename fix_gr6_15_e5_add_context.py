import json
import re

def fix_gr6_15_e5_json():
    """Add distance context to Gr6_15_E5 questions"""
    
    # Load the JSON file
    with open('Gr6_15_E5_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions_updated = 0
    
    for quiz in data['quizzes']:
        backend_desc = quiz.get('backend_description', '')
        question_text = quiz.get('question_text', '')
        
        # Extract distances and locations from backend description
        # Pattern: "Location1 is connected to Location2 by ... line labeled X km"
        connections = re.findall(r'(\w+) is connected to (\w+) by[^,]* labeled ([\d.]+) km', backend_desc)
        
        if len(connections) >= 2:
            # Build the new question text with context
            loc1, loc2, dist1 = connections[0]
            loc3, loc4, dist2 = connections[1]
            
            # Extract the main question (from where to where)
            main_q_match = re.search(r'how far is it from (\w+) to (\w+)\?', question_text)
            if main_q_match:
                from_loc = main_q_match.group(1)
                to_loc = main_q_match.group(2)
                
                # Create new question with context
                new_question = f"The distance from {loc1} to {loc2} is {dist1} km. "
                new_question += f"The distance from {loc3} to {loc4} is {dist2} km. "
                new_question += f"Using the paths shown, how far is it from {from_loc} to {to_loc}?\nkm=_"
                
                quiz['question_text'] = new_question
                questions_updated += 1
                print(f"Updated question {quiz['question_number']}: Added context about {dist1} km and {dist2} km")
    
    # Save the updated JSON
    with open('Gr6_15_E5_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nTotal questions updated: {questions_updated}")

if __name__ == "__main__":
    fix_gr6_15_e5_json()
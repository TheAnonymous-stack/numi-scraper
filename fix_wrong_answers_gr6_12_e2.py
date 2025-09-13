import json

def fix_wrong_answers():
    """Fix the wrong answers in questions 2_50 and 2_51"""
    
    file_path = r'C:\Users\kapil\numi-scraper\Gr6_12_E2_variations.json'
    
    print(f"Processing {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fix question 2_50: 7 × 71 × 5
    for quiz in data['quizzes']:
        if quiz.get('question_number') == '2_50':
            print(f"Fixing question 2_50: 7 × 71 × 5")
            quiz['correct_answers'] = ["7", "7", "35", "2485"]
            quiz['solution'] = [
                ["1/4", "Use properties to find $7 \\cdot 71 \\cdot 5$"],
                ["2/4", "Rearrange using commutative property: $71 \\cdot 7 \\cdot 5$"],
                ["3/4", "Group using associative property: $71 \\cdot (7 \\cdot 5) = 71 \\cdot 35$"],
                ["4/4", "Final calculation: $71 \\cdot 35 = 2485$"]
            ]
        
        # Fix question 2_51: 7 × 43 × 9  
        elif quiz.get('question_number') == '2_51':
            print(f"Fixing question 2_51: 7 × 43 × 9")
            quiz['correct_answers'] = ["7", "7", "63", "2709"]
            quiz['solution'] = [
                ["1/4", "Use properties to find $7 \\cdot 43 \\cdot 9$"],
                ["2/4", "Rearrange using commutative property: $43 \\cdot 7 \\cdot 9$"],
                ["3/4", "Group using associative property: $43 \\cdot (7 \\cdot 9) = 43 \\cdot 63$"],
                ["4/4", "Final calculation: $43 \\cdot 63 = 2709$"]
            ]
    
    # Save the fixed file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Fixed questions 2_50 and 2_51")

if __name__ == "__main__":
    fix_wrong_answers()
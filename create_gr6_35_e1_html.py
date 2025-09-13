import json
import os
import re

def extract_pattern_info(backend_description, question_text):
    """Extract pattern information from backend description"""
    # Extract the step counts
    step_counts = []
    matches = re.findall(r'step (\d+), there are (\d+) circles', backend_description.lower())
    for step, count in matches:
        step_counts.append((int(step), int(count)))
    
    # Extract which step we're asking about
    step_asked = None
    step_match = re.search(r'(\d+)(?:th|st|nd|rd) step', question_text)
    if step_match:
        step_asked = step_match.group(1)
    
    return step_counts, step_asked

def create_pattern_html(step_counts, step_asked, question_num):
    """Create HTML with shape pattern visualization"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
    <title>Grade 6 Math Exercise - Shape Patterns</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 800px;
        }}
        .question {{
            font-size: 18px;
            margin-bottom: 30px;
            font-weight: bold;
            color: #333;
        }}
        .patterns-container {{
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            flex-wrap: wrap;
            gap: 20px;
        }}
        .step-box {{
            background-color: #f9f9f9;
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            min-width: 150px;
            flex: 1;
        }}
        .step-label {{
            font-size: 14px;
            font-weight: bold;
            color: #666;
            margin-bottom: 15px;
        }}
        .dots-container {{
            margin: 15px auto;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100px;
        }}
        .dot {{
            width: 12px;
            height: 12px;
            background-color: #4CAF50;
            border-radius: 50%;
            margin: 2px;
            display: inline-block;
        }}
        .triangular-pattern {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }}
        .dot-row {{
            display: flex;
            gap: 4px;
        }}
        .count-label {{
            font-size: 16px;
            color: #333;
            margin-top: 10px;
            font-weight: bold;
        }}
        .answer-section {{
            margin-top: 30px;
            padding: 20px;
            background-color: #f0f8ff;
            border-radius: 8px;
        }}
        .answer-prompt {{
            font-size: 16px;
            margin-bottom: 15px;
            color: #333;
        }}
        .answer-input {{
            width: 80px;
            padding: 8px;
            border: 2px solid #666;
            border-radius: 4px;
            font-size: 16px;
            text-align: center;
        }}
        .hint {{
            font-size: 14px;
            color: #666;
            margin-top: 20px;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">
            Look at the steps and find the pattern.<br>
            How many dots are in the {step_asked}{'st' if step_asked == '1' else 'nd' if step_asked == '2' else 'rd' if step_asked == '3' else 'th'} step?
        </div>
        
        <div class="patterns-container">"""
    
    # Create visual patterns for the first 3 steps
    for step in range(1, 4):
        # Find count for this step
        count = 0
        for s, c in step_counts:
            if s == step:
                count = c
                break
        
        # If not found in data, calculate triangular number
        if count == 0:
            count = step * (step + 1) // 2
        
        html += f"""
            <div class="step-box">
                <div class="step-label">Step {step}</div>
                <div class="dots-container">
                    <div class="triangular-pattern">"""
        
        # Create triangular pattern of dots
        for row in range(1, step + 1):
            html += """
                        <div class="dot-row">"""
            for dot in range(row):
                html += """
                            <div class="dot"></div>"""
            html += """
                        </div>"""
        
        html += f"""
                    </div>
                </div>
                <div class="count-label">{count} dots</div>
            </div>"""
    
    html += f"""
        </div>
        
        <div class="answer-section">
            <div class="answer-prompt">
                Based on the pattern, how many dots are in Step {step_asked}?
            </div>
            <input type="text" class="answer-input" placeholder="?"> dots
        </div>
        
        <div class="hint">
            Hint: Look at how the dots increase from step to step.<br>
            This forms a triangular pattern where each step adds a new row.<br>
            Step 1: 1 dot<br>
            Step 2: 1 + 2 = 3 dots<br>
            Step 3: 1 + 2 + 3 = 6 dots<br>
            Can you continue the pattern?
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load the JSON file
    with open('Gr6_35_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create HTML directory if it doesn't exist
    os.makedirs('HTML', exist_ok=True)
    
    created_count = 0
    
    for quiz in data['quizzes']:
        question_num = quiz['question_number']
        backend_desc = quiz.get('backend_description', '')
        question_text = quiz.get('question_text', '')
        
        # Extract pattern information
        step_counts, step_asked = extract_pattern_info(backend_desc, question_text)
        
        # Default values if not found
        if not step_counts:
            step_counts = [(1, 1), (2, 3), (3, 6)]
        if not step_asked:
            step_asked = '4'
        
        # Create HTML content
        html_content = create_pattern_html(step_counts, step_asked, question_num)
        
        # Save HTML file
        filename = f'HTML/Gr6_35_E1_{question_num}.html'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        created_count += 1
        print(f"Created {filename}")
    
    print(f"\nTotal HTML files created: {created_count}")

if __name__ == "__main__":
    main()
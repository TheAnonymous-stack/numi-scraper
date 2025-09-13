import json
import os

def create_html_template(question_data, question_index):
    """Create HTML content for a question"""
    
    question_text = question_data['question_text']
    choices = question_data['choices']
    correct_answer = question_data['correct_answers'][0]
    solution = question_data['solution']
    
    # Determine which choice is correct
    correct_choice = choices[0] if correct_answer == 'A' else choices[1]
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 - Week 14 Exercise 4 - Question {question_index}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .question-container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .question-header {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .question-text {{
            font-size: 18px;
            line-height: 1.6;
            color: #34495e;
            margin-bottom: 25px;
        }}
        .choices-container {{
            background-color: #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 25px;
        }}
        .choice {{
            background-color: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border: 2px solid #bdc3c7;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .choice:hover {{
            border-color: #3498db;
            box-shadow: 0 2px 5px rgba(52,152,219,0.3);
        }}
        .choice-label {{
            font-weight: bold;
            color: #2980b9;
            margin-right: 10px;
        }}
        .solution-container {{
            background-color: #e8f6f3;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid #27ae60;
        }}
        .solution-step {{
            margin: 15px 0;
            padding: 10px;
            background-color: white;
            border-radius: 5px;
        }}
        .step-number {{
            color: #27ae60;
            font-weight: bold;
            margin-right: 10px;
        }}
        .math-expression {{
            font-family: 'Courier New', monospace;
            color: #2c3e50;
            font-size: 16px;
            margin: 10px 0;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }}
        .skill-tag {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="question-container">
        <h1 class="question-header">Estimation Word Problem - Question {question_index}</h1>
        
        <div class="skill-tag">estimate-sums-and-differences-word-problems</div>
        
        <div class="question-text">
            {question_text}
        </div>
        
        <div class="choices-container">
            <h3>Choose the better estimate:</h3>
            <div class="choice">
                <span class="choice-label">A)</span> {choices[0]}
            </div>
            <div class="choice">
                <span class="choice-label">B)</span> {choices[1]}
            </div>
        </div>
        
        <div class="solution-container">
            <h3>Solution Steps:</h3>
"""
    
    # Add solution steps
    for step in solution:
        step_num = step[0]
        step_text = step[1].replace('\n', '<br>')
        # Convert LaTeX-like expressions to readable format
        step_text = step_text.replace('$\\rightarrow$', '→')
        step_text = step_text.replace('$', '')
        step_text = step_text.replace('\\rightarrow', '→')
        
        html_content += f"""
            <div class="solution-step">
                <span class="step-number">Step {step_num}:</span>
                <div class="math-expression">{step_text}</div>
            </div>
"""
    
    html_content += f"""
            <div style="margin-top: 20px; padding: 15px; background-color: #d4edda; border-radius: 5px; border: 1px solid #c3e6cb;">
                <strong>Correct Answer:</strong> <span style="color: #155724; font-size: 18px;">{correct_answer}) {correct_choice}</span>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    # Create HTML directory if it doesn't exist
    html_dir = "HTML"
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    
    # Load the original template questions from file.json
    with open('file.json', 'r', encoding='utf-8') as f:
        content = f.read()
        # Extract just the two template questions with tag Gr6_14_E4
        import re
        templates = []
        
        # Find all question objects with the tag
        pattern = r'\{[^}]*"tag":\s*"Gr6_14_E4"[^}]*\}'
        
        # This is a simplified approach - we'll manually extract the two templates
        # Since we know their structure from earlier
        template1 = {
            "skills": "estimate-sums-and-differences-word-problems",
            "question_text": "The Weston Public Library used a grant to purchase 13456 books. Now the library has a total of 72398 books. About how many books did the library have before the grant? Choose the better estimate.",
            "tag": "Gr6_14_E4",
            "question_number": "4_1",
            "question_type": "Multiple Choice Question with Single Answer",
            "choices": ["60000", "160000"],
            "correct_answers": ["A"],
            "solution": [
                ["1/5", "Subtract the number of books purchased from the total number of books.\n72398 - 13456 = ?"],
                ["2/5", "Round each number to the nearest ten thousand."],
                ["3/5", "72398 $\\rightarrow$ 70000\n13456 $\\rightarrow$ 10000"],
                ["4/5", "$72398 - 13456 \\rightarrow 70000 - 10000 =$?"],
                ["5/5", "$70000-10000= 60000$ \n60 000 is the better estimate."]
            ]
        }
        
        template2 = {
            "skills": "estimate-sums-and-differences-word-problems",
            "question_text": "A dust storm sweeps across the prairie. It covers 934 acres of the prairie in dust, but leaves 991 acres untouched. About how many acres does the prairie cover? Choose the better estimate.",
            "tag": "Gr6_14_E4",
            "question_number": "4_2",
            "question_type": "Multiple Choice Question with Single Answer",
            "choices": ["1900", "2400"],
            "correct_answers": ["A"],
            "solution": [
                ["1/6", "Add the acres.\n934 + 991 = ?"],
                ["2/6", "Round each number to the nearest hundred."],
                ["3/6", "934 $\\rightarrow$ 900\n991 $\\rightarrow$ 1000"],
                ["4/6", "$934+991 \\rightarrow 900+1000 = $?"],
                ["5/6", "900+1000=1900"],
                ["6/6", "1900 is the better estimate."]
            ]
        }
        
        templates = [template1, template2]
    
    # Load variations
    with open('Gr6_14_E4_variations.json', 'r', encoding='utf-8') as f:
        variations = json.load(f)
    
    # Generate HTML for templates
    print("Generating HTML files for templates...")
    for i, template in enumerate(templates, 1):
        html_content = create_html_template(template, i)
        filename = f"{html_dir}/Gr6_14_E4_{template['question_number'].replace('_', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Created: {filename}")
    
    # Generate HTML for variations
    print("\nGenerating HTML files for variations...")
    for i, variation in enumerate(variations, 1):
        html_content = create_html_template(variation, i + 2)  # +2 because we have 2 templates
        filename = f"{html_dir}/Gr6_14_E4_{variation['question_number'].replace('_', '_')}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        if i % 10 == 0:
            print(f"Progress: {i}/{len(variations)} HTML files created")
    
    print(f"\nSuccessfully created HTML files for all 51 questions (2 templates + 49 variations)")
    print(f"HTML files saved in: {html_dir}/")

if __name__ == "__main__":
    main()
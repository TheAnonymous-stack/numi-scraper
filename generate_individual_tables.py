import json
import re
import os

# Load the JSON data
with open("C:/Users/kapil/numi-scraper/Gr6_55_E1_variations.json", "r") as f:
    data = json.load(f)

# Create directory for HTML files if it doesn't exist
html_dir = "C:/Users/kapil/numi-scraper/Gr6_55_E1_html"
if not os.path.exists(html_dir):
    os.makedirs(html_dir)

# Process each quiz
for quiz in data["quizzes"]:
    question_num = quiz["question_number"]
    backend_desc = quiz.get("backend_description", "")
    question_text = quiz.get("question_text", "")
    choices = quiz.get("choices", [])
    correct_answer = quiz.get("correct_answers", [""])[0]
    solution_steps = quiz.get("solution", [])
    solution_images = quiz.get("solution_image_tag", [])
    
    # Extract title
    if "titled" in backend_desc:
        parts = backend_desc.split("titled")[1].split(".")[0]
        title = parts.strip().strip('"').strip("'")
    else:
        title = f"Budget Table {question_num}"
    
    # Parse income and expenses from backend description
    income_items = []
    expenses_items = []
    
    if "Income" in backend_desc and "Expenses" in backend_desc:
        # Extract income section
        income_pattern = r"Income column[^:]*:\s*([^.]+)\."
        income_match = re.search(income_pattern, backend_desc)
        if income_match:
            income_text = income_match.group(1)
            item_matches = re.findall(r"'([^:]+):\s*\$(\d+)'", income_text)
            for item, amount in item_matches:
                item = item.strip()
                income_items.append((item, amount))
        
        # Extract expenses section
        expenses_pattern = r"Expenses column[^:]*:\s*([^.]+)\."
        expenses_match = re.search(expenses_pattern, backend_desc)
        if expenses_match:
            expenses_text = expenses_match.group(1)
            item_matches = re.findall(r"'([^:]+):\s*\$(\d+)'", expenses_text)
            for item, amount in item_matches:
                item = item.strip()
                expenses_items.append((item, amount))
    
    # Generate HTML for this question
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Question {question_num}: {title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
            max-width: 900px;
            margin: 0 auto;
        }}
        .question-container {{
            background: white;
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        h1 {{
            color: #2c5282;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .question-text {{
            font-size: 18px;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f0f4f8;
            border-left: 4px solid #4a90e2;
        }}
        .table-container {{
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            max-width: 500px;
            border-collapse: collapse;
            margin: 0 auto 20px;
        }}
        th {{
            background-color: #4a90e2;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #3a7bc8;
        }}
        td {{
            padding: 10px 12px;
            border: 1px solid #ddd;
            background-color: #fff;
        }}
        tr:nth-child(even) td {{
            background-color: #f9f9f9;
        }}
        .amount {{
            text-align: right;
            font-weight: bold;
            color: #2c5282;
        }}
        .choices-container {{
            margin: 20px 0;
            padding: 20px;
            background-color: #fafafa;
            border-radius: 5px;
        }}
        .choices-title {{
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }}
        .choice {{
            padding: 10px 15px;
            margin: 8px 0;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            cursor: pointer;
        }}
        .choice:hover {{
            background-color: #f0f4f8;
        }}
        .correct-choice {{
            background-color: #d4f4dd;
            border-color: #4caf50;
        }}
        .solution-container {{
            margin-top: 30px;
            padding: 20px;
            background-color: #fff9e6;
            border-radius: 5px;
            border: 1px solid #ffc107;
        }}
        .solution-title {{
            font-size: 20px;
            font-weight: bold;
            color: #ff6b35;
            margin-bottom: 20px;
        }}
        .solution-step {{
            margin: 15px 0;
            padding: 15px;
            background-color: white;
            border-left: 3px solid #ff6b35;
            border-radius: 3px;
        }}
        .step-number {{
            color: #ff6b35;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .solution-image {{
            margin: 10px 0;
            padding: 10px;
            background-color: #f0f4f8;
            border-radius: 4px;
            font-style: italic;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="question-container">
        <h1>Question {question_num}</h1>
        
        <div class="question-text">
            {question_text.replace(chr(10), '<br>')}
        </div>
        
        <div class="table-container">
            <h2 style="text-align: center; color: #333;">{title}</h2>
            <table>
                <thead>
                    <tr>
                        <th>Income</th>
                        <th class="amount">Amount</th>
                    </tr>
                </thead>
                <tbody>"""
    
    for item, amount in income_items:
        html_content += f"""
                    <tr>
                        <td>{item}</td>
                        <td class="amount">${amount}</td>
                    </tr>"""
    
    html_content += """
                </tbody>
            </table>
            
            <table>
                <thead>
                    <tr>
                        <th>Expenses</th>
                        <th class="amount">Amount</th>
                    </tr>
                </thead>
                <tbody>"""
    
    for item, amount in expenses_items:
        html_content += f"""
                    <tr>
                        <td>{item}</td>
                        <td class="amount">${amount}</td>
                    </tr>"""
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <div class="choices-container">
            <div class="choices-title">Choose the best answer:</div>"""
    
    # Add choices with correct answer highlighted
    choice_letters = ['A', 'B', 'C', 'D', 'E']
    for i, choice in enumerate(choices):
        if i < len(choice_letters):
            is_correct = choice_letters[i] == correct_answer
            choice_class = "choice correct-choice" if is_correct else "choice"
            html_content += f"""
            <div class="{choice_class}">
                <strong>{choice_letters[i]}.</strong> {choice}
            </div>"""
    
    html_content += """
        </div>
        
        <div class="solution-container">
            <div class="solution-title">Solution Steps</div>"""
    
    # Add solution steps
    for step in solution_steps:
        if len(step) >= 2:
            step_num = step[0]
            step_text = step[1]
            html_content += f"""
            <div class="solution-step">
                <div class="step-number">{step_num}</div>
                <div>{step_text}</div>"""
            
            # Check if there's a corresponding solution image
            for img in solution_images:
                if len(img) >= 3 and img[0] == step_num:
                    html_content += f"""
                <div class="solution-image">
                    Image: {img[2]}
                </div>"""
            
            html_content += """
            </div>"""
    
    html_content += """
        </div>
    </div>
</body>
</html>"""
    
    # Save the HTML file
    filename = f"{html_dir}/Gr6_55_E1_Q{question_num}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"Created {len(data['quizzes'])} individual HTML files in {html_dir}")
print("Each file contains:")
print("  - The question text")
print("  - The budget table with Income and Expenses")
print("  - Multiple choice answers with correct answer highlighted")
print("  - Complete solution steps")
import json
import os

def create_html_for_quiz(quiz):
    """Create clean HTML content for a quiz"""
    
    question_text = quiz.get('question_text', '')
    image_tag = quiz.get('image_tag', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    
    # Get option images
    image_choice_tags = quiz.get('image_choice_tags', [])
    correct_answer = quiz.get('correct_answers', [''])[0]
    
    # Get solution images
    solution_image_tags = quiz.get('solution_image_tag', [])
    solution_steps = quiz.get('solution', [])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tag} Question {question_number}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .question {{
            font-size: 20px;
            margin-bottom: 25px;
            color: #333;
        }}
        .main-image {{
            display: block;
            max-width: 500px;
            margin: 20px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .options {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin: 30px 0;
            flex-wrap: wrap;
        }}
        .option {{
            text-align: center;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .option:hover {{
            border-color: #4CAF50;
            transform: translateY(-2px);
        }}
        .option-label {{
            font-size: 20px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
        }}
        .option img {{
            max-width: 220px;
            height: auto;
            display: block;
        }}
        .correct {{
            background-color: #e8f5e9;
            border-color: #4CAF50;
        }}
        .solution {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }}
        .solution-title {{
            font-size: 22px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 20px;
        }}
        .solution-step {{
            margin: 20px 0;
        }}
        .step-text {{
            font-size: 16px;
            color: #555;
            margin-bottom: 10px;
        }}
        .solution-image {{
            display: block;
            max-width: 450px;
            margin: 15px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="question">{question_text}</div>
"""
    
    # Add main image
    if image_tag:
        html_content += f"""
        <img src="{image_tag}.png" alt="Question Image" class="main-image">
"""
    
    # Add option images
    if image_choice_tags:
        html_content += """
        <div class="options">
"""
        for i, option_tag in enumerate(image_choice_tags):
            option_letter = chr(65 + i)  # A, B, C
            is_correct = option_letter == correct_answer
            correct_class = ' correct' if is_correct else ''
            
            html_content += f"""
            <div class="option{correct_class}">
                <div class="option-label">Option {option_letter}</div>
                <img src="{option_tag}.png" alt="Option {option_letter}">
            </div>
"""
        html_content += """
        </div>
"""
    
    # Add solution section
    if solution_steps:
        html_content += """
        <div class="solution">
            <div class="solution-title">Solution</div>
"""
        
        # Map step numbers to images
        step_images = {}
        for img_info in solution_image_tags:
            step_num = img_info[0] if len(img_info) > 0 else ""
            img_tag = img_info[1] if len(img_info) > 1 else ""
            step_images[step_num] = img_tag
        
        for step in solution_steps:
            step_num = step[0] if len(step) > 0 else ""
            step_text = step[1] if len(step) > 1 else ""
            
            html_content += f"""
            <div class="solution-step">
                <div class="step-text">Step {step_num}: {step_text}</div>
"""
            
            # Add image if exists for this step
            if step_num in step_images:
                img_tag = step_images[step_num]
                html_content += f"""
                <img src="{img_tag}.png" alt="Step {step_num}" class="solution-image">
"""
            
            html_content += """
            </div>
"""
        
        html_content += """
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>"""
    
    return html_content

def process_json_file(json_file, output_dir):
    """Process JSON file and create HTML files"""
    
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return 0
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    count = 0
    for quiz in data['quizzes']:
        question_number = quiz.get('question_number', '')
        tag = quiz.get('tag', '')
        
        filename = f"{tag}_{question_number}.html"
        filepath = os.path.join(output_dir, filename)
        
        html_content = create_html_for_quiz(quiz)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        count += 1
    
    return count

def main():
    """Process Gr6_46_E3 and Gr6_48_E1"""
    
    exercises = [
        'Gr6_46_E3_variations.json',
        'Gr6_48_E1_variations.json'
    ]
    
    output_dir = 'HTML'
    
    print("Creating clean HTML files for Gr6_46_E3 and Gr6_48_E1...")
    print("-" * 50)
    
    for json_file in exercises:
        print(f"\nProcessing {json_file}...")
        count = process_json_file(json_file, output_dir)
        print(f"  Created {count} HTML files")
    
    print("\n" + "-" * 50)
    print("Done! Clean HTML files created.")

if __name__ == "__main__":
    main()
import json
import os

def create_html_for_quiz(quiz, exercise_name):
    """Create HTML content for a quiz with option images"""
    
    question_text = quiz.get('question_text', '')
    image_tag = quiz.get('image_tag', '')
    backend_desc = quiz.get('backend_description', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    
    # Get option images if they exist
    image_choice_tags = quiz.get('image_choice_tags', [])
    image_choice_descriptions = quiz.get('image_choice_tags_backend_description', [])
    correct_answer = quiz.get('correct_answers', [''])[0]
    
    # Get solution images if they exist
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
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .question-container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .question-text {{
            font-size: 18px;
            margin-bottom: 20px;
            color: #333;
            white-space: pre-line;
        }}
        .main-image {{
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
            display: block;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            background-color: #fafafa;
        }}
        .options-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}
        .option {{
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: white;
        }}
        .option:hover {{
            border-color: #4CAF50;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }}
        .option-label {{
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 10px;
            font-size: 20px;
        }}
        .option-image {{
            width: 100%;
            max-width: 180px;
            height: auto;
            margin: 0 auto;
            display: block;
        }}
        .solution-section {{
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
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #4CAF50;
            border-radius: 4px;
        }}
        .solution-image {{
            width: 100%;
            max-width: 350px;
            margin: 15px auto;
            display: block;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 8px;
            background-color: white;
        }}
        .correct-indicator {{
            color: #4CAF50;
            font-weight: bold;
            margin-top: 10px;
        }}
        .image-description {{
            font-style: italic;
            color: #666;
            font-size: 14px;
            margin-top: 8px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="question-container">
        <div class="question-text">{question_text}</div>
"""
    
    # Add main image if it exists
    if image_tag:
        html_content += f"""
        <img src="{image_tag}.png" alt="Question figure" class="main-image">
        <div class="image-description">{backend_desc}</div>
"""
    
    # Add option images if they exist
    if image_choice_tags:
        html_content += """
        <div class="options-container">
"""
        for i, (option_tag, option_desc) in enumerate(zip(image_choice_tags, image_choice_descriptions)):
            option_letter = chr(65 + i)  # A, B, C, etc.
            is_correct = option_letter == correct_answer
            html_content += f"""
            <div class="option">
                <div class="option-label">Option {option_letter}</div>
                <img src="{option_tag}.png" alt="Option {option_letter}" class="option-image">
                <div class="image-description">{option_desc}</div>
                {f'<div class="correct-indicator">✓ Correct Answer</div>' if is_correct else ''}
            </div>
"""
        html_content += """
        </div>
"""
    
    # Add solution section
    if solution_steps:
        html_content += """
        <div class="solution-section">
            <div class="solution-title">Solution</div>
"""
        for i, step in enumerate(solution_steps):
            step_num = step[0] if len(step) > 0 else f"{i+1}"
            step_text = step[1] if len(step) > 1 else ""
            
            html_content += f"""
            <div class="solution-step">
                <strong>Step {step_num}:</strong> {step_text}
"""
            
            # Add solution image if it exists for this step
            for img_info in solution_image_tags:
                if img_info[0] == step[0]:  # Match step number
                    img_tag = img_info[1]
                    img_desc = img_info[2] if len(img_info) > 2 else ""
                    html_content += f"""
                <img src="{img_tag}.png" alt="Solution step {step_num}" class="solution-image">
                <div class="image-description">{img_desc}</div>
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
    """Process a JSON file and create HTML files for each quiz"""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    exercise_name = os.path.basename(json_file).replace('_variations.json', '')
    
    count = 0
    for quiz in data['quizzes']:
        question_number = quiz.get('question_number', '').replace('_', '_')
        tag = quiz.get('tag', exercise_name)
        
        # Create filename
        filename = f"{tag}_{question_number}.html"
        filepath = os.path.join(output_dir, filename)
        
        # Generate HTML content
        html_content = create_html_for_quiz(quiz, exercise_name)
        
        # Write HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        count += 1
    
    return count

def main():
    """Main function to process both JSON files"""
    
    # Process Gr6_45_E4
    json_file_45 = 'Gr6_45_E4_variations.json'
    output_dir_45 = 'HTML'
    
    if os.path.exists(json_file_45):
        print(f"Processing {json_file_45}...")
        count_45 = process_json_file(json_file_45, output_dir_45)
        print(f"  Created {count_45} HTML files for Gr6_45_E4")
    else:
        print(f"Warning: {json_file_45} not found")
    
    # Process Gr6_48_E1
    json_file_48 = 'Gr6_48_E1_variations.json'
    output_dir_48 = 'HTML'
    
    if os.path.exists(json_file_48):
        print(f"Processing {json_file_48}...")
        count_48 = process_json_file(json_file_48, output_dir_48)
        print(f"  Created {count_48} HTML files for Gr6_48_E1")
    else:
        print(f"Warning: {json_file_48} not found")
    
    print("\nDone! HTML files created with option images properly referenced.")

if __name__ == "__main__":
    main()
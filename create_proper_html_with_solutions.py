import json
import os

def create_html_for_quiz(quiz, exercise_name):
    """Create HTML content for a quiz with option images and proper solution images"""
    
    question_text = quiz.get('question_text', '')
    image_tag = quiz.get('image_tag', '')
    backend_desc = quiz.get('backend_description', '')
    question_number = quiz.get('question_number', '')
    tag = quiz.get('tag', '')
    
    # Get option images if they exist (handle both naming conventions)
    image_choice_tags = quiz.get('image_choice_tags', [])
    image_choice_descriptions = quiz.get('image_choice_tags_backend_description', 
                                        quiz.get('image_choice_backend_description', []))
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
            max-width: 900px;
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
            font-size: 20px;
            margin-bottom: 25px;
            color: #333;
            white-space: pre-line;
            font-weight: 500;
        }}
        .main-image {{
            width: 100%;
            max-width: 450px;
            margin: 20px auto;
            display: block;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            background-color: #fafafa;
        }}
        .options-container {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-top: 35px;
        }}
        .option {{
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background-color: white;
        }}
        .option:hover {{
            border-color: #4CAF50;
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }}
        .option-label {{
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 15px;
            font-size: 24px;
        }}
        .option-image {{
            width: 100%;
            max-width: 200px;
            height: auto;
            margin: 0 auto;
            display: block;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 5px;
        }}
        .solution-section {{
            margin-top: 50px;
            padding-top: 35px;
            border-top: 3px solid #e0e0e0;
        }}
        .solution-title {{
            font-size: 26px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 25px;
            text-align: center;
        }}
        .solution-step {{
            margin: 25px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-left: 5px solid #4CAF50;
            border-radius: 5px;
        }}
        .step-header {{
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
            font-size: 18px;
        }}
        .step-text {{
            color: #333;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        .solution-image {{
            width: 100%;
            max-width: 400px;
            margin: 20px auto;
            display: block;
            border: 2px solid #ddd;
            border-radius: 6px;
            padding: 10px;
            background-color: white;
        }}
        .correct-indicator {{
            color: #4CAF50;
            font-weight: bold;
            margin-top: 12px;
            font-size: 16px;
        }}
        .image-description {{
            font-style: italic;
            color: #666;
            font-size: 14px;
            margin-top: 10px;
            text-align: center;
            line-height: 1.4;
        }}
        .answer-badge {{
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 14px;
            margin-left: 10px;
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
        for i, option_tag in enumerate(image_choice_tags):
            option_letter = chr(65 + i)  # A, B, C, etc.
            is_correct = option_letter == correct_answer
            option_desc = image_choice_descriptions[i] if i < len(image_choice_descriptions) else ""
            
            html_content += f"""
            <div class="option">
                <div class="option-label">
                    Option {option_letter}
                    {f'<span class="answer-badge">✓ Correct</span>' if is_correct else ''}
                </div>
                <img src="{option_tag}.png" alt="Option {option_letter}" class="option-image">
                <div class="image-description">{option_desc}</div>
            </div>
"""
        html_content += """
        </div>
"""
    
    # Add solution section with proper image mapping
    if solution_steps:
        html_content += """
        <div class="solution-section">
            <div class="solution-title">Solution Steps</div>
"""
        
        # Create a dictionary to map step numbers to images
        step_images = {}
        for img_info in solution_image_tags:
            step_num = img_info[0] if len(img_info) > 0 else ""
            img_tag = img_info[1] if len(img_info) > 1 else ""
            img_desc = img_info[2] if len(img_info) > 2 else ""
            step_images[step_num] = (img_tag, img_desc)
        
        for step in solution_steps:
            step_num = step[0] if len(step) > 0 else ""
            step_text = step[1] if len(step) > 1 else ""
            
            html_content += f"""
            <div class="solution-step">
                <div class="step-header">Step {step_num}</div>
                <div class="step-text">{step_text}</div>
"""
            
            # Add corresponding image if it exists
            if step_num in step_images:
                img_tag, img_desc = step_images[step_num]
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
    
    if not os.path.exists(json_file):
        print(f"Warning: {json_file} not found")
        return 0
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    exercise_name = os.path.basename(json_file).replace('_variations.json', '')
    
    count = 0
    for quiz in data['quizzes']:
        question_number = quiz.get('question_number', '')
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
    """Main function to process JSON files"""
    
    exercises = [
        'Gr6_45_E4_variations.json',
        'Gr6_46_E3_variations.json', 
        'Gr6_48_E1_variations.json'
    ]
    
    output_dir = 'HTML'
    
    print("Processing JSON files and creating HTML with proper solution images...")
    print("=" * 60)
    
    total_count = 0
    for json_file in exercises:
        print(f"\nProcessing {json_file}...")
        count = process_json_file(json_file, output_dir)
        if count > 0:
            print(f"  [OK] Created {count} HTML files")
            total_count += count
        else:
            print(f"  [SKIP] Skipped (file not found or no quizzes)")
    
    print("\n" + "=" * 60)
    print(f"Done! Created {total_count} HTML files total with proper solution images.")
    print(f"All files saved to: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    main()
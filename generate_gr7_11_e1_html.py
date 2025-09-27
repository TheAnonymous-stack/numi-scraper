#!/usr/bin/env python3
"""
Script to generate HTML files for Grade 7 Week 11 Exercise 1 questions.
Processes Gr7_11_E1_variations.json and creates HTML files for all questions with visual components.
"""

import json
import os
from pathlib import Path

def load_json_file(file_path):
    """Load and parse the JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_html_template(question_data):
    """Generate HTML content for a single question."""
    question_number = question_data.get('question_number', '')
    question_text = question_data.get('question_text', '').replace('\n', '<br>')
    image_choice_tags = question_data.get('image_choice_tags', [])
    image_choice_descriptions = question_data.get('image_choice_tags_backend_description', [])
    solution = question_data.get('solution', [])
    solution_image_tags = question_data.get('solution_image_tag', [])
    correct_answers = question_data.get('correct_answers', [])

    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Question {question_number}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .question {{ margin-bottom: 20px; }}
        .image-container {{ margin: 20px 0; }}
        .choices {{ display: flex; flex-wrap: wrap; gap: 20px; }}
        .choice {{ border: 2px solid #ddd; padding: 10px; cursor: pointer; }}
        .choice:hover {{ border-color: #007bff; }}
        .choice.correct {{ border-color: #28a745; background-color: #d4edda; }}
        .solution {{ margin-top: 30px; border-top: 2px solid #ccc; padding-top: 20px; }}
        .solution-step {{ margin: 15px 0; }}
        .solution-image {{ margin: 10px 0; }}
        .item {{ display: inline-block; margin: 10px; }}
    </style>
</head>
<body>
    <div class="question">
        <h2>Question {question_number}</h2>
        <p>{question_text}</p>
    </div>

"""

    # Add image choices if they exist
    if image_choice_tags:
        html_content += '    <div class="choices">\n'
        for i, (tag, description) in enumerate(zip(image_choice_tags, image_choice_descriptions)):
            choice_letter = chr(65 + i)  # A, B, C, D...
            is_correct = choice_letter in correct_answers
            correct_class = ' correct' if is_correct else ''

            html_content += f'        <div class="choice{correct_class}">\n'
            html_content += f'            <div class="item" label="{tag}">\n'
            html_content += f'                <!-- {description} -->\n'
            html_content += f'                <img src="{tag}.png" alt="Choice {choice_letter}">\n'
            html_content += f'            </div>\n'
            html_content += f'        </div>\n'
        html_content += '    </div>\n\n'

    # Add solution section
    if solution:
        html_content += '    <div class="solution">\n'
        html_content += '        <h3>Solution</h3>\n'

        for i, step in enumerate(solution):
            if len(step) >= 2:
                step_number = step[0]
                step_text = step[1].replace('\n', '<br>')

                html_content += f'        <div class="solution-step">\n'
                html_content += f'            <h4>Step {step_number}</h4>\n'
                html_content += f'            <p>{step_text}</p>\n'

                # Check if there's a corresponding solution image
                if i < len(solution_image_tags) and solution_image_tags[i]:
                    image_tag = solution_image_tags[i]
                    html_content += f'            <div class="solution-image">\n'
                    html_content += f'                <div class="item" label="{image_tag}">\n'
                    html_content += f'                    <img src="{image_tag}.png" alt="Step {step_number}">\n'
                    html_content += f'                </div>\n'
                    html_content += f'            </div>\n'

                html_content += f'        </div>\n'

        html_content += '    </div>\n'

    html_content += '</body>\n</html>'

    return html_content

def main():
    """Main function to process JSON and generate HTML files."""
    # File paths
    json_file = Path("C:/Users/kapil/numi-scraper/Gr7_11_E1_variations.json")
    html_dir = Path("C:/Users/kapil/numi-scraper/HTML")

    # Create HTML directory if it doesn't exist
    html_dir.mkdir(exist_ok=True)

    # Load JSON data
    print(f"Loading JSON file: {json_file}")
    data = load_json_file(json_file)

    questions = data.get('quizzes', [])
    print(f"Found {len(questions)} questions to process")

    # Process each question
    for i, question in enumerate(questions, 1):
        question_number = question.get('question_number', f'1_{i}')

        # Generate HTML filename following the pattern: Gr7_11_1_{question_number}.html
        # Extract the last part after underscore for the filename
        if '_' in question_number:
            q_num = question_number.split('_')[-1]
        else:
            q_num = question_number

        html_filename = f"Gr7_11_1_{q_num}.html"
        html_filepath = html_dir / html_filename

        # Generate HTML content
        html_content = generate_html_template(question)

        # Write HTML file
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"Generated: {html_filename}")

    print(f"\nSuccessfully generated {len(questions)} HTML files in {html_dir}")

if __name__ == "__main__":
    main()
import json
import os

def create_area_model_html(description, tag):
    """Generate HTML for fraction multiplication area models"""
    import re

    # Parse description to extract grid dimensions and shading info
    desc_lower = description.lower()

    # Extract grid dimensions (e.g., "4x3 grid", "5x2 grid")
    grid_match = re.search(r'(\d+)x(\d+)\s+grid', desc_lower)
    if grid_match:
        cols = int(grid_match.group(1))
        rows = int(grid_match.group(2))
    else:
        # Try alternate patterns for step images
        if 'columns' in desc_lower and 'rows' in desc_lower:
            col_match = re.search(r'(\d+)\s+(?:equal\s+)?(?:vertical\s+)?columns?', desc_lower)
            row_match = re.search(r'(\d+)\s+(?:equal\s+)?(?:horizontal\s+)?rows?', desc_lower)
            if col_match and row_match:
                cols = int(col_match.group(1))
                rows = int(row_match.group(1))
            else:
                # Try to extract from fractions mentioned
                cols, rows = 4, 3  # Default
        elif 'divided into' in desc_lower and 'columns' in desc_lower:
            col_match = re.search(r'divided into\s+(\d+)\s+(?:equal\s+)?(?:vertical\s+)?columns?', desc_lower)
            if col_match:
                cols = int(col_match.group(1))
                rows = 1  # Default for step 1 images
            else:
                cols = 4  # Default
                rows = 1
        else:
            cols, rows = 4, 3  # Default

    # Determine shading pattern
    first_shaded_cols = 0
    first_shaded_rows = 0
    double_shaded_rows = 0

    # Parse for column shading
    if 'leftmost' in desc_lower:
        col_match = re.search(r'leftmost\s+(\d+)\s+columns?', desc_lower)
        if col_match:
            first_shaded_cols = int(col_match.group(1))
        elif 'leftmost column' in desc_lower:
            first_shaded_cols = 1

    # Parse for row shading in double-shaded area
    if 'top' in desc_lower:
        # Look for "top X rows" or "top X squares"
        row_match = re.search(r'top\s+(\d+)\s+(?:rows?|squares?)', desc_lower)
        if row_match:
            double_shaded_rows = int(row_match.group(1))

    # Handle step-by-step images
    if '_step_1' in tag:
        # Step 1: Show only first fraction (vertical columns shaded)
        # For step 1, we need to extract columns from the step description
        step1_cols_match = re.search(r'leftmost\s+(\d+)\s+columns?', description.lower())
        if step1_cols_match:
            step1_shaded_cols = int(step1_cols_match.group(1))
        else:
            step1_shaded_cols = first_shaded_cols if first_shaded_cols > 0 else 1

        # Also extract total columns for step 1
        step1_total_match = re.search(r'divided into\s+(\d+)\s+(?:equal\s+)?(?:vertical\s+)?columns?', description.lower())
        if step1_total_match:
            step1_total_cols = int(step1_total_match.group(1))
        else:
            step1_total_cols = cols

        html = f'''<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="200" height="200" fill="white" stroke="black" stroke-width="2"/>'''

        cell_width = 200 / step1_total_cols
        for i in range(step1_total_cols):
            if i < step1_shaded_cols:
                html += f'''
  <rect x="{i * cell_width}" y="0" width="{cell_width}" height="200" fill="#E6D4F1" stroke="black" stroke-width="1"/>'''
            else:
                html += f'''
  <rect x="{i * cell_width}" y="0" width="{cell_width}" height="200" fill="none" stroke="black" stroke-width="1"/>'''

        html += '''
</svg>'''

    elif '_step_2' in tag:
        # Step 2: Show grid with double shading
        # Extract grid dimensions from step 2 description
        step2_grid_match = re.search(r'(\d+)\s+columns?\s+and\s+(\d+)\s+rows?', description.lower())
        if step2_grid_match:
            step2_cols = int(step2_grid_match.group(1))
            step2_rows = int(step2_grid_match.group(2))
        else:
            step2_cols = cols
            step2_rows = rows

        # Extract shaded columns from step 2 description
        step2_cols_match = re.search(r'leftmost\s+(\d+)\s+columns?\s+remain', description.lower())
        if step2_cols_match:
            step2_shaded_cols = int(step2_cols_match.group(1))
        else:
            step2_shaded_cols = first_shaded_cols if first_shaded_cols > 0 else 1

        # Extract double-shaded rows from step 2 description
        step2_rows_match = re.search(r'top\s+(\d+)\s+(?:squares?|rows?)', description.lower())
        if step2_rows_match:
            step2_double_rows = int(step2_rows_match.group(1))
        else:
            step2_double_rows = double_shaded_rows if double_shaded_rows > 0 else 1

        html = f'''<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="200" height="200" fill="white" stroke="black" stroke-width="2"/>'''

        cell_width = 200 / step2_cols
        cell_height = 200 / step2_rows

        for i in range(step2_cols):
            for j in range(step2_rows):
                x = i * cell_width
                y = j * cell_height

                if i < step2_shaded_cols:
                    # This column is shaded
                    if j < step2_double_rows:
                        # Double shaded with diagonal stripes
                        html += f'''
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="#E6D4F1" stroke="black" stroke-width="1"/>
  <pattern id="diagonalStripes_{tag}_{i}_{j}" patternUnits="userSpaceOnUse" width="4" height="4">
    <path d="M0,4 l4,-4 M0,0 l4,4" stroke="#9B7FB8" stroke-width="0.5"/>
  </pattern>
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="url(#diagonalStripes_{tag}_{i}_{j})" stroke="black" stroke-width="1"/>'''
                    else:
                        # Single shaded
                        html += f'''
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="#E6D4F1" stroke="black" stroke-width="1"/>'''
                else:
                    # Not shaded
                    html += f'''
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="none" stroke="black" stroke-width="1"/>'''

        html += '''
</svg>'''

    else:
        # Main image: Show complete grid with shading and double shading
        html = f'''<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="diagonalStripes_{tag}" patternUnits="userSpaceOnUse" width="4" height="4">
      <path d="M0,4 l4,-4 M0,0 l4,4" stroke="#9B7FB8" stroke-width="0.5"/>
    </pattern>
  </defs>
  <rect x="0" y="0" width="200" height="200" fill="white" stroke="black" stroke-width="2"/>'''

        cell_width = 200 / cols
        cell_height = 200 / rows

        for i in range(cols):
            for j in range(rows):
                x = i * cell_width
                y = j * cell_height

                if i < first_shaded_cols:
                    # This column is shaded
                    if j < double_shaded_rows:
                        # Double shaded with diagonal stripes
                        html += f'''
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="#E6D4F1" stroke="black" stroke-width="1"/>
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="url(#diagonalStripes_{tag})" stroke="black" stroke-width="1"/>'''
                    else:
                        # Single shaded
                        html += f'''
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="#E6D4F1" stroke="black" stroke-width="1"/>'''
                else:
                    # Not shaded
                    html += f'''
  <rect x="{x}" y="{y}" width="{cell_width}" height="{cell_height}" fill="none" stroke="black" stroke-width="1"/>'''

        html += '''
</svg>'''

    return html

def generate_html_files():
    # Load JSON data
    with open('C:/Users/kapil/numi-scraper/Gr7_20_E1_variations.json', 'r') as f:
        data = json.load(f)

    # Extract week and exercise numbers from filename
    week_number = "20"
    exercise_number = "1"

    # Process each question
    for question in data['quizzes']:
        question_number = question['question_number']

        # Create HTML filename
        html_filename = f"Gr7_{week_number}_E{exercise_number} {exercise_number}_{question_number}.html"
        html_path = os.path.join('C:/Users/kapil/numi-scraper', html_filename)

        # Start HTML content
        html_content = '''<!DOCTYPE html>
<html>
<head>
    <style>
        .item {
            display: inline-block;
            margin: 10px;
            padding: 10px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
'''

        # Add main image
        if 'image_tag' in question and 'backend_description' in question:
            main_svg = create_area_model_html(question['backend_description'], question['image_tag'])
            html_content += f'''    <div class="item" label="{question['image_tag']}">
{main_svg}
    </div>
'''

        # Add solution step images
        if 'solution_image_tag' in question:
            for step in question['solution_image_tag']:
                if len(step) >= 3:
                    step_tag = step[1]
                    step_description = step[2]
                    step_svg = create_area_model_html(step_description, step_tag)
                    html_content += f'''    <div class="item" label="{step_tag}">
{step_svg}
    </div>
'''

        # Close HTML
        html_content += '''</body>
</html>'''

        # Write HTML file
        with open(html_path, 'w') as f:
            f.write(html_content)

        print(f"Generated: {html_filename}")

if __name__ == "__main__":
    generate_html_files()
    print("All HTML files generated successfully!")
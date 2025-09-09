import json
import os
import re
from pathlib import Path

def create_histogram(description, tag):
    """Create a histogram visualization"""
    # Parse the description to extract histogram data
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="400" height="300" viewBox="0 0 400 300">\n'
    
    # Extract data from description
    if "histogram" in description.lower():
        # Default histogram with bars
        bars = []
        if "5 bars" in description:
            bars = [('1', 30), ('2', 45), ('3', 60), ('4', 35), ('5', 50)]
        elif "6 bars" in description:
            bars = [('1', 25), ('2', 40), ('3', 55), ('4', 45), ('5', 35), ('6', 30)]
        else:
            # Extract specific values if mentioned
            numbers = re.findall(r'\d+', description)
            if len(numbers) >= 2:
                num_bars = min(int(numbers[0]) if numbers else 4, 10)
                bars = [(str(i+1), 20 + (i * 10) % 60) for i in range(num_bars)]
            else:
                bars = [('1', 40), ('2', 60), ('3', 35), ('4', 50)]
        
        # Draw axes
        html += '<line x1="50" y1="250" x2="350" y2="250" stroke="black" stroke-width="2"/>\n'
        html += '<line x1="50" y1="50" x2="50" y2="250" stroke="black" stroke-width="2"/>\n'
        
        # Draw bars
        bar_width = 250 / len(bars)
        for i, (label, height) in enumerate(bars):
            x = 60 + i * bar_width
            bar_height = height * 2
            y = 250 - bar_height
            
            html += f'<rect x="{x}" y="{y}" width="{bar_width * 0.8}" height="{bar_height}" fill="#4A90E2"/>\n'
            html += f'<text x="{x + bar_width * 0.4}" y="270" text-anchor="middle" font-size="12">{label}</text>\n'
            html += f'<text x="{x + bar_width * 0.4}" y="{y - 5}" text-anchor="middle" font-size="10">{height}</text>\n'
        
        # Add labels
        if "episodes" in description.lower():
            html += '<text x="200" y="290" text-anchor="middle" font-size="14">Episodes</text>\n'
            html += '<text x="25" y="150" text-anchor="middle" font-size="14" transform="rotate(-90 25 150)">Frequency</text>\n'
        elif "books" in description.lower():
            html += '<text x="200" y="290" text-anchor="middle" font-size="14">Books Read</text>\n'
            html += '<text x="25" y="150" text-anchor="middle" font-size="14" transform="rotate(-90 25 150)">Students</text>\n'
        
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_number_line(description, tag):
    """Create a number line visualization"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="600" height="150" viewBox="0 0 600 150">\n'
    
    # Draw the main line
    html += '<line x1="50" y1="75" x2="550" y2="75" stroke="black" stroke-width="2"/>\n'
    
    # Determine range and increments
    if "0 to 1" in description:
        # Fractions from 0 to 1
        fractions = [(0, "0"), (0.25, "1/4"), (0.5, "1/2"), (0.75, "3/4"), (1, "1")]
        for val, label in fractions:
            x = 50 + val * 500
            html += f'<line x1="{x}" y1="65" x2="{x}" y2="85" stroke="black" stroke-width="2"/>\n'
            html += f'<text x="{x}" y="105" text-anchor="middle" font-size="14">{label}</text>\n'
    elif "negative" in description.lower():
        # Number line with negative numbers
        for i in range(-5, 6):
            x = 300 + i * 50
            html += f'<line x1="{x}" y1="65" x2="{x}" y2="85" stroke="black" stroke-width="2"/>\n'
            html += f'<text x="{x}" y="105" text-anchor="middle" font-size="14">{i}</text>\n'
    else:
        # Standard number line 0-10
        for i in range(11):
            x = 50 + i * 50
            html += f'<line x1="{x}" y1="65" x2="{x}" y2="85" stroke="black" stroke-width="2"/>\n'
            html += f'<text x="{x}" y="105" text-anchor="middle" font-size="14">{i}</text>\n'
    
    # Add any specific points mentioned
    if "point at" in description:
        point_match = re.search(r'point at ([\d./-]+)', description)
        if point_match:
            point_val = point_match.group(1)
            # Calculate position and add a dot
            try:
                if '/' in point_val:
                    num, den = point_val.split('/')
                    val = float(num) / float(den)
                else:
                    val = float(point_val)
                x = 50 + val * 50
                html += f'<circle cx="{x}" cy="75" r="5" fill="red"/>\n'
            except:
                pass
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_angle_diagram(description, tag):
    """Create an angle diagram"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="300" height="300" viewBox="0 0 300 300">\n'
    
    # Extract angle value
    angle_match = re.search(r'(\d+)\s*degree', description)
    angle = int(angle_match.group(1)) if angle_match else 45
    
    # Draw the angle
    cx, cy = 150, 150
    radius = 100
    
    # Draw the two rays
    html += f'<line x1="{cx}" y1="{cy}" x2="{cx + radius}" y2="{cy}" stroke="black" stroke-width="2"/>\n'
    
    # Calculate second ray position
    import math
    angle_rad = math.radians(angle)
    x2 = cx + radius * math.cos(angle_rad)
    y2 = cy - radius * math.sin(angle_rad)  # Negative because SVG y-axis is inverted
    
    html += f'<line x1="{cx}" y1="{cy}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="2"/>\n'
    
    # Draw the arc
    if angle <= 90:
        arc_radius = 30
        end_x = cx + arc_radius * math.cos(angle_rad)
        end_y = cy - arc_radius * math.sin(angle_rad)
        large_arc = 0
        html += f'<path d="M {cx + arc_radius} {cy} A {arc_radius} {arc_radius} 0 {large_arc} 0 {end_x} {end_y}" stroke="blue" stroke-width="2" fill="none"/>\n'
    
    # Add angle label
    label_angle = angle_rad / 2
    label_x = cx + 40 * math.cos(label_angle)
    label_y = cy - 40 * math.sin(label_angle)
    html += f'<text x="{label_x}" y="{label_y}" text-anchor="middle" font-size="16">{angle}°</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_place_value_chart(description, tag):
    """Create a place value chart"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="500" height="200" viewBox="0 0 500 200">\n'
    
    # Extract the number from description
    number_match = re.search(r'(\d+)', description)
    number = number_match.group(1) if number_match else "12345"
    
    # Determine columns needed
    num_digits = len(number)
    columns = []
    column_labels = ["Hundred Thousands", "Ten Thousands", "Thousands", "Hundreds", "Tens", "Ones"]
    
    # Use appropriate columns based on number size
    if num_digits <= 3:
        columns = column_labels[-3:]
        digits = number.zfill(3)
    elif num_digits <= 6:
        columns = column_labels[-(num_digits):]
        digits = number
    else:
        columns = column_labels
        digits = number[-6:]
    
    col_width = 400 / len(columns)
    
    # Draw table headers
    for i, col in enumerate(columns):
        x = 50 + i * col_width
        html += f'<rect x="{x}" y="30" width="{col_width}" height="40" stroke="black" fill="#f0f0f0" stroke-width="1"/>\n'
        html += f'<text x="{x + col_width/2}" y="55" text-anchor="middle" font-size="12">{col}</text>\n'
    
    # Draw digit cells
    for i, digit in enumerate(digits):
        x = 50 + i * col_width
        html += f'<rect x="{x}" y="70" width="{col_width}" height="60" stroke="black" fill="white" stroke-width="1"/>\n'
        html += f'<text x="{x + col_width/2}" y="110" text-anchor="middle" font-size="24" font-weight="bold">{digit}</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_map_visualization(description, tag):
    """Create a map with locations and distances"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="400" height="400" viewBox="0 0 400 400">\n'
    
    # Extract location names
    locations = re.findall(r'([A-Z][a-z]+)', description)
    if len(locations) >= 3:
        locations = locations[:3]
    else:
        locations = ["CityA", "CityB", "CityC"]
    
    # Position locations in a triangle
    positions = [
        (200, 100),  # Top
        (100, 250),  # Bottom left
        (300, 250)   # Bottom right
    ]
    
    # Draw connections
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            html += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="gray" stroke-width="2" stroke-dasharray="5,5"/>\n'
    
    # Draw locations
    for i, (x, y) in enumerate(positions):
        html += f'<circle cx="{x}" cy="{y}" r="30" fill="#4A90E2" stroke="black" stroke-width="2"/>\n'
        if i < len(locations):
            html += f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-size="12" fill="white">{locations[i]}</text>\n'
    
    # Add distance labels if mentioned
    distances = re.findall(r'(\d+)\s*(?:miles|km|kilometers)', description)
    if distances:
        # Add distance labels on the lines
        mid_points = [
            ((positions[0][0] + positions[1][0])/2, (positions[0][1] + positions[1][1])/2),
            ((positions[1][0] + positions[2][0])/2, (positions[1][1] + positions[2][1])/2),
            ((positions[0][0] + positions[2][0])/2, (positions[0][1] + positions[2][1])/2)
        ]
        for i, (x, y) in enumerate(mid_points[:len(distances)]):
            html += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="14" fill="black">{distances[i]} km</text>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def create_generic_shape(description, tag):
    """Create a generic geometric shape based on description"""
    html = f'<div class="item" label="{tag}">\n'
    html += '<svg width="300" height="300" viewBox="0 0 300 300">\n'
    
    if "triangle" in description.lower():
        html += '<polygon points="150,50 250,200 50,200" fill="lightblue" stroke="black" stroke-width="2"/>\n'
    elif "rectangle" in description.lower() or "square" in description.lower():
        html += '<rect x="50" y="75" width="200" height="150" fill="lightgreen" stroke="black" stroke-width="2"/>\n'
    elif "circle" in description.lower():
        html += '<circle cx="150" cy="150" r="80" fill="lightyellow" stroke="black" stroke-width="2"/>\n'
    elif "pentagon" in description.lower():
        points = "150,50 220,110 190,190 110,190 80,110"
        html += f'<polygon points="{points}" fill="lightcoral" stroke="black" stroke-width="2"/>\n'
    elif "hexagon" in description.lower():
        points = "150,50 210,85 210,145 150,180 90,145 90,85"
        html += f'<polygon points="{points}" fill="lightpink" stroke="black" stroke-width="2"/>\n'
    else:
        # Default rectangle
        html += '<rect x="75" y="75" width="150" height="150" fill="lightgray" stroke="black" stroke-width="2"/>\n'
    
    html += '</svg>\n'
    html += '</div>\n'
    return html

def generate_html_content(visual_info, question):
    """Generate HTML content based on visual information"""
    html_parts = []
    
    # Handle image_tag
    if 'image_tag' in visual_info and visual_info['image_tag']:
        tag = question.get('image_tag', 'image')
        description = visual_info['image_tag']
        
        if "histogram" in description.lower():
            html_parts.append(create_histogram(description, tag))
        elif "number line" in description.lower():
            html_parts.append(create_number_line(description, tag))
        elif "angle" in description.lower() and "degree" in description.lower():
            html_parts.append(create_angle_diagram(description, tag))
        elif "place value" in description.lower():
            html_parts.append(create_place_value_chart(description, tag))
        elif "map" in description.lower() or "locations" in description.lower():
            html_parts.append(create_map_visualization(description, tag))
        else:
            html_parts.append(create_generic_shape(description, tag))
    
    # Handle solution_image_tag
    if 'solution_image_tag' in visual_info and visual_info['solution_image_tag']:
        for step_info in visual_info['solution_image_tag']:
            if len(step_info) >= 3:
                step_num = step_info[0]
                step_tag = step_info[1]
                step_description = step_info[2]
                
                if "histogram" in step_description.lower():
                    html_parts.append(create_histogram(step_description, step_tag))
                elif "number line" in step_description.lower():
                    html_parts.append(create_number_line(step_description, step_tag))
                elif "angle" in step_description.lower():
                    html_parts.append(create_angle_diagram(step_description, step_tag))
                elif "place value" in step_description.lower():
                    html_parts.append(create_place_value_chart(step_description, step_tag))
                elif "map" in step_description.lower():
                    html_parts.append(create_map_visualization(step_description, step_tag))
                else:
                    html_parts.append(create_generic_shape(step_description, step_tag))
    
    # Handle image_choice_tags
    if 'image_choice_tags' in visual_info and visual_info['image_choice_tags']:
        tags = visual_info['image_choice_tags']
        descriptions = visual_info.get('image_choice_descriptions', [])
        
        for i, tag in enumerate(tags):
            if i < len(descriptions):
                description = descriptions[i]
                if "histogram" in description.lower():
                    html_parts.append(create_histogram(description, tag))
                elif "number line" in description.lower():
                    html_parts.append(create_number_line(description, tag))
                elif "angle" in description.lower():
                    html_parts.append(create_angle_diagram(description, tag))
                elif "place value" in description.lower():
                    html_parts.append(create_place_value_chart(description, tag))
                else:
                    html_parts.append(create_generic_shape(description, tag))
    
    # Handle shape_image_tags
    if 'shape_image_tags' in visual_info and visual_info['shape_image_tags']:
        for shape_info in visual_info['shape_image_tags']:
            if isinstance(shape_info, dict):
                tag = shape_info.get('tag', 'shape')
                description = shape_info.get('backend_description', '')
                html_parts.append(create_generic_shape(description, tag))
    
    return '\n'.join(html_parts)

def main():
    # Load the list of files to generate
    with open('gr6_files_to_generate.json', 'r') as f:
        files_to_generate = json.load(f)
    
    total_files = len(files_to_generate)
    generated_count = 0
    
    print(f"Starting generation of {total_files} HTML files...")
    
    for i, file_info in enumerate(files_to_generate):
        if i % 100 == 0:
            print(f"Progress: {i}/{total_files} files processed...")
        
        filename = file_info['filename']
        visual_info = file_info['visual_info']
        question = file_info['question']
        
        # Generate HTML content
        html_content = generate_html_content(visual_info, question)
        
        if html_content:
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated_count += 1
    
    print(f"\nCompleted! Generated {generated_count} HTML files out of {total_files} total.")

if __name__ == "__main__":
    main()
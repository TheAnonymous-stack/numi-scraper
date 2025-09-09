import json
import os
import re
from pathlib import Path

def generate_map_visualization(desc):
    """Generate HTML for map distance problems"""
    # Extract locations and distances
    locations_match = re.search(r'three locations: ([^,]+), ([^,]+), and ([^.]+)\.', desc)
    if locations_match:
        loc1, loc2, loc3 = locations_match.groups()
    else:
        # Fallback parsing
        parts = desc.split('three locations: ')[1].split('. ')[0] if 'three locations:' in desc else ""
        if parts:
            locations = parts.replace(' and ', ', ').split(', ')
            loc1, loc2, loc3 = locations[0] if len(locations) > 0 else "", locations[1] if len(locations) > 1 else "", locations[2] if len(locations) > 2 else ""
        else:
            loc1, loc2, loc3 = "Location A", "Location B", "Location C"
    
    distances = re.findall(r'(\d+\.\d+) km', desc)
    dist1 = distances[0] if len(distances) > 0 else "0.0"
    dist2 = distances[1] if len(distances) > 1 else "0.0"
    
    return f'''<div class="item" label="{{label}}">
<svg width="400" height="300" viewBox="0 0 400 300">
  <!-- Map showing {loc1.strip()}, {loc2.strip()}, and {loc3.strip()} -->
  <!-- Connection lines (pink) -->
  <line x1="50" y1="150" x2="200" y2="100" stroke="#FF69B4" stroke-width="3"/>
  <line x1="200" y1="100" x2="350" y2="150" stroke="#FF69B4" stroke-width="3"/>
  
  <!-- Location dots (blue) -->
  <circle cx="50" cy="150" r="5" fill="#4169E1"/>
  <circle cx="200" cy="100" r="5" fill="#4169E1"/>
  <circle cx="350" cy="150" r="5" fill="#4169E1"/>
  
  <!-- Location labels -->
  <text x="50" y="175" text-anchor="middle" font-size="14" font-weight="bold">{loc1.strip()}</text>
  <text x="200" y="85" text-anchor="middle" font-size="14" font-weight="bold">{loc2.strip()}</text>
  <text x="350" y="175" text-anchor="middle" font-size="14" font-weight="bold">{loc3.strip()}</text>
  
  <!-- Distance labels -->
  <text x="125" y="120" text-anchor="middle" font-size="12" fill="#FF1493">{dist1} km</text>
  <text x="275" y="120" text-anchor="middle" font-size="12" fill="#FF1493">{dist2} km</text>
</svg>
</div>
'''

def generate_fraction_rectangle(desc, label):
    """Generate HTML for fraction addition with rectangles"""
    # Extract fractions from description
    fractions = re.findall(r'(\d+)/(\d+)', desc)
    
    if len(fractions) >= 2:
        num1, den1 = fractions[0]
        num2, den2 = fractions[1]
    else:
        num1, den1 = "1", "4"
        num2, den2 = "1", "2"
    
    # Calculate rectangle widths proportionally
    width1 = int(200 * int(num1) / int(den1))
    width2 = int(200 * int(num2) / int(den2))
    
    return f'''<div class="item" label="{label}">
<svg width="400" height="200" viewBox="0 0 400 200">
  <!-- Fraction addition visualization -->
  <!-- First fraction: {num1}/{den1} -->
  <rect x="50" y="40" width="{width1}" height="30" fill="#4169E1" stroke="black" stroke-width="1"/>
  <text x="{50 + width1//2}" y="60" text-anchor="middle" font-size="14" fill="white">{num1}/{den1}</text>
  
  <!-- Plus sign -->
  <text x="30" y="90" font-size="20">+</text>
  
  <!-- Second fraction: {num2}/{den2} -->
  <rect x="50" y="100" width="{width2}" height="30" fill="#FF69B4" stroke="black" stroke-width="1"/>
  <text x="{50 + width2//2}" y="120" text-anchor="middle" font-size="14" fill="white">{num2}/{den2}</text>
  
  <!-- Division line -->
  <line x1="40" y1="140" x2="300" y2="140" stroke="black" stroke-width="2"/>
</svg>
</div>
'''

def generate_angle_visualization(desc, label):
    """Generate HTML for angle problems"""
    # Extract angle value
    angle_match = re.search(r'(\d+)°', desc)
    angle = int(angle_match.group(1)) if angle_match else 45
    
    # Determine angle type
    if angle < 90:
        angle_type = "Acute"
    elif angle == 90:
        angle_type = "Right"
    else:
        angle_type = "Obtuse"
    
    # Calculate second line position
    import math
    rad = math.radians(angle)
    x2 = 200 + 150 * math.cos(rad)
    y2 = 200 - 150 * math.sin(rad)
    
    return f'''<div class="item" label="{label}">
<svg width="400" height="400" viewBox="0 0 400 400">
  <!-- {angle_type} angle: {angle}° -->
  <line x1="200" y1="200" x2="350" y2="200" stroke="black" stroke-width="3"/>
  <line x1="200" y1="200" x2="{x2:.1f}" y2="{y2:.1f}" stroke="black" stroke-width="3"/>
  
  <!-- Angle arc -->
  <path d="M 240 200 A 40 40 0 0 0 {200 + 40*math.cos(rad):.1f} {200 - 40*math.sin(rad):.1f}" 
        stroke="blue" stroke-width="2" fill="lightblue" fill-opacity="0.3"/>
  
  <!-- Angle label -->
  <text x="{200 + 50*math.cos(rad/2):.1f}" y="{200 - 50*math.sin(rad/2):.1f}" 
        text-anchor="middle" font-size="18" font-weight="bold">{angle}°</text>
  
  <!-- Angle type label -->
  <text x="200" y="50" text-anchor="middle" font-size="16" font-style="italic">{angle_type} Angle</text>
  
  <!-- Vertex -->
  <circle cx="200" cy="200" r="3" fill="black"/>
  <text x="185" y="220" font-size="14" font-weight="bold">vertex</text>
</svg>
</div>
'''

def generate_coordinate_grid(desc, label):
    """Generate HTML for coordinate plane problems"""
    # Extract points from description
    points = re.findall(r'\((-?\d+),\s*(-?\d+)\)', desc)
    
    html = f'''<div class="item" label="{label}">
<svg width="400" height="400" viewBox="0 0 400 400">
  <!-- Coordinate grid -->
  <!-- Grid lines -->'''
    
    # Add grid lines
    for i in range(0, 401, 40):
        html += f'\n  <line x1="{i}" y1="0" x2="{i}" y2="400" stroke="#e0e0e0" stroke-width="1"/>'
        html += f'\n  <line x1="0" y1="{i}" x2="400" y2="{i}" stroke="#e0e0e0" stroke-width="1"/>'
    
    # Add axes
    html += '''
  <!-- Axes -->
  <line x1="200" y1="0" x2="200" y2="400" stroke="black" stroke-width="2"/>
  <line x1="0" y1="200" x2="400" y2="200" stroke="black" stroke-width="2"/>
  
  <!-- Origin -->
  <circle cx="200" cy="200" r="3" fill="black"/>
  <text x="210" y="220" font-size="12">O</text>'''
    
    # Add points if found
    for x, y in points[:5]:  # Limit to 5 points
        px = 200 + int(x) * 20
        py = 200 - int(y) * 20
        html += f'''
  <circle cx="{px}" cy="{py}" r="4" fill="red"/>
  <text x="{px+5}" y="{py-5}" font-size="12">({x},{y})</text>'''
    
    html += '''
</svg>
</div>
'''
    return html

def generate_default_visualization(label):
    """Generate a default placeholder visualization"""
    return f'''<div class="item" label="{label}">
<svg width="400" height="300" viewBox="0 0 400 300">
  <rect x="50" y="50" width="300" height="200" fill="#E8F4FD" stroke="#2196F3" stroke-width="2"/>
  <text x="200" y="150" text-anchor="middle" font-size="16" fill="#2196F3">Mathematical Visualization</text>
</svg>
</div>
'''

def process_json_file(json_file):
    """Process a single JSON file and generate HTML files"""
    print(f"Processing {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract exercise info from filename
    parts = json_file.stem.split('_')
    week = parts[1]
    exercise = parts[2]
    
    generated_files = []
    
    for quiz in data.get('quizzes', []):
        # Determine visualization type based on content
        if 'image_tag' in quiz:
            desc = quiz.get('backend_description', '')
            label = quiz['image_tag']
            
            # Determine type of visualization needed
            if 'map' in desc.lower() and 'km' in desc:
                html_content = generate_map_visualization(desc).replace('{label}', label)
            elif 'fraction' in desc.lower() or 'rectangle' in desc.lower() and '/' in desc:
                html_content = generate_fraction_rectangle(desc, label)
            elif 'angle' in desc.lower() or '°' in desc:
                html_content = generate_angle_visualization(desc, label)
            elif 'coordinate' in desc.lower() or 'point' in desc.lower() and '(' in desc:
                html_content = generate_coordinate_grid(desc, label)
            else:
                html_content = generate_default_visualization(label)
            
            # Get question number
            q_num = quiz['question_number'].split('_')[1]
            
            # Write HTML file
            filename = f"Gr6_{week}_{exercise} {exercise}_{q_num}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            generated_files.append(filename)
        
        # Handle solution_image_tag if present
        if 'solution_image_tag' in quiz:
            for step_info in quiz['solution_image_tag']:
                if len(step_info) >= 3:
                    step_num = step_info[0]
                    step_label = step_info[1]
                    step_desc = step_info[2]
                    
                    # Generate appropriate visualization
                    if 'fraction' in step_desc.lower() or 'rectangle' in step_desc.lower():
                        html_content = generate_fraction_rectangle(step_desc, step_label)
                    else:
                        html_content = generate_default_visualization(step_label)
                    
                    # Create step HTML file
                    q_num = quiz['question_number'].split('_')[1]
                    step_filename = f"Gr6_{week}_{exercise} {exercise}_{q_num}_step_{step_num.replace('/', '_')}.html"
                    with open(step_filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    generated_files.append(step_filename)
    
    return generated_files

# List of exercises to process
exercises_to_process = [
    "Gr6_15_E5", "Gr6_17_E1", "Gr6_1_E1", "Gr6_1_E2", "Gr6_22_E3", "Gr6_23_E1", 
    "Gr6_23_E3", "Gr6_24_E1", "Gr6_24_E3", "Gr6_26_E1", "Gr6_26_E2", "Gr6_27_E1",
    "Gr6_27_E3", "Gr6_27_E4", "Gr6_2_E2", "Gr6_2_E3", "Gr6_33_E1", "Gr6_33_E3",
    "Gr6_34_E3", "Gr6_35_E1", "Gr6_35_E4", "Gr6_36_E1", "Gr6_37_E1", "Gr6_3_E1",
    "Gr6_3_E2", "Gr6_3_E3", "Gr6_42_E2", "Gr6_42_E3", "Gr6_42_E4", "Gr6_45_E2",
    "Gr6_45_E3", "Gr6_45_E4", "Gr6_46_E1", "Gr6_46_E2", "Gr6_47_E2", "Gr6_4_E1",
    "Gr6_4_E2", "Gr6_4_E3", "Gr6_50_E1", "Gr6_51_E2", "Gr6_51_E3", "Gr6_52_E1",
    "Gr6_55_E1", "Gr6_5_E1", "Gr6_5_E2", "Gr6_5_E3", "Gr6_5_E4", "Gr6_6_E1",
    "Gr6_6_E2", "Gr6_6_E3", "Gr6_6_E4", "Gr6_7_E1", "Gr6_7_E2", "Gr6_7_E3",
    "Gr6_7_E4", "Gr6_8_E1"
]

# Process all JSON files
all_generated = []
for exercise in exercises_to_process:
    json_file = Path(f"{exercise}_variations.json")
    if json_file.exists():
        generated = process_json_file(json_file)
        all_generated.extend(generated)
        print(f"  Generated {len(generated)} HTML files for {exercise}")
    else:
        print(f"  Warning: {json_file} not found")

print(f"\nTotal files generated/updated: {len(all_generated)}")
print("Regeneration complete!")
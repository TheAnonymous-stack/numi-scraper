import json
import os
import re
import math
from pathlib import Path

def generate_spinner_visualization(sections, label):
    """Generate HTML for spinner probability problems"""
    if not sections:
        sections = 5
    
    angle_per_section = 360 / sections
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FED766", "#9B59B6", "#3498DB", "#E74C3C", "#2ECC71"]
    
    html = f'''<div class="item" label="{label}">
<svg width="300" height="300" viewBox="0 0 300 300">
  <!-- Spinner with {sections} equal sections -->'''
    
    for i in range(sections):
        start_angle = i * angle_per_section - 90
        end_angle = (i + 1) * angle_per_section - 90
        
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        x1 = 150 + 100 * math.cos(start_rad)
        y1 = 150 + 100 * math.sin(start_rad)
        x2 = 150 + 100 * math.cos(end_rad)
        y2 = 150 + 100 * math.sin(end_rad)
        
        large_arc = 1 if angle_per_section > 180 else 0
        
        html += f'''
  <path d="M 150 150 L {x1:.1f} {y1:.1f} A 100 100 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z" 
        fill="{colors[i % len(colors)]}" stroke="black" stroke-width="2"/>'''
    
    # Add center dot and arrow
    html += '''
  <!-- Center dot -->
  <circle cx="150" cy="150" r="5" fill="black"/>
  
  <!-- Spinner arrow -->
  <line x1="150" y1="150" x2="150" y2="50" stroke="black" stroke-width="3"/>
  <polygon points="150,45 145,55 155,55" fill="black"/>
</svg>
</div>
'''
    return html

def generate_dice_visualization(sides, label):
    """Generate HTML for dice probability problems"""
    if sides == 6:
        # Standard 6-sided die
        return f'''<div class="item" label="{label}">
<svg width="200" height="200" viewBox="0 0 200 200">
  <!-- 6-sided die -->
  <rect x="50" y="50" width="100" height="100" rx="10" fill="white" stroke="black" stroke-width="2"/>
  
  <!-- Dots for number 3 (example) -->
  <circle cx="70" cy="70" r="8" fill="black"/>
  <circle cx="100" cy="100" r="8" fill="black"/>
  <circle cx="130" cy="130" r="8" fill="black"/>
  
  <text x="100" y="180" text-anchor="middle" font-size="14">6-sided die</text>
</svg>
</div>
'''
    elif sides == 4:
        # Tetrahedral die
        return f'''<div class="item" label="{label}">
<svg width="200" height="200" viewBox="0 0 200 200">
  <!-- 4-sided die (tetrahedron) -->
  <polygon points="100,40 50,130 150,130" fill="white" stroke="black" stroke-width="2"/>
  <line x1="100" y1="40" x2="100" y2="130" stroke="black" stroke-width="1" stroke-dasharray="5,5"/>
  
  <!-- Number on visible face -->
  <text x="100" y="90" text-anchor="middle" font-size="20" font-weight="bold">3</text>
  
  <text x="100" y="160" text-anchor="middle" font-size="14">4-sided die</text>
</svg>
</div>
'''
    else:
        # Generic polygon die
        return generate_spinner_visualization(sides, label)

def generate_geometry_shape(shape_type, desc, label):
    """Generate HTML for geometry shapes"""
    if 'triangle' in shape_type.lower():
        # Check if it's a right triangle
        if 'right' in desc.lower():
            return f'''<div class="item" label="{label}">
<svg width="300" height="300" viewBox="0 0 300 300">
  <!-- Right triangle -->
  <polygon points="50,250 250,250 50,50" fill="lightblue" stroke="black" stroke-width="2"/>
  
  <!-- Right angle indicator -->
  <rect x="50" y="230" width="20" height="20" fill="none" stroke="black" stroke-width="1"/>
  
  <!-- Labels -->
  <text x="150" y="270" text-anchor="middle" font-size="14">base</text>
  <text x="30" y="150" text-anchor="middle" font-size="14">height</text>
  <text x="160" y="140" text-anchor="middle" font-size="14">hypotenuse</text>
</svg>
</div>
'''
        else:
            # Generic triangle
            return f'''<div class="item" label="{label}">
<svg width="300" height="300" viewBox="0 0 300 300">
  <!-- Triangle -->
  <polygon points="150,50 50,250 250,250" fill="lightgreen" stroke="black" stroke-width="2"/>
</svg>
</div>
'''
    elif 'rectangle' in shape_type.lower() or 'square' in shape_type.lower():
        return f'''<div class="item" label="{label}">
<svg width="300" height="200" viewBox="0 0 300 200">
  <!-- Rectangle -->
  <rect x="50" y="50" width="200" height="100" fill="lightyellow" stroke="black" stroke-width="2"/>
</svg>
</div>
'''
    elif 'circle' in shape_type.lower():
        return f'''<div class="item" label="{label}">
<svg width="200" height="200" viewBox="0 0 200 200">
  <!-- Circle -->
  <circle cx="100" cy="100" r="80" fill="lightpink" stroke="black" stroke-width="2"/>
</svg>
</div>
'''
    elif 'parallelogram' in shape_type.lower():
        return f'''<div class="item" label="{label}">
<svg width="300" height="200" viewBox="0 0 300 200">
  <!-- Parallelogram -->
  <polygon points="70,150 250,150 280,50 100,50" fill="lightcoral" stroke="black" stroke-width="2"/>
</svg>
</div>
'''
    else:
        # Default shape
        return generate_default_visualization(label)

def generate_number_line(desc, label):
    """Generate HTML for number line visualization"""
    # Extract range if possible
    numbers = re.findall(r'-?\d+\.?\d*', desc)
    if numbers:
        min_val = min(float(n) for n in numbers[:5])
        max_val = max(float(n) for n in numbers[:5])
    else:
        min_val, max_val = 0, 10
    
    html = f'''<div class="item" label="{label}">
<svg width="400" height="150" viewBox="0 0 400 150">
  <!-- Number line -->
  <line x1="30" y1="75" x2="370" y2="75" stroke="black" stroke-width="2"/>
  
  <!-- Arrow heads -->
  <polygon points="25,75 35,70 35,80" fill="black"/>
  <polygon points="375,75 365,70 365,80" fill="black"/>'''
    
    # Add tick marks and labels
    num_ticks = 11
    for i in range(num_ticks):
        x = 50 + (i * 30)
        val = min_val + (max_val - min_val) * i / (num_ticks - 1)
        html += f'''
  <line x1="{x}" y1="70" x2="{x}" y2="80" stroke="black" stroke-width="1"/>
  <text x="{x}" y="95" text-anchor="middle" font-size="12">{val:.1f}</text>'''
    
    html += '''
</svg>
</div>
'''
    return html

def generate_bar_graph(data_desc, label):
    """Generate HTML for bar graph visualization"""
    html = f'''<div class="item" label="{label}">
<svg width="400" height="300" viewBox="0 0 400 300">
  <!-- Bar graph -->
  <!-- Y-axis -->
  <line x1="50" y1="30" x2="50" y2="250" stroke="black" stroke-width="2"/>
  <!-- X-axis -->
  <line x1="50" y1="250" x2="350" y2="250" stroke="black" stroke-width="2"/>
  
  <!-- Sample bars -->
  <rect x="80" y="150" width="40" height="100" fill="#4ECDC4"/>
  <rect x="140" y="100" width="40" height="150" fill="#FF6B6B"/>
  <rect x="200" y="180" width="40" height="70" fill="#45B7D1"/>
  <rect x="260" y="120" width="40" height="130" fill="#FED766"/>
  
  <!-- Labels -->
  <text x="100" y="270" text-anchor="middle" font-size="12">A</text>
  <text x="160" y="270" text-anchor="middle" font-size="12">B</text>
  <text x="220" y="270" text-anchor="middle" font-size="12">C</text>
  <text x="280" y="270" text-anchor="middle" font-size="12">D</text>
</svg>
</div>
'''
    return html

def generate_fraction_circles(fractions, label):
    """Generate HTML for fraction visualization using circles"""
    html = f'''<div class="item" label="{label}">
<svg width="400" height="200" viewBox="0 0 400 200">'''
    
    x_offset = 50
    for i, (num, den) in enumerate(fractions[:3]):
        cx = x_offset + i * 120
        cy = 100
        
        # Draw circle divided into sections
        for j in range(int(den)):
            angle_start = j * 360 / int(den) - 90
            angle_end = (j + 1) * 360 / int(den) - 90
            
            start_rad = math.radians(angle_start)
            end_rad = math.radians(angle_end)
            
            x1 = cx + 40 * math.cos(start_rad)
            y1 = cy + 40 * math.sin(start_rad)
            x2 = cx + 40 * math.cos(end_rad)
            y2 = cy + 40 * math.sin(end_rad)
            
            large_arc = 0
            fill_color = "#4ECDC4" if j < int(num) else "white"
            
            html += f'''
  <path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A 40 40 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z" 
        fill="{fill_color}" stroke="black" stroke-width="1"/>'''
        
        # Add fraction label
        html += f'''
  <text x="{cx}" y="{cy + 60}" text-anchor="middle" font-size="14">{num}/{den}</text>'''
    
    html += '''
</svg>
</div>
'''
    return html

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
    
    distances = re.findall(r'(\d+\.?\d*) km', desc)
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

def generate_default_visualization(label):
    """Generate a default placeholder visualization"""
    return f'''<div class="item" label="{label}">
<svg width="400" height="300" viewBox="0 0 400 300">
  <rect x="50" y="50" width="300" height="200" fill="#E8F4FD" stroke="#2196F3" stroke-width="2"/>
  <text x="200" y="150" text-anchor="middle" font-size="16" fill="#2196F3">Mathematical Visualization</text>
</svg>
</div>
'''

def detect_visualization_type(quiz, desc):
    """Detect what type of visualization is needed based on content"""
    text = quiz.get('question_text', '').lower() + ' ' + desc.lower()
    
    if 'spinner' in text:
        # Extract number of sections
        sections_match = re.search(r'(\d+)\s+equal\s+sections', text)
        sections = int(sections_match.group(1)) if sections_match else 5
        return 'spinner', sections
    elif 'die' in text or 'dice' in text:
        # Extract number of sides
        sides_match = re.search(r'(\d+)-sided', text)
        sides = int(sides_match.group(1)) if sides_match else 6
        return 'dice', sides
    elif 'map' in desc and 'km' in desc:
        return 'map', None
    elif 'fraction' in desc and ('rectangle' in desc or 'model' in desc):
        return 'fraction_rectangle', None
    elif 'angle' in desc or '°' in desc:
        return 'angle', None
    elif 'coordinate' in text or 'point' in text and '(' in text:
        return 'coordinate', None
    elif 'triangle' in text:
        return 'triangle', None
    elif 'rectangle' in text or 'square' in text:
        return 'rectangle', None
    elif 'circle' in text:
        return 'circle', None
    elif 'parallelogram' in text:
        return 'parallelogram', None
    elif 'number line' in text:
        return 'number_line', None
    elif 'bar graph' in text or 'bar chart' in text:
        return 'bar_graph', None
    else:
        return 'default', None

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
        # Check for image_tag
        if 'image_tag' in quiz:
            desc = quiz.get('backend_description', '')
            label = quiz['image_tag']
            
            # Detect visualization type
            viz_type, param = detect_visualization_type(quiz, desc)
            
            # Generate appropriate visualization
            if viz_type == 'spinner':
                html_content = generate_spinner_visualization(param, label)
            elif viz_type == 'dice':
                html_content = generate_dice_visualization(param, label)
            elif viz_type == 'map':
                html_content = generate_map_visualization(desc).replace('{label}', label)
            elif viz_type == 'fraction_rectangle':
                html_content = generate_fraction_rectangle(desc, label)
            elif viz_type == 'number_line':
                html_content = generate_number_line(desc, label)
            elif viz_type == 'bar_graph':
                html_content = generate_bar_graph(desc, label)
            elif viz_type in ['triangle', 'rectangle', 'circle', 'parallelogram']:
                html_content = generate_geometry_shape(viz_type, desc, label)
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
                    
                    # Detect and generate appropriate visualization
                    viz_type, param = detect_visualization_type({'question_text': ''}, step_desc)
                    
                    if viz_type == 'fraction_rectangle':
                        html_content = generate_fraction_rectangle(step_desc, step_label)
                    else:
                        html_content = generate_default_visualization(step_label)
                    
                    # Create step HTML file
                    q_num = quiz['question_number'].split('_')[1]
                    step_filename = f"Gr6_{week}_{exercise} {exercise}_{q_num}_step_{step_num.replace('/', '_')}.html"
                    with open(step_filename, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    
                    generated_files.append(step_filename)
        
        # Also check for image_choice_tags
        if 'image_choice_tags' in quiz:
            tags = quiz['image_choice_tags']
            descs = quiz.get('image_choice_tags_backend_description', [])
            
            for i, tag in enumerate(tags):
                desc = descs[i] if i < len(descs) else ""
                
                # Detect and generate visualization
                viz_type, param = detect_visualization_type(quiz, desc)
                
                if viz_type == 'spinner':
                    html_content = generate_spinner_visualization(param, tag)
                elif viz_type == 'dice':
                    html_content = generate_dice_visualization(param, tag)
                else:
                    html_content = generate_default_visualization(tag)
                
                # Write HTML file
                q_num = quiz['question_number'].split('_')[1]
                choice_filename = f"Gr6_{week}_{exercise} {exercise}_{q_num}_choice_{i+1}.html"
                with open(choice_filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                generated_files.append(choice_filename)
    
    return generated_files

# Process all Grade 6 JSON files
all_json_files = list(Path('.').glob('Gr6_*_variations.json'))
print(f"Found {len(all_json_files)} Grade 6 JSON files")

total_generated = 0
for json_file in sorted(all_json_files):
    generated = process_json_file(json_file)
    total_generated += len(generated)
    if generated:
        print(f"  Generated {len(generated)} HTML files")

print(f"\nTotal HTML files generated: {total_generated}")
print("Regeneration complete!")
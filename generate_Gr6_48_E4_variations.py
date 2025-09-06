import json
import random
import copy

def load_templates():
    """Load template questions from the fixed JSON file"""
    with open('file_fixed.json', 'r') as f:
        data = json.load(f)
    return [q for q in data if q.get('tag') == 'Gr6_48_E4']

def generate_rotation_variations():
    """Generate diverse coordinate transformations for rotations"""
    variations = []
    
    # Different starting points across all quadrants
    start_points = [
        (1, 4), (2, 3), (3, 2), (4, 1), (3, 4),            # Quadrant I
        (-1, 4), (-2, 3), (-3, 2), (-4, 1), (-3, 4),       # Quadrant II
        (-1, -4), (-2, -3), (-3, -2), (-4, -1), (-3, -4),  # Quadrant III
        (1, -4), (2, -3), (3, -2), (4, -1), (3, -4),        # Quadrant IV
        (5, 0), (-5, 0), (0, 5), (0, -5),                   # On axes
        (2, 2), (-2, 2), (-2, -2), (2, -2),                 # Diagonal points
        (1, 3), (-1, 3), (-1, -3), (1, -3),                 # Other points
        (4, 2), (-4, 2), (-4, -2), (4, -2)
    ]
    
    # Rotation angles and directions
    rotations = [
        (90, 'counterclockwise'),
        (90, 'clockwise'),
        (180, 'counterclockwise'),  # 180 is same both ways
        (270, 'counterclockwise'),
        (270, 'clockwise')
    ]
    
    # Generate combinations
    used_combinations = set()
    point_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    for start in start_points:
        for angle, direction in rotations:
            combo = (start, angle, direction)
            if combo not in used_combinations and len(variations) < 50:
                used_combinations.add(combo)
                
                # Calculate result based on rotation
                x, y = start
                
                if angle == 90:
                    if direction == 'counterclockwise':
                        result = (-y, x)
                    else:  # clockwise
                        result = (y, -x)
                elif angle == 180:
                    result = (-x, -y)
                elif angle == 270:
                    if direction == 'counterclockwise':
                        result = (y, -x)
                    else:  # clockwise
                        result = (-y, x)
                
                # Ensure result is within grid bounds (-6 to 6)
                if -6 <= result[0] <= 6 and -6 <= result[1] <= 6:
                    point_name = random.choice(point_names)
                    variations.append({
                        'start': start,
                        'angle': angle,
                        'direction': direction,
                        'result': result,
                        'point_name': point_name
                    })
    
    # Add more variations if needed
    while len(variations) < 50:
        x = random.randint(-5, 5)
        y = random.randint(-5, 5)
        if x == 0 and y == 0:
            continue
            
        angle, direction = random.choice(rotations)
        combo = ((x, y), angle, direction)
        
        if combo not in used_combinations:
            used_combinations.add(combo)
            
            if angle == 90:
                if direction == 'counterclockwise':
                    result = (-y, x)
                else:
                    result = (y, -x)
            elif angle == 180:
                result = (-x, -y)
            elif angle == 270:
                if direction == 'counterclockwise':
                    result = (y, -x)
                else:
                    result = (-y, x)
                    
            if -6 <= result[0] <= 6 and -6 <= result[1] <= 6:
                point_name = random.choice(point_names)
                variations.append({
                    'start': (x, y),
                    'angle': angle,
                    'direction': direction,
                    'result': result,
                    'point_name': point_name
                })
    
    return variations[:50]  # Return exactly 50 variations

def get_quadrant(x, y):
    """Determine which quadrant a point is in"""
    if x > 0 and y > 0:
        return "I", "first quadrant"
    elif x < 0 and y > 0:
        return "II", "second quadrant"
    elif x < 0 and y < 0:
        return "III", "third quadrant"
    elif x > 0 and y < 0:
        return "IV", "fourth quadrant"
    else:
        return "axis", "on an axis"

def create_variation(template, variation_data, variation_num):
    """Create a single variation from template and variation data"""
    new_q = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    new_q['question_number'] = f"{template_num}_{variation_num}"
    
    # Update question text
    start_x, start_y = variation_data['start']
    point_name = variation_data['point_name']
    angle = variation_data['angle']
    direction = variation_data['direction']
    
    # Use degree symbol
    new_q['question_text'] = f"The point {point_name}({start_x},{start_y}) is rotated {angle}° {direction} around the origin. What are the coordinates of the resulting point, {point_name}'= (___, ___)"
    
    # Update correct answers
    result_x, result_y = variation_data['result']
    new_q['correct_answers'] = [str(result_x), str(result_y)]
    
    # Update image tag
    new_q['image_tag'] = f"Gr6_48_4_{variation_num}"
    
    # Update backend description
    start_quad_roman, start_quad_desc = get_quadrant(start_x, start_y)
    
    new_q['backend_description'] = f"This image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. A green point labeled '{point_name}' is plotted at ({start_x},{start_y}) in the {start_quad_desc}."
    
    # Update solution image tags
    result_quad_roman, result_quad_desc = get_quadrant(result_x, result_y)
    
    # Determine arrow description based on rotation
    if angle == 90:
        if direction == 'counterclockwise':
            arrow_desc = "a red curved arrow starting at the positive x-axis and ending at the positive y-axis, indicating a 90-degree counterclockwise rotation"
        else:
            arrow_desc = "a red curved arrow starting at the positive x-axis and ending at the negative y-axis, indicating a 90-degree clockwise rotation"
    elif angle == 180:
        arrow_desc = "a red curved arrow showing a 180-degree rotation"
    elif angle == 270:
        if direction == 'counterclockwise':
            arrow_desc = "a red curved arrow showing a 270-degree counterclockwise rotation"
        else:
            arrow_desc = "a red curved arrow showing a 270-degree clockwise rotation"
    
    new_q['solution_image_tag'] = [
        [
            "1/3",
            f"Gr6_48_4_{variation_num}_step_1",
            f"The image shows a coordinate plane with {arrow_desc} centered at the origin."
        ],
        [
            "2/3",
            f"Gr6_48_4_{variation_num}_step_2",
            f"This image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. A green point labeled '{point_name}' is plotted at ({start_x},{start_y}) in the {start_quad_desc}"
        ],
        [
            "3/3",
            f"Gr6_48_4_{variation_num}_step_3",
            f"The image shows a coordinate plane with two labeled points, {point_name} (plotted at ({start_x},{start_y})) and {point_name}' (plotted at ({result_x},{result_y})), and shaded right-angled triangles connecting each point to the origin. The origin is marked with a black dot, indicating a {angle}-degree {direction} rotation from {point_name} to {point_name}' about the origin."
        ]
    ]
    
    # Update solution text
    fraction_map = {90: "1/4", 180: "1/2", 270: "3/4"}
    fraction = fraction_map[angle]
    
    # Determine quadrant movement description
    if start_quad_roman != "axis" and result_quad_roman != "axis":
        if start_quad_roman == result_quad_roman:
            movement = f"The point stays in Quadrant {start_quad_roman}."
        else:
            movement = f"The point will move from Quadrant {start_quad_roman} to Quadrant {result_quad_roman}."
    else:
        movement = "The point moves to a new position."
    
    new_q['solution'] = [
        [
            "1/4",
            f"{angle}° is $\\frac{{{fraction.split('/')[0]}}}{{{fraction.split('/')[1]}}}$ of a full turn. The rotation will turn the point $\\frac{{{fraction.split('/')[0]}}}{{{fraction.split('/')[1]}}}$ of a full turn in the {direction} direction."
        ],
        [
            "2/4",
            f"Start with the point {point_name}({start_x},{start_y})."
        ],
        [
            "3/4",
            f"Rotate the point {angle}° {direction} around the origin. {movement} To find the exact location, imagine (0, 0) and {point_name} forming opposite corners of a box. Rotate the box, keeping the (0, 0) corner fixed."
        ],
        [
            "4/4",
            f"{point_name}' has coordinates ({result_x},{result_y})."
        ]
    ]
    
    return new_q

def main():
    """Generate all variations for Gr6_48_E4"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_48_E4")
        return
    
    # Use the first (and only) template
    template = templates[0]
    
    # Generate variation data
    variation_data = generate_rotation_variations()
    
    # Create all variations
    variations = []
    for i, var_data in enumerate(variation_data, start=2):  # Start from 2 since template is 1
        variation = create_variation(template, var_data, i)
        variations.append(variation)
    
    # Save variations to JSON file
    output_file = 'Gr6_48_E4_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_48_E4")
    print(f"Saved to {output_file}")
    print(f"Total questions (including template): {len(variations) + 1}")

if __name__ == "__main__":
    main()
import json
import random
import copy

def load_templates():
    """Load template questions from the fixed JSON file"""
    with open('file_fixed.json', 'r') as f:
        data = json.load(f)
    return [q for q in data if q.get('tag') == 'Gr6_48_E3']

def generate_reflection_variations():
    """Generate diverse coordinate transformations for reflections"""
    variations = []
    
    # Different starting points across all quadrants
    start_points = [
        (1, -3), (2, -4), (3, -2), (4, -5), (5, -1),        # Quadrant IV
        (-2, -3), (-3, -4), (-4, -2), (-5, -3), (-1, -5),  # Quadrant III
        (2, 3), (3, 4), (4, 2), (5, 3), (1, 5),             # Quadrant I
        (-2, 3), (-3, 4), (-4, 2), (-5, 3), (-1, 5),       # Quadrant II
        (0, -3), (0, 3), (3, 0), (-3, 0),                   # On axes
        (1, 1), (-1, -1), (2, 2), (-2, -2),                 # Diagonal points
        (1, -1), (-1, 1), (2, -2), (-2, 2)                  # Other diagonal
    ]
    
    # Reflection types
    reflection_types = ['x-axis', 'y-axis']
    
    # Generate combinations
    used_combinations = set()
    point_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    for start in start_points:
        for reflection in reflection_types:
            combo = (start, reflection)
            if combo not in used_combinations and len(variations) < 50:
                used_combinations.add(combo)
                
                # Calculate result
                x, y = start
                if reflection == 'x-axis':
                    result = (x, -y)
                else:  # y-axis
                    result = (-x, y)
                
                # Ensure result is within grid bounds (-6 to 6)
                if -6 <= result[0] <= 6 and -6 <= result[1] <= 6:
                    point_name = random.choice(point_names)
                    variations.append({
                        'start': start,
                        'reflection': reflection,
                        'result': result,
                        'point_name': point_name
                    })
    
    # Add more variations with different coordinates if needed
    while len(variations) < 50:
        x = random.randint(-6, 6)
        y = random.randint(-6, 6)
        if y == 0 and reflection == 'x-axis':  # Skip points on x-axis for x-axis reflection
            continue
        if x == 0 and reflection == 'y-axis':  # Skip points on y-axis for y-axis reflection
            continue
            
        reflection = random.choice(reflection_types)
        combo = ((x, y), reflection)
        
        if combo not in used_combinations:
            used_combinations.add(combo)
            
            if reflection == 'x-axis':
                result = (x, -y)
            else:
                result = (-x, y)
                
            point_name = random.choice(point_names)
            variations.append({
                'start': (x, y),
                'reflection': reflection,
                'result': result,
                'point_name': point_name
            })
    
    return variations[:50]  # Return exactly 50 variations

def create_variation(template, variation_data, variation_num):
    """Create a single variation from template and variation data"""
    new_q = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    new_q['question_number'] = f"{template_num}_{variation_num}"
    
    # Update question text
    start_x, start_y = variation_data['start']
    point_name = variation_data['point_name']
    reflection = variation_data['reflection']
    new_q['question_text'] = f"The point {point_name}({start_x},{start_y}) is reflected over the {reflection}. What are the coordinates of the resulting point, {point_name}' = (___, ___)"
    
    # Update correct answers
    result_x, result_y = variation_data['result']
    new_q['correct_answers'] = [str(result_x), str(result_y)]
    
    # Update image tag
    new_q['image_tag'] = f"Gr6_48_3_{variation_num}"
    
    # Update backend description
    quadrant_map = {
        (True, True): "first quadrant",
        (False, True): "second quadrant",
        (False, False): "third quadrant",
        (True, False): "fourth quadrant"
    }
    
    start_quadrant = quadrant_map.get((start_x > 0, start_y > 0), "on an axis")
    
    if reflection == 'x-axis':
        axis_color = "red"
        axis_description = "A red horizontal line is drawn along the x-axis, highlighting it."
    else:
        axis_color = "blue"
        axis_description = "A blue vertical line is drawn along the y-axis, highlighting it."
    
    new_q['backend_description'] = f"This image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. {axis_description} A green point labeled '{point_name}' is plotted at ({start_x},{start_y}) in the {start_quadrant}."
    
    # Update solution image tags
    result_quadrant = quadrant_map.get((result_x > 0, result_y > 0), "on an axis")
    
    new_q['solution_image_tag'] = [
        [
            "1/3",
            f"Gr6_48_3_{variation_num}_step_1",
            f"This image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. {axis_description} A green point labeled '{point_name}' is plotted at ({start_x},{start_y}) in the {start_quadrant}."
        ],
        [
            "2/3",
            f"Gr6_48_3_{variation_num}_step_2",
            f"The image shows a coordinate plane with both the x-axis and y-axis labeled. The grid ranges from -6 to 6 on both axes. {axis_description} A green point labeled '{point_name}' is plotted at ({start_x},{start_y}) in the {start_quadrant}; a pink point labeled '{point_name}'' is plotted at ({result_x},{result_y}) in the {result_quadrant}, showing a reflection over the {reflection}."
        ]
    ]
    
    # Update solution text
    if reflection == 'x-axis':
        distance_from = abs(start_y)
        distance_desc = f"{distance_from} units {'below' if start_y < 0 else 'above'} the x-axis"
        result_desc = f"{distance_from} units {'above' if start_y < 0 else 'below'} the x-axis"
    else:
        distance_from = abs(start_x)
        distance_desc = f"{distance_from} units {'to the left of' if start_x < 0 else 'to the right of'} the y-axis"
        result_desc = f"{distance_from} units {'to the right of' if start_x < 0 else 'to the left of'} the y-axis"
    
    new_q['solution'] = [
        [
            "1/3",
            f"Start with the point {point_name}({start_x},{start_y}) and the {reflection}."
        ],
        [
            "2/3",
            f"Reflect the point over the line."
        ],
        [
            "3/3",
            f"Since {point_name} is {distance_desc}, {point_name}' is {result_desc}. {point_name}' has coordinates ({result_x},{result_y})."
        ]
    ]
    
    return new_q

def main():
    """Generate all variations for Gr6_48_E3"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_48_E3")
        return
    
    # Use the first (and only) template
    template = templates[0]
    
    # Generate variation data
    variation_data = generate_reflection_variations()
    
    # Create all variations
    variations = []
    for i, var_data in enumerate(variation_data, start=2):  # Start from 2 since template is 1
        variation = create_variation(template, var_data, i)
        variations.append(variation)
    
    # Save variations to JSON file
    output_file = 'Gr6_48_E3_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_48_E3")
    print(f"Saved to {output_file}")
    print(f"Total questions (including template): {len(variations) + 1}")

if __name__ == "__main__":
    main()
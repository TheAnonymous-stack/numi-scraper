import json
import random
import copy

def load_templates():
    """Load template questions from the templates file."""
    with open('templates.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # Filter for Gr6_47_E2 templates
    templates = [q for q in all_questions if q.get('tag') == 'Gr6_47_E2']
    return templates

def generate_variations():
    """Generate 51 total versions including templates for Gr6_47_E2."""
    templates = load_templates()
    
    # We have 2 templates, need 49 more variations
    variations = []
    
    # Generate coordinate variations (positive and negative numbers)
    coordinate_variations = []
    
    # Generate diverse coordinates for points with positive and negative values
    for i in range(49):
        # Generate random points with diverse coordinates
        point_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        # Select 4 random point names for a more complex coordinate plane
        selected_names = random.sample(point_names, 4)
        
        # Generate coordinates (positive and negative, -10 to 10 range)
        coords = []
        for _ in range(4):
            x = random.randint(-10, 10)
            y = random.randint(-10, 10)
            # Avoid origin
            while x == 0 or y == 0:
                x = random.randint(-10, 10)
                y = random.randint(-10, 10)
            coords.append((x, y))
        
        # Ensure all coordinates are different
        while len(set(coords)) < 4:
            coords = []
            for _ in range(4):
                x = random.randint(-10, 10)
                y = random.randint(-10, 10)
                while x == 0 or y == 0:
                    x = random.randint(-10, 10)
                    y = random.randint(-10, 10)
                coords.append((x, y))
        
        # Randomly choose which point and coordinate to ask about
        target_idx = random.randint(0, 3)
        target_point = selected_names[target_idx]
        target_coord = coords[target_idx]
        
        if i % 2 == 0:  # Ask for x-coordinate
            question_text = f"What is the x-coordinate of point {target_point}?\nx-coordinate: ___"
            correct_answer = str(target_coord[0])
            axis_type = "x"
            solution_direction = "down" if target_coord[1] > 0 else "up"
            if target_coord[0] > 0:
                axis_position = f"{abs(target_coord[0])} units to the right of"
                qualifier = ""
            else:
                axis_position = f"{abs(target_coord[0])} units to the left of"
                qualifier = " All x-coordinates to the left of the origin are negative."
        else:  # Ask for y-coordinate
            question_text = f"What is the y-coordinate of point {target_point}?\ny-coordinate: ___"
            correct_answer = str(target_coord[1])
            axis_type = "y"
            solution_direction = "right" if target_coord[0] < 0 else "left"
            if target_coord[1] > 0:
                axis_position = f"{abs(target_coord[1])} units above"
                qualifier = ""
            else:
                axis_position = f"{abs(target_coord[1])} units below"
                qualifier = " All y-coordinates below the origin are negative."
        
        coordinate_variations.append({
            "question_text": question_text,
            "points": list(zip(selected_names, coords)),
            "target_point": target_point,
            "target_coord": target_coord,
            "correct_answer": correct_answer,
            "axis_type": axis_type,
            "solution_direction": solution_direction,
            "axis_position": axis_position,
            "qualifier": qualifier
        })
    
    # Generate variations
    variation_num = 3  # Start from 3 since we have templates 1 and 2
    
    for var_data in coordinate_variations:
        # Randomly select a template
        template = random.choice(templates)
        template_num = template['question_number'].split('_')[0]
        
        variation = copy.deepcopy(template)
        variation['question_number'] = f"{template_num}_{variation_num}"
        variation['question_text'] = var_data['question_text']
        variation['correct_answers'] = [var_data['correct_answer']]
        
        # Update image tag
        if 'image_tag' in variation:
            variation['image_tag'] = f"Gr6_47_{template_num}_{variation_num}"
        
        # Update backend description
        colors = ["purple", "pink", "blue", "green", "yellow", "orange", "red", "cyan"]
        selected_colors = random.sample(colors, 4)
        
        desc_parts = ["This image shows a coordinate plane with x-axis is labeled 'x' and the y-axis is labeled 'y'."]
        for i, (name, coord) in enumerate(var_data['points']):
            desc_parts.append(f"Point {name} is labeled '{name}' with a {selected_colors[i]} dot and is located at the point {coord}.")
        
        variation['backend_description'] = " ".join(desc_parts)
        
        # Update solution
        variation['solution'] = [
            ["1/3", f"Start at point {var_data['target_point']} and move {var_data['solution_direction']} until you reach the {var_data['axis_type']}-axis."],
            ["2/3", f"This position on the {var_data['axis_type']}-axis is {var_data['axis_position']} the origin.{var_data['qualifier']}"],
            ["3/3", f"So, the {var_data['axis_type']}-coordinate of point {var_data['target_point']} is {var_data['correct_answer']}."]
        ]
        
        # Update solution image tag
        if 'solution_image_tag' in variation:
            new_tag = f"Gr6_47_{template_num}_{variation_num}_step_1"
            
            line_type = "horizontal" if var_data['axis_type'] == 'y' else "vertical"
            end_point = f"(0, {var_data['target_coord'][1]})" if var_data['axis_type'] == 'y' else f"({var_data['target_coord'][0]}, 0)"
            
            # Build description with faded points
            desc_parts = ["This image shows a coordinate plane with x-axis is labeled 'x' and the y-axis is labeled 'y'."]
            for i, (name, coord) in enumerate(var_data['points']):
                if name == var_data['target_point']:
                    desc_parts.append(f"Point {name} is labeled '{name}' with a {selected_colors[i]} dot and is located at the point {coord}.")
                else:
                    desc_parts.append(f"Point {name} is faded out, labeled '{name}' and is located at the point {coord}.")
            desc_parts.append(f"There is a dashed red {line_type} line connecting point {var_data['target_point']} to the {var_data['axis_type']}-axis, ending at the point {end_point}.")
            
            variation['solution_image_tag'][0][1] = new_tag
            variation['solution_image_tag'][0][2] = " ".join(desc_parts)
        
        variations.append(variation)
        variation_num += 1
    
    return variations

def main():
    """Main function to generate and save variations."""
    variations = generate_variations()
    
    # Save to JSON file
    output_file = 'Gr6_47_E2_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_47_E2")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
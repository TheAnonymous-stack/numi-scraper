import json
import random
import copy

def load_templates():
    """Load template questions from the templates file."""
    with open('templates.json', 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    # Filter for Gr6_48_E1 templates
    templates = [q for q in all_questions if q.get('tag') == 'Gr6_48_E1']
    return templates

def generate_variations():
    """Generate 51 total versions including templates for Gr6_48_E1."""
    templates = load_templates()
    
    # We have 3 templates, need 48 more variations
    variations = []
    
    # Shape transformations: reflection, rotation, translation
    shapes = [
        {"name": "triangle", "color": "blue", "description": "triangle"},
        {"name": "square", "color": "red", "description": "square"},
        {"name": "rectangle", "color": "green", "description": "rectangle"},
        {"name": "trapezoid", "color": "purple", "description": "trapezoid"},
        {"name": "parallelogram", "color": "orange", "description": "parallelogram"},
        {"name": "rhombus", "color": "yellow", "description": "rhombus"},
        {"name": "pentagon", "color": "pink", "description": "pentagon"},
        {"name": "hexagon", "color": "cyan", "description": "hexagon"},
        {"name": "L-shape", "color": "brown", "description": "L-shaped figure"},
        {"name": "T-shape", "color": "gray", "description": "T-shaped figure"},
        {"name": "arrow", "color": "magenta", "description": "arrow shape"},
        {"name": "cross", "color": "teal", "description": "cross shape"}
    ]
    
    transformations = ["reflection", "rotation", "translation"]
    
    # Grid positions for original shape
    positions = [
        "top-left corner", "top-right corner", "bottom-left corner", "bottom-right corner",
        "center", "left side", "right side", "top", "bottom"
    ]
    
    variation_num = 4  # Start from 4 since we have templates 1, 2, and 3
    
    for i in range(48):  # Generate 48 variations
        # Randomly select a template
        template = random.choice(templates)
        template_num = template['question_number'].split('_')[0]
        
        variation = copy.deepcopy(template)
        
        # Select random shape and transformation
        shape = random.choice(shapes)
        transformation = random.choice(transformations)
        position = random.choice(positions)
        
        variation['question_number'] = f"{template_num}_{variation_num}"
        
        # Update question text
        if transformation == "reflection":
            variation['question_text'] = "Look at this shape:\nWhich image shows a reflection?"
        elif transformation == "rotation":
            variation['question_text'] = "Look at this shape:\nWhich image shows a rotation?"
        else:  # translation
            variation['question_text'] = "Look at this shape:\nWhich image shows a translation?"
        
        # Update image tag
        variation['image_tag'] = f"Gr6_48_{template_num}_{variation_num}"
        
        # Update backend description
        variation['backend_description'] = (
            f"This image shows a {shape['color']} {shape['description']} in the {position} of a grid. "
            f"It is shaded light {shape['color']} with a bold {shape['color']} outline."
        )
        
        # Update image choice tags
        variation['image_choice_tags'] = [
            f"Gr6_48_{template_num}_{variation_num}_A",
            f"Gr6_48_{template_num}_{variation_num}_B",
            f"Gr6_48_{template_num}_{variation_num}_C"
        ]
        
        # Create descriptions for the three options
        other_transformations = [t for t in transformations if t != transformation]
        random.shuffle(other_transformations)
        
        # Generate movement parameters
        translation_x = random.randint(1, 4)
        translation_y = random.randint(1, 4)
        rotation_angle = random.choice([90, 180, 270])
        reflection_line = random.choice(["horizontal", "vertical", "diagonal"])
        
        # Create choice descriptions based on the target transformation
        descriptions = []
        correct_idx = random.randint(0, 2)  # Randomly place correct answer
        
        for j in range(3):
            if j == correct_idx:
                # This is the correct transformation
                if transformation == "rotation":
                    desc = f"This image shows the same {shape['color']} {shape['description']} as in the image 'Gr6_48_{template_num}_{variation_num}', but it has been rotated {rotation_angle}°."
                elif transformation == "reflection":
                    desc = f"This image shows the same {shape['color']} {shape['description']} as in the image 'Gr6_48_{template_num}_{variation_num}', but it has been reflected/flipped {reflection_line}ly."
                else:  # translation
                    desc = f"This image shows the same {shape['color']} {shape['description']} as in the image 'Gr6_48_{template_num}_{variation_num}', but it has been translated {translation_x} units {'down' if random.random() > 0.5 else 'up'} and {translation_y} units {'right' if random.random() > 0.5 else 'left'}."
            else:
                # This is an incorrect transformation
                wrong_trans = other_transformations.pop(0) if other_transformations else random.choice([t for t in transformations if t != transformation])
                if wrong_trans == "rotation":
                    desc = f"This image shows the same {shape['color']} {shape['description']} as in the image 'Gr6_48_{template_num}_{variation_num}', but it has been rotated {rotation_angle}°."
                elif wrong_trans == "reflection":
                    desc = f"This image shows the same {shape['color']} {shape['description']} as in the image 'Gr6_48_{template_num}_{variation_num}', but it has been reflected/flipped {reflection_line}ly."
                else:  # translation
                    desc = f"This image shows the same {shape['color']} {shape['description']} as in the image 'Gr6_48_{template_num}_{variation_num}', but it has been translated {translation_x} units {'down' if random.random() > 0.5 else 'up'} and {translation_y} units {'right' if random.random() > 0.5 else 'left'}."
            
            descriptions.append(desc)
        
        variation['image_choice_tags_backend_description'] = descriptions
        variation['correct_answers'] = [chr(65 + correct_idx)]  # 'A', 'B', or 'C'
        
        # Update solution image tags
        if 'solution_image_tag' in variation:
            new_solution_tags = []
            
            # Step 1: Original shape
            new_solution_tags.append([
                "1/5",
                f"Gr6_48_{template_num}_{variation_num}_step_1",
                variation['backend_description']
            ])
            
            # Steps 3-5: Show each transformation
            step_num = 3
            for j, desc in enumerate(descriptions):
                choice_letter = chr(65 + j)
                trans_type = ""
                if "rotated" in desc:
                    trans_type = "rotation"
                    trans_desc = f"Rotate the shape {rotation_angle}°."
                elif "reflected" in desc:
                    trans_type = "reflection"
                    trans_desc = f"Reflect the shape across a {reflection_line} line."
                else:
                    trans_type = "translation"
                    trans_desc = f"Translate the shape {translation_x} {'down' if 'down' in desc else 'up'} and {translation_y} {'right' if 'right' in desc else 'left'}."
                
                is_correct = (j == correct_idx)
                
                new_solution_tags.append([
                    f"{step_num}/5",
                    f"Gr6_48_{template_num}_{variation_num}_step_{step_num}",
                    desc.replace(f"'Gr6_48_{template_num}_{variation_num}'", f"step 1 ('Gr6_48_{template_num}_{variation_num}_step_1')")
                ])
                step_num += 1
            
            variation['solution_image_tag'] = new_solution_tags
        
        # Update solution text
        solution_steps = [
            ["1/5", "Look at the first shape:"],
            ["2/5", f"Now find the image that shows a {transformation}."]
        ]
        
        step_num = 3
        for j, desc in enumerate(descriptions):
            choice_letter = chr(65 + j)
            if "rotated" in desc:
                trans_type = "rotation"
                trans_desc = f"Rotate the shape {rotation_angle}°."
            elif "reflected" in desc:
                trans_type = "reflection"
                trans_desc = f"Reflect the shape across a {reflection_line} line."
            else:
                trans_type = "translation"
                parts = desc.split("translated")[1].split(".")[0]
                trans_desc = f"Translate the shape{parts}."
            
            is_correct = (j == correct_idx)
            
            if step_num == 5:  # Last step
                if is_correct:
                    solution_steps.append([
                        f"{step_num}/5",
                        f"Image {choice_letter} shows a {trans_type}. {trans_desc} \nImage {choice_letter} is the correct image."
                    ])
                else:
                    solution_steps.append([
                        f"{step_num}/5",
                        f"Image {choice_letter} shows a {trans_type}. {trans_desc}"
                    ])
            else:
                solution_steps.append([
                    f"{step_num}/5",
                    f"Image {choice_letter} shows a {trans_type}. {trans_desc}"
                ])
            step_num += 1
        
        variation['solution'] = solution_steps
        
        variations.append(variation)
        variation_num += 1
    
    return variations

def main():
    """Main function to generate and save variations."""
    variations = generate_variations()
    
    # Save to JSON file
    output_file = 'Gr6_48_E1_variations.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2)
    
    print(f"Generated {len(variations)} variations for Gr6_48_E1")
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
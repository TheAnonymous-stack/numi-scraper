import json
import random
import copy

def load_templates():
    """Load template questions from parsed_templates.json"""
    with open('parsed_templates.json', 'r') as f:
        data = json.load(f)
    return data.get('Gr6_46_E1', [])

def generate_shape_classification_questions():
    """Generate questions about classifying shapes"""
    
    # Define shape properties and relationships
    shapes = {
        'quadrilateral': {
            'properties': '4 sides',
            'includes': ['trapezoid', 'parallelogram', 'rectangle', 'rhombus', 'square', 'kite'],
            'image_descriptions': [
                "This image shows a green shape with 4 sides. The sides are not all the same length, and the angles are not all right angles, and there are no parallel sides.",
                "This image shows a blue shape with 4 sides of different lengths and no parallel sides.",
                "This image shows a red irregular quadrilateral with 4 unequal sides and no special properties.",
                "This image shows a yellow shape with 4 sides, no right angles, and no parallel sides."
            ]
        },
        'trapezoid': {
            'properties': 'exactly 1 pair of parallel sides',
            'includes': [],
            'excludes': ['parallelogram', 'rectangle', 'rhombus', 'square'],
            'image_descriptions': [
                "This image shows a green trapezoid with one pair of parallel sides.",
                "This image shows a blue shape with 4 sides, where exactly one pair of opposite sides are parallel.",
                "This image shows a red trapezoid with parallel top and bottom sides of different lengths.",
                "This image shows a yellow trapezoid with one pair of parallel horizontal sides."
            ]
        },
        'parallelogram': {
            'properties': '2 pairs of parallel sides',
            'includes': ['rectangle', 'rhombus', 'square'],
            'image_descriptions': [
                "This image shows a green parallelogram with opposite sides parallel and equal.",
                "This image shows a blue slanted parallelogram with two pairs of parallel sides.",
                "This image shows a red parallelogram tilted at an angle.",
                "This image shows a yellow parallelogram with opposite sides parallel."
            ]
        },
        'rectangle': {
            'properties': '4 right angles',
            'includes': ['square'],
            'sometimes': ['rhombus'],
            'image_descriptions': [
                "This image shows a green rectangle with 4 right angles and opposite sides equal.",
                "This image shows a blue rectangle with longer horizontal sides than vertical sides.",
                "This image shows a red rectangle with 4 right angles.",
                "This image shows a yellow rectangular shape with all angles at 90 degrees."
            ]
        },
        'rhombus': {
            'properties': '4 equal sides',
            'includes': ['square'],
            'sometimes': ['rectangle'],
            'image_descriptions': [
                "This image shows a green rhombus (diamond shape) with 4 equal sides.",
                "This image shows a blue rhombus tilted at 45 degrees with all sides equal.",
                "This image shows a red diamond-shaped rhombus with 4 equal sides.",
                "This image shows a yellow rhombus with all sides the same length."
            ]
        },
        'square': {
            'properties': '4 equal sides and 4 right angles',
            'is_always': ['quadrilateral', 'parallelogram', 'rectangle', 'rhombus'],
            'image_descriptions': [
                "This image shows a green square with 4 equal sides and 4 right angles.",
                "This image shows a blue square with all sides equal and all angles 90 degrees.",
                "This image shows a red perfect square.",
                "This image shows a yellow square with equal sides and right angles."
            ]
        },
        'kite': {
            'properties': '2 pairs of adjacent equal sides',
            'sometimes': ['rhombus'],
            'image_descriptions': [
                "This image shows a green kite shape with two pairs of adjacent equal sides.",
                "This image shows a blue kite with symmetry along one diagonal.",
                "This image shows a red kite shape like those flown in the sky.",
                "This image shows a yellow kite with two pairs of adjacent sides equal."
            ]
        }
    }
    
    return shapes

def generate_relationship_questions():
    """Generate questions about shape relationships"""
    
    relationships = [
        # Always true relationships
        ("square", "rectangle", "always", "A square has 4 right angles, which is the defining property of a rectangle."),
        ("square", "rhombus", "always", "A square has 4 equal sides, which is the defining property of a rhombus."),
        ("square", "parallelogram", "always", "A square has 2 pairs of parallel sides, making it a parallelogram."),
        ("square", "quadrilateral", "always", "A square has 4 sides, making it a quadrilateral."),
        ("rectangle", "parallelogram", "always", "A rectangle has 2 pairs of parallel sides, making it a parallelogram."),
        ("rhombus", "parallelogram", "always", "A rhombus has 2 pairs of parallel sides, making it a parallelogram."),
        ("parallelogram", "quadrilateral", "always", "A parallelogram has 4 sides, making it a quadrilateral."),
        ("trapezoid", "quadrilateral", "always", "A trapezoid has 4 sides, making it a quadrilateral."),
        
        # Sometimes true relationships
        ("rectangle", "rhombus", "sometimes", "A rectangle is a rhombus only when all 4 sides are equal (making it a square)."),
        ("rhombus", "rectangle", "sometimes", "A rhombus is a rectangle only when all 4 angles are right angles (making it a square)."),
        ("kite", "rhombus", "sometimes", "A kite is a rhombus when all 4 sides are equal."),
        
        # Never true relationships
        ("trapezoid", "parallelogram", "never", "A trapezoid has exactly 1 pair of parallel sides, while a parallelogram has 2 pairs."),
        ("trapezoid", "rectangle", "never", "A trapezoid has exactly 1 pair of parallel sides, while a rectangle has 2 pairs."),
        ("trapezoid", "rhombus", "never", "A trapezoid has exactly 1 pair of parallel sides, while a rhombus has 2 pairs."),
        ("trapezoid", "square", "never", "A trapezoid has exactly 1 pair of parallel sides, while a square has 2 pairs.")
    ]
    
    return relationships

def generate_pop_culture_contexts():
    """Generate pop culture themed contexts for word problems"""
    contexts = [
        "In a Minecraft building challenge",
        "While designing a Pokemon gym",
        "In a Naruto ninja academy lesson",
        "During a My Hero Academia training exercise",
        "In a Dragon Ball Z tournament arena",
        "While creating Attack on Titan wall designs",
        "In a One Piece treasure map",
        "During a Demon Slayer training session",
        "In a Jujutsu Kaisen barrier technique",
        "While playing Fortnite building mode",
        "In an Among Us map design",
        "During a League of Legends champion design",
        "In a Genshin Impact puzzle room",
        "While creating a Roblox game level",
        "In a Super Mario level design"
    ]
    return contexts

def generate_variation_type_1(template, var_num):
    """Generate 'Which words describe this shape?' variations"""
    variation = copy.deepcopy(template)
    shapes = generate_shape_classification_questions()
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    # Update image tag
    if 'image_tag' in template:
        old_tag = template['image_tag']
        parts = old_tag.split('_')
        if len(parts) >= 4:
            parts[3] = str(var_num)
            variation['image_tag'] = '_'.join(parts)
    
    # Choose a shape to show
    shape_shown = random.choice(['quadrilateral', 'trapezoid', 'parallelogram', 'rectangle', 'rhombus', 'square', 'kite'])
    
    # Determine correct classifications
    correct_classifications = ['quadrilateral']  # All are quadrilaterals
    
    if shape_shown == 'trapezoid':
        correct_classifications = ['quadrilateral', 'trapezoid']
    elif shape_shown == 'parallelogram':
        correct_classifications = ['quadrilateral', 'parallelogram']
    elif shape_shown == 'rectangle':
        correct_classifications = ['quadrilateral', 'parallelogram', 'rectangle']
    elif shape_shown == 'rhombus':
        correct_classifications = ['quadrilateral', 'parallelogram', 'rhombus']
    elif shape_shown == 'square':
        correct_classifications = ['quadrilateral', 'parallelogram', 'rectangle', 'rhombus', 'square']
    elif shape_shown == 'kite':
        correct_classifications = ['quadrilateral', 'kite']
    
    # Generate choices
    all_shapes = ['quadrilateral', 'trapezoid', 'parallelogram', 'rectangle', 'rhombus', 'square', 'kite']
    choices = random.sample(all_shapes, min(4, len(all_shapes)))
    
    # Ensure at least one correct answer is in choices
    if not any(c in correct_classifications for c in choices):
        choices[0] = random.choice(correct_classifications)
    
    # Find the correct answer (first correct classification in choices)
    correct_answer = None
    for i, choice in enumerate(choices):
        if choice in correct_classifications:
            correct_answer = chr(65 + i)  # A, B, C, or D
            break
    
    # Add context occasionally
    if random.random() < 0.2:
        context = random.choice(generate_pop_culture_contexts())
        variation['question_text'] = f"{context}, which words describe this shape? Choose all that apply."
    else:
        variation['question_text'] = "Which words describe this shape? Choose all that apply."
    
    variation['choices'] = choices
    variation['correct_answers'] = [correct_answer]
    
    # Update backend description
    if 'backend_description' in variation:
        variation['backend_description'] = random.choice(shapes[shape_shown]['image_descriptions'])
    
    # Generate solution based on shape shown
    solution_steps = []
    
    if 'quadrilateral' in correct_classifications:
        solution_steps.append(["1/5", f"Yes, this shape is a quadrilateral, because it has 4 sides."])
    
    if shape_shown == 'trapezoid':
        solution_steps.append(["2/5", "Yes, this shape is a trapezoid, because it has exactly 1 pair of parallel sides."])
        solution_steps.append(["3/5", "No, this shape is not a parallelogram, rectangle, rhombus, or square, because it does not have 2 pairs of parallel sides."])
    elif shape_shown == 'square':
        solution_steps.append(["2/5", "Yes, this shape is a square, because it has 4 equal sides and 4 right angles."])
        solution_steps.append(["3/5", "A square is also a rectangle (4 right angles), a rhombus (4 equal sides), and a parallelogram (2 pairs of parallel sides)."])
    
    solution_steps.append(["4/5", f"Therefore, this shape is: {', '.join(correct_classifications)}."])
    solution_steps.append(["5/5", f"The best answer from the choices given is: {choices[ord(correct_answer) - 65]}."])
    
    variation['solution'] = solution_steps
    
    return variation

def generate_variation_type_2(template, var_num):
    """Generate 'Is X always/sometimes/never Y?' variations"""
    variation = copy.deepcopy(template)
    relationships = generate_relationship_questions()
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    # Update solution image tags if present
    if 'solution_image_tag' in template:
        for step in variation['solution_image_tag']:
            if len(step) > 1:
                old_tag = step[1]
                parts = old_tag.split('_')
                if len(parts) >= 4:
                    # Keep the step suffix
                    step_suffix = '_'.join(parts[4:]) if len(parts) > 4 else ''
                    parts[3] = str(var_num)
                    new_tag = '_'.join(parts[:4])
                    if step_suffix:
                        new_tag += '_' + step_suffix
                    step[1] = new_tag
                    
                    # Update backend description
                    if len(step) > 2:
                        if "square" in step[2].lower():
                            step[2] = "This image shows a green square."
                        elif "rectangle" in step[2].lower():
                            step[2] = "This image shows a pink rectangle."
                        elif "rhombus" in step[2].lower():
                            step[2] = "This image shows a blue rhombus."
                        elif "parallelogram" in step[2].lower():
                            step[2] = "This image shows a yellow parallelogram."
    
    # Choose a relationship
    shape1, shape2, answer, explanation = random.choice(relationships)
    
    # Generate question text
    question_formats = [
        f"Is a {shape1} always a {shape2}?",
        f"Is every {shape1} also a {shape2}?",
        f"Must a {shape1} be a {shape2}?",
        f"Are all {shape1}s also {shape2}s?"
    ]
    
    variation['question_text'] = random.choice(question_formats)
    
    # Set choices based on answer type
    if answer == "always" or answer == "never":
        variation['choices'] = ["yes", "no"]
        variation['correct_answers'] = ["A"] if answer == "always" else ["B"]
    else:  # sometimes - not used in yes/no format
        # Convert to always/sometimes/never format
        variation['question_text'] = f"A {shape1} is ____ a {shape2}."
        variation['choices'] = ["always", "sometimes", "never"]
        variation['correct_answers'] = ["B"]  # sometimes
    
    # Generate solution
    if answer == "always":
        variation['solution'] = [
            ["1/3", f"A {shape1} is always a {shape2}."],
            ["2/3", explanation],
            ["3/3", f"Therefore, the answer is yes."]
        ]
    elif answer == "never":
        variation['solution'] = [
            ["1/3", f"A {shape1} is never a {shape2}."],
            ["2/3", explanation],
            ["3/3", f"Therefore, the answer is no."]
        ]
    else:  # sometimes
        variation['solution'] = [
            ["1/3", f"A {shape1} is sometimes a {shape2}."],
            ["2/3", explanation],
            ["3/3", f"Therefore, the answer is sometimes."]
        ]
    
    return variation

def generate_variation_type_3(template, var_num):
    """Generate 'Choose the word that makes this sentence true' variations"""
    variation = copy.deepcopy(template)
    
    # Update question number
    template_num = template['question_number'].split('_')[0]
    variation['question_number'] = f"{template_num}_{var_num}"
    
    # Define sentence patterns
    patterns = [
        ("trapezoid", "quadrilateral", "always", "A trapezoid has 4 sides.", "This means a trapezoid is always a quadrilateral because it has 4 sides."),
        ("parallelogram", "quadrilateral", "always", "A parallelogram has 4 sides.", "This means a parallelogram is always a quadrilateral because it has 4 sides."),
        ("rectangle", "parallelogram", "always", "A rectangle has 2 pairs of parallel sides.", "This means a rectangle is always a parallelogram."),
        ("square", "rectangle", "always", "A square has 4 right angles.", "This means a square is always a rectangle."),
        ("square", "rhombus", "always", "A square has 4 equal sides.", "This means a square is always a rhombus."),
        ("rhombus", "parallelogram", "always", "A rhombus has 2 pairs of parallel sides.", "This means a rhombus is always a parallelogram."),
        ("rectangle", "square", "sometimes", "A rectangle has 4 right angles.", "A rectangle is only a square when all 4 sides are equal, so a rectangle is sometimes a square."),
        ("rhombus", "square", "sometimes", "A rhombus has 4 equal sides.", "A rhombus is only a square when all 4 angles are right angles, so a rhombus is sometimes a square."),
        ("parallelogram", "rectangle", "sometimes", "A parallelogram has 2 pairs of parallel sides.", "A parallelogram is only a rectangle when all angles are right angles, so a parallelogram is sometimes a rectangle."),
        ("trapezoid", "parallelogram", "never", "A trapezoid has exactly 1 pair of parallel sides, while a parallelogram has 2 pairs.", "This means a trapezoid is never a parallelogram."),
        ("trapezoid", "rectangle", "never", "A trapezoid has exactly 1 pair of parallel sides, while a rectangle has 2 pairs.", "This means a trapezoid is never a rectangle."),
        ("trapezoid", "rhombus", "never", "A trapezoid has exactly 1 pair of parallel sides, while a rhombus has 2 pairs.", "This means a trapezoid is never a rhombus.")
    ]
    
    # Choose a pattern
    shape1, shape2, correct_answer, property, explanation = random.choice(patterns)
    
    # Add context occasionally
    if random.random() < 0.2:
        context = random.choice(generate_pop_culture_contexts())
        variation['question_text'] = f"{context}, choose the word that makes this sentence true.\nA {shape1} is ____ a {shape2}."
    else:
        variation['question_text'] = f"Choose the word that makes this sentence true.\nA {shape1} is ____ a {shape2}."
    
    variation['choices'] = ["always", "sometimes", "never"]
    
    # Set correct answer
    if correct_answer == "always":
        variation['correct_answers'] = ["A"]
    elif correct_answer == "sometimes":
        variation['correct_answers'] = ["B"]
    else:  # never
        variation['correct_answers'] = ["C"]
    
    # Generate solution
    variation['solution'] = [
        ["1/2", property],
        ["2/2", explanation]
    ]
    
    return variation

def generate_variation(template, var_num, total_templates):
    """Generate a single variation based on template type"""
    
    # Determine template type based on question structure
    if "Which words describe this shape?" in template['question_text']:
        return generate_variation_type_1(template, var_num)
    elif "Is a" in template['question_text'] and "always" in template['question_text']:
        return generate_variation_type_2(template, var_num)
    elif "Choose the word that makes this sentence true" in template['question_text']:
        return generate_variation_type_3(template, var_num)
    else:
        # Default to type 3 for unknown formats
        return generate_variation_type_3(template, var_num)

def main():
    """Main function to generate all variations"""
    templates = load_templates()
    
    if not templates:
        print("No templates found for Gr6_46_E1")
        return
    
    print(f"Found {len(templates)} templates for Gr6_46_E1")
    
    # Calculate how many variations we need
    total_needed = 51
    variations_needed = total_needed - len(templates)
    
    print(f"Generating {variations_needed} variations to reach {total_needed} total")
    
    variations = []
    
    # Ensure variety by cycling through template types
    template_cycle = []
    for _ in range(variations_needed // len(templates) + 1):
        template_cycle.extend(templates)
    
    # Generate variations
    for i in range(variations_needed):
        # Select template in a round-robin fashion for variety
        template = template_cycle[i % len(template_cycle)]
        
        # Generate variation number (starting after templates)
        var_num = len(templates) + i + 1
        
        variation = generate_variation(template, var_num, len(templates))
        variations.append(variation)
        
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1} variations...")
    
    # Save variations to file
    output_file = 'Gr6_46_E1_variations.json'
    with open(output_file, 'w') as f:
        json.dump(variations, f, indent=2)
    
    print(f"\nSuccessfully generated {len(variations)} variations")
    print(f"Variations saved to {output_file}")
    
    # Verify uniqueness
    question_texts = [v['question_text'] for v in variations]
    unique_questions = len(set(question_texts))
    print(f"Unique question texts: {unique_questions}/{len(variations)}")

if __name__ == "__main__":
    main()
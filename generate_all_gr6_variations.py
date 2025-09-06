import json
import random
import copy
from collections import defaultdict

def load_templates():
    """Load all template questions from parsed_templates.json"""
    with open('parsed_templates.json', 'r') as f:
        all_templates = json.load(f)
    
    # Group templates by tag
    templates_by_tag = defaultdict(list)
    for template in all_templates:
        if 'tag' in template:
            templates_by_tag[template['tag']].append(template)
    
    return templates_by_tag

def generate_Gr6_51_E3_variations(templates):
    """Generate variations for complementary angles questions"""
    variations = []
    variations_needed = 51 - len(templates)
    
    angle_pairs = [
        ("AGB", "CGD"), ("BGC", "DGE"), ("CGD", "EGF"), 
        ("DGE", "FGA"), ("EGF", "AGB"), ("FGA", "BGC"),
        ("AGC", "CGE"), ("BGD", "DGF"), ("CGE", "EGA"),
        ("DGF", "FGB"), ("EGA", "AGC"), ("FGB", "BGD")
    ]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Select random angle pair
        main_angle, comp_angle = random.choice(angle_pairs)
        
        # Create wrong options
        all_angles = ["AGB", "BGC", "CGD", "DGE", "EGF", "FGA"]
        wrong_angles = [a for a in all_angles if a != comp_angle]
        random.shuffle(wrong_angles)
        wrong_options = wrong_angles[:3]
        
        # Create choices and randomize correct position
        choices = wrong_options + [f"$\\angle {comp_angle}$"]
        random.shuffle(choices)
        correct_index = choices.index(f"$\\angle {comp_angle}$")
        
        variation['question_text'] = f"Which angle is complementary to $\\angle {main_angle}$?"
        # Format choices properly
        formatted_choices = []
        for opt in choices:
            if '$' not in opt:
                formatted_choices.append(f"$\\angle {opt}$")
            else:
                formatted_choices.append(opt)
        variation['choices'] = formatted_choices
        variation['correct_answers'] = [chr(65 + correct_index)]  # A, B, C, or D
        variation['question_number'] = f"3_{i+5}"
        
        # Update image tag
        variation['image_tag'] = f"Gr6_51_3_{i+5}"
        if 'solution_image_tag' in variation:
            for img in variation['solution_image_tag']:
                img[1] = f"Gr6_51_3_{i+5}_step_{img[0].split('/')[0]}"
        
        # Update solution text
        if 'solution' in variation:
            for step in variation['solution']:
                if len(step) >= 2 and "complementary to" in step[1]:
                    step[1] = f"$\\angle {comp_angle}$ is complementary to $\\angle {main_angle}$." + step[1].split('.', 1)[1] if '.' in step[1] else ""
        
        variations.append(variation)
    
    return variations

def generate_Gr6_51_E4_variations(templates):
    """Generate variations for finding angle measures"""
    variations = []
    variations_needed = 51 - len(templates)
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random complementary angle pairs
        angle1 = random.randint(10, 80)
        angle2 = 90 - angle1
        
        # Randomly decide which angle to find
        if random.choice([True, False]):
            given_angle = angle1
            find_angle = angle2
        else:
            given_angle = angle2
            find_angle = angle1
        
        # Use different variable names
        var_names = ['f', 'x', 'y', 'a', 'b', 'c', 'm', 'n', 'p', 'q']
        var = random.choice(var_names)
        
        variation['question_text'] = f"What is the value of {var}?\\n{var}=___°"
        variation['backend_description'] = f"The diagram shows three rays extending from a common point. A red arc marks a right angle at the common point. Two angles are formed: angle {var} and an angle labeled {given_angle}°. Together, they make up the 90° right angle."
        variation['correct_answers'] = [str(find_angle)]
        variation['question_number'] = f"4_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/4", "Complementary angles have measures that add to 90°. When a right angle is divided into two adjacent angles, complementary angles are formed."],
                ["2/4", f"Add the measures of the complementary angles and set the sum equal to 90°. Then solve for {var}."],
                ["3/4", f"{given_angle}°+{var}=90°\\n{var}=90°-{given_angle}°\\n{var}={find_angle}°"],
                ["4/4", f"So, {var} = {find_angle}°"]
            ]
        
        # Update image tag
        variation['image_tag'] = f"Gr6_51_4_{i+2}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_52_E1_variations(templates):
    """Generate variations for understanding trapezoid area"""
    variations = []
    variations_needed = 51 - len(templates)
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random trapezoid dimensions
        base1 = random.randint(2, 8)
        base2 = random.randint(base1 + 2, 12)
        height = random.randint(2, 6)
        
        variation['backend_description'] = f"This image shows a trapezoid shaded in blue, with the top base measuring {base1} meters, the bottom base measuring {base2} meters, and the height labeled as {height} meter{'s' if height > 1 else ''}."
        variation['question_number'] = f"1_{i+2}"
        
        # Keep the same question structure about cutting into triangles
        # Randomize correct answer position
        if random.choice([True, False]):
            variation['correct_answers'] = ['A']
            variation['image_choice_tags_backend_description'] = [
                "A white diagonal line is drawn from corner to corner. This line splits the trapezoid into two triangles.",
                "A white horizontal line is drawn across the trapezoid, parallel to the bases. This splits the trapezoid into two smaller trapezoids."
            ]
        else:
            variation['correct_answers'] = ['B']
            variation['image_choice_tags_backend_description'] = [
                "A white horizontal line is drawn across the trapezoid, parallel to the bases. This splits the trapezoid into two smaller trapezoids.",
                "A white diagonal line is drawn from corner to corner. This line splits the trapezoid into two triangles."
            ]
        
        # Update image tags
        variation['image_tag'] = f"Gr6_52_1_{i+2}"
        variation['image_choice_tags'] = [f"Gr6_52_1_{i+2}_A", f"Gr6_52_1_{i+2}_B"]
        
        if 'solution_image_tag' in variation:
            for img in variation['solution_image_tag']:
                img[1] = f"Gr6_52_1_{i+2}_step_{img[0].split('/')[0]}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_52_E2_variations(templates):
    """Generate variations for area of trapezoids"""
    variations = []
    variations_needed = 51 - len(templates)
    
    units = ["metres", "feet", "yards", "inches", "centimetres", "kilometers", "miles"]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random trapezoid dimensions
        base1 = random.randint(10, 30)
        base2 = random.randint(5, base1 - 2)
        height = random.randint(6, 20)
        
        # Calculate area
        area = int(0.5 * height * (base1 + base2))
        
        # Select random unit
        unit = random.choice(units)
        
        variation['question_text'] = f"What is the area?\\n___ square {unit}"
        variation['backend_description'] = f"This image shows a trapezoid shaded in green, with the bottom base measuring {base1} {unit}, the top base measuring {base2} {unit}, and the height labeled as {height} {unit}."
        variation['correct_answers'] = [str(area)]
        variation['question_number'] = f"2_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/3", f"Find the bases and height of the trapezoid.\\n$\\text{{base}}_1 = {base1}$ {unit[0]}\\n$\\text{{base}}_2 = {base2}$ {unit[0]}\\n$\\text{{height}} = {height}$ {unit[0]}"],
                ["2/3", f"Use these numbers in the area of a trapezoid formula.\\n$\\text{{Area}} = \\frac{{1}}{{2}} \\times \\text{{height}} \\times (\\text{{base}}_1 + \\text{{base}}_2)$\\n$= \\frac{{1}}{{2}} \\times {height}({base1}+{base2})$\\n$= {area}$"],
                ["3/3", f"Now find the units. The lengths are measured in {unit}, so the area is measured in square {unit}."],
                ["4/4", f"The area of the trapezoid is {area} square {unit}."]
            ]
        
        # Update image tag
        variation['image_tag'] = f"Gr6_52_2_{i+2}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_52_E3_variations(templates):
    """Generate variations for area of rhombuses"""
    variations = []
    variations_needed = 51 - len(templates)
    
    units = ["kilometres", "meters", "feet", "yards", "inches", "centimetres", "miles"]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random rhombus diagonals
        d1 = random.randint(6, 20)
        d2 = random.randint(4, 18)
        
        # Calculate area
        area = int(0.5 * d1 * d2)
        
        # Select random unit
        unit = random.choice(units)
        
        variation['question_text'] = f"The diagonals of this rhombus are {d1} {unit} and {d2} {unit}.\\nWhat is the area of the rhombus?\\n___ square {unit}"
        variation['backend_description'] = f"This image shows a rhombus shaded in blue, with the diagonals labeled as {d1} {unit} and {d2} {unit}."
        variation['correct_answers'] = [str(area)]
        variation['question_number'] = f"3_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/3", f"The rhombus has diagonals $d_1$={d1} {unit} and $d_2$={d2} {unit}."],
                ["2/3", f"Use these numbers in the area of a rhombus formula:\\n$A = \\frac{{1}}{{2}} d_1 d_2$\\n$= \\frac{{1}}{{2}} ({d1})({d2})$\\n$= ({d1//2})({d2})$ if d1 is even else $= {area}$\\n$= {area}$"],
                ["3/3", f"The area of the rhombus is $\\textbf{{{area} square {unit}}}$."]
            ]
        
        # Update image tag
        variation['image_tag'] = f"Gr6_52_3_{i+2}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_52_E4_variations(templates):
    """Generate variations for area of compound figures"""
    variations = []
    variations_needed = 51 - len(templates)
    
    units = ["kilometres", "meters", "feet", "yards", "miles", "centimetres"]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random dimensions for two rectangles
        rect1_width = random.randint(15, 30)
        rect1_height = random.randint(8, 20)
        rect2_width = random.randint(4, 10)
        rect2_height = random.randint(3, 8)
        
        # Calculate areas
        area1 = rect1_width * rect1_height
        area2 = rect2_width * rect2_height
        total_area = area1 + area2
        
        # Select random unit
        unit = random.choice(units)
        
        variation['question_text'] = f"What is the area of this figure?\\n___ square {unit}"
        variation['backend_description'] = f"This image shows a compound figure made up of two rectangles joined together. The larger rectangle measures {rect1_width} {unit} wide and {rect1_height} {unit} tall. The smaller rectangle measures {rect2_width} {unit} wide and {rect2_height} {unit} tall."
        variation['correct_answers'] = [str(total_area)]
        variation['question_number'] = f"4_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/7", "Divide the figure into rectangles:"],
                ["2/7", f"Start with rectangle A. Rectangle A is {rect1_width} {unit} wide and {rect1_height} {unit} tall."],
                ["3/7", f"Multiply:\\n${rect1_width} \\times {rect1_height} = {area1}$\\nThe area of rectangle A is {area1} square {unit}."],
                ["4/7", f"Look at rectangle B. Rectangle B is {rect2_width} {unit} wide and {rect2_height} {unit} tall."],
                ["5/7", f"Multiply:\\n${rect2_width} \\times {rect2_height} = {area2}$\\nThe area of rectangle B is {area2} square {unit}."],
                ["6/7", f"Now add the areas of the two rectangles:\\n${area1} + {area2} = {total_area}$"],
                ["7/7", f"The area is {total_area} square {unit}."]
            ]
        
        # Update image tags
        variation['image_tag'] = f"Gr6_52_4_{i+2}"
        if 'solution_image_tag' in variation:
            for img in variation['solution_image_tag']:
                img[1] = f"Gr6_52_4_{i+2}_step_{img[0].split('/')[0]}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_53_E2_variations(templates):
    """Generate variations for surface area of cubes"""
    variations = []
    variations_needed = 51 - len(templates)
    
    units = ["centimetres", "inches", "feet", "meters", "millimetres"]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random cube side length
        side = random.randint(3, 15)
        
        # Calculate surface area
        face_area = side * side
        surface_area = 6 * face_area
        
        # Select random unit
        unit = random.choice(units)
        
        variation['question_text'] = f"What is the surface area?\\n___ square {unit}"
        variation['backend_description'] = f"This image shows a cube with each side labeled as {side} {unit}."
        variation['correct_answers'] = [str(surface_area)]
        variation['question_number'] = f"2_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/6", f"Each face of the cube is a square with sides that are {side} {unit} long."],
                ["2/6", "Find the area of one face:"],
                ["3/6", f"Area = side $\\times$ side\\n$= {side} \\times {side}$\\n$= {face_area}$"],
                ["4/6", f"The area of each face is {face_area} square {unit}. There are 6 faces."],
                ["5/6", f"Multiply:\\nSurface Area = $6 \\times {face_area} = {surface_area}$"],
                ["6/6", f"The surface area of the cube is {surface_area} square {unit}."]
            ]
        
        # Update image tags
        variation['image_tag'] = f"Gr6_53_2_{i+2}"
        if 'solution_image_tag' in variation:
            for img in variation['solution_image_tag']:
                img[1] = f"Gr6_53_2_{i+2}_step_{img[0].split('/')[0]}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_53_E3_variations(templates):
    """Generate variations for surface area of triangular prisms"""
    variations = []
    variations_needed = 51 - len(templates)
    
    units = ["inches", "centimetres", "feet", "meters", "millimetres"]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random triangular prism dimensions
        tri_base = random.randint(8, 20)
        tri_height = random.randint(6, 16)
        prism_length = random.randint(8, 15)
        
        # Calculate areas
        tri_area = int(0.5 * tri_base * tri_height)
        rect1_area = prism_length * prism_length  # Two square faces
        rect2_area = tri_base * prism_length  # Bottom rectangular face
        
        surface_area = 2 * tri_area + 2 * rect1_area + rect2_area
        
        # Select random unit
        unit = random.choice(units)
        
        variation['question_text'] = f"What is the surface area?\\n___ square {unit}"
        variation['backend_description'] = f"This image shows a triangular prism with triangular bases having base {tri_base} {unit} and height {tri_height} {unit}. The prism length is {prism_length} {unit}."
        variation['correct_answers'] = [str(surface_area)]
        variation['question_number'] = f"3_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/9", "Find the area of each face."],
                ["2/9", f"1st: $\\frac{{1}}{{2}} \\times {tri_base} \\times {tri_height} = {tri_area}$"],
                ["3/9", f"2nd: $\\frac{{1}}{{2}} \\times {tri_base} \\times {tri_height} = {tri_area}$"],
                ["4/9", f"3rd: ${prism_length} \\times {prism_length} = {rect1_area}$"],
                ["5/9", f"4th: ${prism_length} \\times {prism_length} = {rect1_area}$"],
                ["6/9", f"5th: ${tri_base} \\times {prism_length} = {rect2_area}$"],
                ["7/9", "Add the areas of the 5 faces to find the surface area."],
                ["8/9", f"Surface area = ${tri_area} + {tri_area} + {rect1_area} + {rect1_area} + {rect2_area} = {surface_area}$"],
                ["9/9", f"The surface area is {surface_area} square {unit}."]
            ]
        
        # Update image tags
        variation['image_tag'] = f"Gr6_53_3_{i+2}"
        if 'solution_image_tag' in variation:
            for idx, img in enumerate(variation['solution_image_tag']):
                img[1] = f"Gr6_53_3_{i+2}_step_{idx+2}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_53_E4_variations(templates):
    """Generate variations for surface area of pyramids"""
    variations = []
    variations_needed = 51 - len(templates)
    
    units = ["metres", "feet", "inches", "centimetres", "yards"]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Generate random pyramid dimensions
        base_side = random.randint(3, 8)
        slant_height = random.randint(base_side + 1, 12)
        
        # Calculate areas
        tri_area = int(0.5 * base_side * slant_height)
        base_area = base_side * base_side
        surface_area = 4 * tri_area + base_area
        
        # Select random unit
        unit = random.choice(units)
        
        variation['question_text'] = f"What is the surface area of this rectangular pyramid?\\n___ square {unit}"
        variation['backend_description'] = f"This image shows a rectangular pyramid with a square base of {base_side} {unit} by {base_side} {unit}. Each triangular face has a base of {base_side} {unit} and a slant height of {slant_height} {unit}."
        variation['correct_answers'] = [str(surface_area)]
        variation['question_number'] = f"4_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            variation['solution'] = [
                ["1/9", "Find the area of each face."],
                ["2/9", f"1st: $\\frac{{1}}{{2}}\\times {base_side} \\times {slant_height} = {tri_area}$"],
                ["3/9", f"2nd: $\\frac{{1}}{{2}}\\times {base_side} \\times {slant_height} = {tri_area}$"],
                ["4/9", f"3rd: $\\frac{{1}}{{2}}\\times {base_side} \\times {slant_height} = {tri_area}$"],
                ["5/9", f"4th: $\\frac{{1}}{{2}}\\times {base_side} \\times {slant_height} = {tri_area}$"],
                ["6/9", f"5th: ${base_side} \\times {base_side} = {base_area}$"],
                ["7/9", "Add the areas of the 5 faces to find the surface area."],
                ["8/9", f"Surface area = ${tri_area} + {tri_area} + {tri_area} + {tri_area} + {base_area} = {surface_area}$"],
                ["9/9", f"The surface area of the rectangular pyramid is {surface_area} square {unit}."]
            ]
        
        # Update image tags
        variation['image_tag'] = f"Gr6_53_4_{i+2}"
        if 'solution_image_tag' in variation:
            for idx, img in enumerate(variation['solution_image_tag']):
                img[1] = f"Gr6_53_4_{i+2}_step_{idx+2}"
        
        variations.append(variation)
    
    return variations

def generate_Gr6_54_E1_variations(templates):
    """Generate variations for payment methods questions"""
    variations = []
    variations_needed = 51 - len(templates)
    
    payment_scenarios = [
        {
            "context": "movie tickets",
            "payment": "credit card",
            "advantages": [
                "You can buy now and pay later.",
                "Credit cards offer fraud protection.",
                "You can earn rewards points."
            ],
            "disadvantages": [
                "You may spend more than you can afford.",
                "Interest charges apply if not paid in full.",
                "Annual fees may apply."
            ]
        },
        {
            "context": "groceries",
            "payment": "cash",
            "advantages": [
                "No fees or interest charges.",
                "Helps control spending.",
                "Accepted everywhere."
            ],
            "disadvantages": [
                "Can be lost or stolen.",
                "No purchase protection.",
                "Need exact change sometimes."
            ]
        },
        {
            "context": "online shopping",
            "payment": "digital wallet",
            "advantages": [
                "Quick and convenient.",
                "Enhanced security features.",
                "No need to enter card details."
            ],
            "disadvantages": [
                "Not accepted everywhere.",
                "Requires internet connection.",
                "Technical issues can occur."
            ]
        },
        {
            "context": "restaurant bill",
            "payment": "debit card",
            "advantages": [
                "Uses your own money.",
                "No interest charges.",
                "Easy to track spending."
            ],
            "disadvantages": [
                "Need sufficient account balance.",
                "Overdraft fees if insufficient funds.",
                "Less fraud protection than credit cards."
            ]
        },
        {
            "context": "concert tickets",
            "payment": "prepaid card",
            "advantages": [
                "Spending limit built in.",
                "No bank account needed.",
                "Good for budgeting."
            ],
            "disadvantages": [
                "Fees for loading money.",
                "Balance can expire.",
                "Limited acceptance."
            ]
        }
    ]
    
    for i in range(variations_needed):
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Select random scenario
        scenario = random.choice(payment_scenarios)
        
        # Randomly choose between advantage or disadvantage question
        is_advantage = random.choice([True, False])
        
        if is_advantage:
            variation['question_text'] = f"Which of the following is an advantage of using a {scenario['payment']} to pay for {scenario['context']}?"
            correct = random.choice(scenario['advantages'])
            incorrect = random.sample(scenario['disadvantages'], 2)
        else:
            variation['question_text'] = f"Which of the following is a disadvantage of using a {scenario['payment']} to pay for {scenario['context']}?"
            correct = random.choice(scenario['disadvantages'])
            incorrect = random.sample(scenario['advantages'], 2)
        
        # Create choices and randomize position
        choices = incorrect + [correct]
        random.shuffle(choices)
        correct_index = choices.index(correct)
        
        variation['choices'] = choices
        variation['correct_answers'] = [chr(65 + correct_index)]  # A, B, or C
        variation['question_number'] = f"1_{i+2}"
        
        # Update solution
        if 'solution' in variation:
            new_solution = []
            for j, choice in enumerate(choices):
                step_num = f"{j+2}/4"
                if j == correct_index:
                    explanation = f"{choice}\\nThis is {'an advantage' if is_advantage else 'a disadvantage'} of paying with a {scenario['payment']}."
                else:
                    explanation = f"x {choice}\\nThis is {'a disadvantage' if is_advantage else 'an advantage'}, not {'an advantage' if is_advantage else 'a disadvantage'}, of paying with a {scenario['payment']}."
                new_solution.append([step_num, explanation])
            
            # Add introduction
            new_solution.insert(0, ["1/4", f"Remember, a {scenario['payment']} is a payment method with specific advantages and disadvantages."])
            variation['solution'] = new_solution
        
        variations.append(variation)
    
    return variations

def generate_Gr6_45_E4_variations(templates):
    """Generate variations for nets of 3D figures questions"""
    variations = []
    # We have 2 templates, need 49 more variations for total of 51
    variations_needed = 49
    
    # Define 3D shapes and their characteristics
    shapes_data = {
        "cube": {
            "description": "This figure shows a cube.",
            "net_description": "a net made of six connected squares",
            "faces": "six square faces"
        },
        "rectangular prism": {
            "description": "This figure shows a rectangular prism.",
            "net_description": "a net made up of six connected rectangles arranged in a cross shape",
            "faces": "six rectangular faces"
        },
        "triangular prism": {
            "description": "This figure shows a triangular prism.",
            "net_description": "a net with two triangular faces and three rectangular faces",
            "faces": "two triangle faces and three rectangular faces"
        },
        "triangular pyramid": {
            "description": "This figure shows a triangular pyramid (tetrahedron).",
            "net_description": "a triangle with a smaller upside-down triangle outlined with dashed lines inside it",
            "faces": "four triangular faces"
        },
        "square pyramid": {
            "description": "This figure shows a square pyramid.",
            "net_description": "a net with one square base and four triangular faces",
            "faces": "one square base and four triangular faces"
        },
        "pentagonal prism": {
            "description": "This figure shows a pentagonal prism.",
            "net_description": "a net with two pentagonal faces and five rectangular faces",
            "faces": "two pentagonal faces and five rectangular faces"
        },
        "hexagonal prism": {
            "description": "This figure shows a hexagonal prism.",
            "net_description": "a net with two hexagonal faces and six rectangular faces",
            "faces": "two hexagonal faces and six rectangular faces"
        },
        "cylinder": {
            "description": "This figure shows a cylinder.",
            "net_description": "a net with two circular faces and one rectangular face",
            "faces": "two circular bases and one curved rectangular surface"
        },
        "cone": {
            "description": "This figure shows a cone.",
            "net_description": "a net with one circular base and one sector (partial circle)",
            "faces": "one circular base and one curved surface"
        },
        "octahedron": {
            "description": "This figure shows an octahedron.",
            "net_description": "a net made of eight connected triangles",
            "faces": "eight triangular faces"
        }
    }
    
    # Pop culture themes for context variety
    themes = [
        "gift box", "treasure chest", "minecraft block", "dice", "building block",
        "shipping box", "storage container", "puzzle piece", "game piece", "crystal",
        "tent", "house roof", "pyramid monument", "prism sculpture", "art installation",
        "package", "jewelry box", "music box", "toy block", "display case"
    ]
    
    for i in range(variations_needed):
        # Randomly select a template to base the variation on
        template = random.choice(templates)
        variation = copy.deepcopy(template)
        
        # Determine if this is a "which net" or "which figure" question
        is_which_net = "Which net will make" in template['question_text']
        
        # Select random shape for this variation
        shape_name = random.choice(list(shapes_data.keys()))
        shape_info = shapes_data[shape_name]
        
        # Select incorrect shape for wrong answer
        incorrect_shapes = [s for s in shapes_data.keys() if s != shape_name]
        incorrect_shape = random.choice(incorrect_shapes)
        incorrect_info = shapes_data[incorrect_shape]
        
        # Add theme context occasionally (30% of the time)
        context = ""
        if random.random() < 0.3:
            theme = random.choice(themes)
            context = f" for a {theme}"
        
        # Update question text
        if is_which_net:
            variation['question_text'] = f"Which net will make this figure{context}?"
            variation['backend_description'] = shape_info['description']
            
            # Update image choices descriptions
            if 'image_choice_tags_backend_description' in variation:
                # Randomize correct answer position
                correct_pos = random.choice([0, 1])
                if correct_pos == 0:
                    variation['image_choice_tags_backend_description'] = [
                        f"This image shows {shape_info['net_description']}, with dashed fold lines. This is the correct net for a {shape_name}.",
                        f"This image shows {incorrect_info['net_description']}. This is not the correct net."
                    ]
                    variation['correct_answers'] = ['A']
                else:
                    variation['image_choice_tags_backend_description'] = [
                        f"This image shows {incorrect_info['net_description']}. This is not the correct net.",
                        f"This image shows {shape_info['net_description']}, with dashed fold lines. This is the correct net for a {shape_name}."
                    ]
                    variation['correct_answers'] = ['B']
        else:
            variation['question_text'] = f"Which figure will this net make{context}?"
            variation['backend_description'] = f"This image shows {shape_info['net_description']}. This is a 2D layout that can be folded along the dashed lines to form a 3D {shape_name} shape."
            
            # Update image choices descriptions
            if 'image_choice_tags_backend_description' in variation:
                # Randomize correct answer position
                correct_pos = random.choice([0, 1])
                if correct_pos == 0:
                    variation['image_choice_tags_backend_description'] = [
                        f"This image shows a {shape_name}, which has {shape_info['faces']}.",
                        f"This image shows a {incorrect_shape}, which has {incorrect_info['faces']}."
                    ]
                    variation['correct_answers'] = ['A']
                else:
                    variation['image_choice_tags_backend_description'] = [
                        f"This image shows a {incorrect_shape}, which has {incorrect_info['faces']}.",
                        f"This image shows a {shape_name}, which has {shape_info['faces']}."
                    ]
                    variation['correct_answers'] = ['B']
        
        # Update solution text
        if 'solution' in variation:
            new_solution = []
            for step in variation['solution']:
                if len(step) >= 2:
                    step_num = step[0]
                    step_text = step[1]
                    
                    # Update solution text based on shape
                    if "Imagine folding" in step_text:
                        new_solution.append([step_num, "Imagine folding this net along the dotted lines."])
                    elif "makes a" in step_text and "correct" in step_text:
                        new_solution.append([step_num, f"When folded, this net makes a {shape_name}. This is the correct answer."])
                    elif "makes a" in step_text and "not the correct" in step_text:
                        new_solution.append([step_num, f"When folded, this net makes a {incorrect_shape}. This is not the correct answer."])
                    elif "makes a" in step_text:
                        new_solution.append([step_num, f"This net makes a {shape_name}."])
                    else:
                        new_solution.append(step)
            variation['solution'] = new_solution
        
        # Update question number for variation
        template_num = template['question_number'].split('_')[0]
        variation['question_number'] = f"{template_num}_{i+3}"
        
        # Update image tags
        if 'image_tag' in variation:
            variation['image_tag'] = f"Gr6_45_4_{i+3}"
        
        if 'image_choice_tags' in variation:
            variation['image_choice_tags'] = [
                f"Gr6_45_4_{i+3}_A",
                f"Gr6_45_4_{i+3}_B"
            ]
        
        if 'solution_image_tag' in variation:
            new_solution_images = []
            for img in variation['solution_image_tag']:
                new_img = img.copy()
                new_img[1] = f"Gr6_45_4_{i+3}_step_{img[0].split('/')[0]}"
                new_solution_images.append(new_img)
            variation['solution_image_tag'] = new_solution_images
        
        variations.append(variation)
    
    return variations

def main():
    """Main function to generate all variations"""
    templates_by_tag = load_templates()
    
    # Dictionary of generation functions
    generators = {
        'Gr6_45_E4': generate_Gr6_45_E4_variations,
        'Gr6_51_E3': generate_Gr6_51_E3_variations,
        'Gr6_51_E4': generate_Gr6_51_E4_variations,
        'Gr6_52_E1': generate_Gr6_52_E1_variations,
        'Gr6_52_E2': generate_Gr6_52_E2_variations,
        'Gr6_52_E3': generate_Gr6_52_E3_variations,
        'Gr6_52_E4': generate_Gr6_52_E4_variations,
        'Gr6_53_E2': generate_Gr6_53_E2_variations,
        'Gr6_53_E3': generate_Gr6_53_E3_variations,
        'Gr6_53_E4': generate_Gr6_53_E4_variations,
        'Gr6_54_E1': generate_Gr6_54_E1_variations
    }
    
    # Generate variations for each tag
    for tag, templates in templates_by_tag.items():
        if tag in generators:
            print(f"Generating variations for {tag}...")
            variations = generators[tag](templates)
            
            # Save variations to file
            filename = f"{tag}_variations.json"
            with open(filename, 'w') as f:
                json.dump(variations, f, indent=2)
            
            print(f"Created {len(variations)} variations for {tag}")
            print(f"Total for {tag}: {len(templates)} templates + {len(variations)} variations = {len(templates) + len(variations)}")
        else:
            print(f"No generator found for {tag}")
    
    print("\nAll variations generated successfully!")

if __name__ == "__main__":
    main()
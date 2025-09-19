import json
import random
import copy
from fractions import Fraction

def load_templates():
    """Load all template questions from the current file"""
    with open(r'C:\Users\kapil\numi-scraper\file.json', 'r') as f:
        content = f.read().strip().rstrip(',')
        if not content.startswith('['):
            content = '[' + content + ']'
        data = json.loads(content)
    return data

def generate_gr7_22_e1_variations(templates):
    """Generate variations for dividing fractions"""
    variations = []

    # Generate 50 new variations (1_2 through 1_51)
    for i in range(2, 52):
        var = copy.deepcopy(templates[0])

        # Generate random whole number and fraction
        whole = random.randint(2, 12)
        num = random.randint(1, 5)
        denom = random.randint(2, 8)

        # Calculate result
        result = whole * denom / num

        var['question_text'] = f"Divide.\\n\\n{whole} dollars ÷ {num}/{denom} = \\_\\_\\_\\_ $\\n\\n"

        # Format result
        if result.is_integer():
            var['correct_answers'] = [[str(int(result))], [f"{int(result)}/1"], [f"{result:.1f}"]]
        else:
            # Convert to fraction
            frac = Fraction(whole * denom, num)
            var['correct_answers'] = [[str(frac)], [str(float(frac))]]

        # Update solution
        var['solution'] = [
            ["1/4", f"You are dividing {whole} by $\\frac{{{num}}}{{{denom}}}$.\\n{whole} dollars ÷ \\frac{{{num}}}{{{denom}}}$."],
            ["2/4", f"To divide by a fraction, multiply by its reciprocal. The reciprocal of $\\frac{{{num}}}{{{denom}}}$ is $\\frac{{{denom}}}{{{num}}}$."],
            ["3/4", f"So, {whole} dollars ÷ \\frac{{{num}}}{{{denom}}} = {whole} x \\frac{{{denom}}}{{{num}}} = {result:.2f}$."],
            ["4/4", f"Therefore, {whole} dollars ÷ \\frac{{{num}}}{{{denom}}} = {result:.2f}$."]
        ]

        var['question_number'] = f"1_{i}"
        variations.append(var)

    return variations

def generate_gr7_22_e2_variations(templates):
    """Generate word problem variations for dividing fractions with pop culture themes"""
    variations = []

    themes = [
        ("wizard", "potion ingredients", "cauldrons"),
        ("chef", "special sauce", "pizza slices"),
        ("Pokemon trainer", "rare candies", "Pokemon"),
        ("Minecraft player", "diamonds", "chests"),
        ("superhero", "power crystals", "team members"),
        ("Jedi", "kyber crystals", "lightsabers"),
        ("ninja", "smoke bombs", "missions"),
        ("pirate", "treasure map pieces", "crew members"),
        ("astronaut", "oxygen tanks", "space stations"),
        ("alchemist", "philosopher's stones", "apprentices"),
    ]

    # Generate 50 new variations
    for i in range(2, 52):
        var = copy.deepcopy(templates[0])

        theme = random.choice(themes)
        profession, item, recipients = theme

        # Generate fractions
        num = random.randint(1, 5)
        denom = random.randint(2, 8)
        divisor = random.randint(2, 8)

        # Calculate result
        result = Fraction(num, denom * divisor)

        var['question_text'] = f"A {profession} spread $\\frac{{{num}}}{{{denom}}}$ of a bag of {item} evenly over {divisor} equal-sized {recipients}.\\n\\nHow much {item} did they put on each {recipients[:-1]}?\\n\\nWrite your answer as a fraction or as a whole or mixed number.\\n\\n"

        # Format answer
        if result.denominator == 1:
            var['correct_answers'] = [[str(result.numerator)]]
        else:
            var['correct_answers'] = [[f"{result.numerator}/{result.denominator}"], [str(float(result))]]

        # Update solution image tags
        var['solution_image_tag'] = [
            ["1/4", f"Gr7_22_2_{i}_step_1", f"Shows the division problem: {num}/{denom} ÷ {divisor}. The {profession} is dividing {num}/{denom} bag of {item} among {divisor} {recipients}."],
            ["2/4", f"Gr7_22_2_{i}_step_2", f"Shows converting {divisor} to a fraction: {divisor} = {divisor}/1. This allows the division to be rewritten as fraction ÷ fraction."],
            ["3/4", f"Gr7_22_2_{i}_step_3", f"Shows converting division to multiplication by the reciprocal: {num}/{denom} ÷ {divisor}/1 = {num}/{denom} x 1/{divisor}. The reciprocal of {divisor}/1 is 1/{divisor}."],
            ["4/4", f"Gr7_22_2_{i}_step_4", f"Shows the final multiplication: {num}/{denom} x 1/{divisor} = {result.numerator}/{result.denominator}. Multiplying the numerators and denominators gives the answer."]
        ]

        # Update solution
        var['solution'] = [
            ["1/4", f"The {profession} used {num}/{denom} of a bag of {item} and spread it evenly over {divisor} {recipients}. So we divide:."],
            ["2/4", f"To divide by a whole number, turn it into a fraction:\\n"],
            ["3/4", f"Now multiply by the reciprocal of {divisor}/1, which is 1/{divisor}:\\n"],
            ["4/4", f"So, the {profession} used {result.numerator}/{result.denominator} of a bag of {item} for each {recipients[:-1]}.\\n"]
        ]

        var['question_number'] = f"2_{i}"
        variations.append(var)

    return variations

def generate_gr7_22_e3_variations(templates):
    """Generate variations for dividing mixed numbers"""
    variations = []

    # Generate 50 new variations
    for i in range(2, 52):
        var = copy.deepcopy(templates[0])

        # Generate mixed number and fraction
        whole = random.randint(1, 5)
        num1 = random.randint(1, 4)
        denom1 = random.randint(2, 6)

        num2 = random.randint(1, 7)
        denom2 = random.randint(2, 8)

        # Convert mixed to improper
        improper_num = whole * denom1 + num1

        # Calculate result
        result_num = improper_num * denom2
        result_denom = denom1 * num2
        result = Fraction(result_num, result_denom)

        # Format as mixed number if needed
        if result > 1:
            whole_part = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            mixed_str = f"{whole_part} {remainder}/{result.denominator}"
        else:
            mixed_str = f"{result.numerator}/{result.denominator}"

        var['image_tag'] = f"Gr7_22_3_{i}"
        var['backend_description'] = f"Shows the division problem {whole} {num1}/{denom1} ÷ {num2}/{denom2} with an empty box for the answer."

        var['correct_answers'] = [[mixed_str], [f"{result.numerator}/{result.denominator}"]]

        # Update solution image tags
        var['solution_image_tag'] = [
            ["1/4", f"Gr7_22_3_{i}_step_1", f"Shows converting the mixed number {whole} {num1}/{denom1} to an improper fraction: {improper_num}/{denom1}."],
            ["2/4", f"Gr7_22_3_{i}_step_2", f"Shows converting division to multiplication by the reciprocal: {improper_num}/{denom1} ÷ {num2}/{denom2} = {improper_num}/{denom1} x {denom2}/{num2}."],
            ["3/4", f"Gr7_22_3_{i}_step_3", f"Shows the multiplication and simplification process."],
            ["4/4", f"Gr7_22_3_{i}_step_4", f"Shows converting the result to a mixed number if applicable."]
        ]

        var['question_number'] = f"3_{i}"
        variations.append(var)

    return variations

def generate_gr7_22_e4_variations(templates):
    """Generate word problem variations for dividing fractions and mixed numbers"""
    variations = []

    themes = [
        ("veterinarian", "medicine", "cats", "sick"),
        ("doctor", "vaccine", "patients", "ill"),
        ("coach", "energy drink", "players", "tired"),
        ("teacher", "bonus points", "students", "struggling"),
        ("baker", "special frosting", "cakes", "decorated"),
        ("scientist", "experimental serum", "test subjects", "selected"),
    ]

    # Generate 50 new variations
    for i in range(2, 52):
        var = copy.deepcopy(templates[0])

        theme = random.choice(themes)
        profession, item, recipients, adjective = theme

        # Generate fractions
        num = random.randint(2, 7)
        denom = random.randint(3, 10)
        divisor = random.randint(2, 6)

        # Calculate result
        result = Fraction(num, denom * divisor)

        var['question_text'] = f"A {profession} divided $\\frac{{{num}}}{{{denom}}}$ of a bottle of {item} equally among {divisor} {adjective} {recipients}. How much did they give each {adjective} {recipients[:-1]}?\\n\\nWrite your answer as a fraction or as a whole or mixed number.\\n\\n"

        # Format answer
        var['correct_answers'] = [[f"{result.numerator}/{result.denominator}"]]
        if float(result) == round(float(result), 2):
            var['correct_answers'].append([str(float(result))])

        # Update solution image tags and solution text
        var['solution_image_tag'] = [
            ["1/4", f"Gr7_22_4_{i}_step_1", f"Shows the division problem: {num}/{denom} ÷ {divisor}."],
            ["2/4", f"Gr7_22_4_{i}_step_2", f"Shows converting to multiplication by the reciprocal."],
            ["3/4", f"Gr7_22_4_{i}_step_3", f"Shows the simplification process."],
            ["4/4", f"Gr7_22_4_{i}_step_4", f"Shows the final answer: {result.numerator}/{result.denominator}."]
        ]

        var['question_number'] = f"4_{i}"
        variations.append(var)

    return variations

def generate_gr7_23_variations(templates, tag):
    """Generate variations for decimal multiplication problems"""
    variations = []

    template = templates[0]

    if "E2" in tag:  # Word problems with decimals
        themes = [
            ("metal ball", "weighs", "grams"),
            ("gold coin", "weighs", "ounces"),
            ("magic crystal", "contains", "mana points"),
            ("power cell", "stores", "energy units"),
            ("potion vial", "holds", "milliliters"),
        ]

        for i in range(2, 52):
            var = copy.deepcopy(template)

            theme = random.choice(themes)
            item, verb, unit = theme

            decimal = round(random.uniform(0.1, 9.9), 1)
            multiplier = random.randint(2, 12)
            result = round(decimal * multiplier, 2)

            var['question_text'] = f"Each {item} {verb} {decimal} {unit}. How much do {multiplier} {item}s {verb[:-1]} in all?\\n\\n"

            var['correct_answers'] = [[str(result)], [f"{result:.2f}"]]

            var['solution_image_tag'] = [
                ["2/5", f"Gr7_23_2_{i}_step_2", f"Shows the multiplication calculation: {decimal} x {multiplier}."]
            ]

            var['question_number'] = f"2_{i}"
            variations.append(var)

    elif "E3" in tag:  # Decimal multiplication with visual model
        for i in range(2, 52):
            var = copy.deepcopy(template)

            dec1 = round(random.uniform(0.1, 0.9), 1)
            dec2 = round(random.uniform(0.1, 0.9), 1)
            result = round(dec1 * dec2, 2)

            var['question_text'] = f"The model shows {dec1} x {dec2}.\\n\\nMultiply.\\n\\n{dec1} dollars x {dec2} = \\_\\_\\_\\_$"
            var['image_tag'] = f"Gr7_23_3_{i}"
            var['backend_description'] = f"Shows a 10x10 grid representing 1 whole. The visual model displays {dec1} x {dec2}."

            var['correct_answers'] = [str(result)]

            var['question_number'] = f"3_{i}"
            variations.append(var)

    else:  # E1 - multiply decimal by multi-digit whole number
        for i in range(2, 52):
            var = copy.deepcopy(template)

            decimal = round(random.uniform(0.1, 99.9), 1)
            whole = random.randint(10, 99)
            result = round(decimal * whole, 2)

            var['question_text'] = f"Multiply:\\n\\n{decimal} dollars x {whole} = \\_\\_\\_\\_$\\n\\n"

            var['correct_answers'] = [[str(result)], [f"{result:.2f}"]]

            var['question_number'] = f"1_{i}"
            variations.append(var)

    return variations[:50]  # Return only 50 variations

def generate_gr7_24_variations(templates, tag):
    """Generate variations for decimal division problems"""
    variations = []

    template = templates[0]

    if "E1" in tag:  # Divide decimals by whole numbers
        for i in range(2, 52):
            var = copy.deepcopy(template)

            # Generate decimal with 2 decimal places
            decimal = round(random.uniform(100.00, 999.99), 2)
            divisor = random.randint(2, 9)
            result = round(decimal / divisor, 3)

            var['question_text'] = f"Divide. Give the exact answer, written as a decimal.\\n\\n{decimal} dollars ÷ {divisor} = \\_\\_\\_\\_$\\n\\n"
            var['correct_answers'] = [str(result)]

            var['solution_image_tag'] = [
                ["1/8", f"Gr7_24_1_{i}_step_1", f"Shows the long division setup for {decimal} ÷ {divisor}."]
            ]

            var['question_number'] = f"1_{i}"
            variations.append(var)

    elif "E2" in tag:  # Word problems
        themes = [
            ("cafeteria", "beans", "batches of chili", "kilograms"),
            ("factory", "metal", "car parts", "pounds"),
            ("bakery", "flour", "batches of bread", "kilograms"),
            ("laboratory", "chemicals", "experiments", "liters"),
        ]

        for i in range(2, 52):
            var = copy.deepcopy(template)

            theme = random.choice(themes)
            place, material, product, unit = theme

            total = round(random.uniform(100.00, 999.99), 2)
            divisor = random.randint(4, 12)
            result = round(total / divisor, 4)

            var['question_text'] = f"A {place} used {total} {unit} of {material} to make {divisor} {product}. What quantity of {material} went into each one?\\n"
            var['correct_answers'] = [str(result)]

            var['question_number'] = f"2_{i}"
            variations.append(var)

    elif "E3" in tag:  # Division with visual
        for i in range(2, 52):
            var = copy.deepcopy(template)

            decimal = round(random.uniform(10.0, 99.9), 1)
            divisor = random.randint(2, 9)
            result = round(decimal / divisor, 2)

            var['image_tag'] = f"Gr7_24_3_{i}"
            var['backend_description'] = f"Shows the division problem {decimal} ÷ {divisor} with an empty box for the answer."

            var['correct_answers'] = [[str(result)], [f"{result:.2f}"]]

            var['question_number'] = f"3_{i}"
            variations.append(var)

    return variations[:50]

def generate_gr7_25_variations(templates, tag):
    """Generate variations for proportions problems"""
    variations = []

    template = templates[0]

    if "E1" in tag:  # Do ratios form a proportion
        for i in range(2, 52):
            var = copy.deepcopy(template)

            # Generate two ratios
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            d = random.randint(1, 10)

            # Check if they form a proportion
            forms_proportion = (a * d == b * c)

            var['question_text'] = f"Do the ratios $\\frac{{{a}}}{{{b}}}$ and $\\frac{{{c}}}{{{d}}}$ form a proportion?"
            var['correct_answers'] = ["A" if forms_proportion else "B"]

            var['question_number'] = f"1_{i}"
            variations.append(var)

    elif "E2" in tag:  # Word problems - do ratios form proportion
        items = [
            ("rakes", "lawnmowers"),
            ("pencils", "erasers"),
            ("apples", "oranges"),
            ("books", "shelves"),
            ("cars", "parking spaces"),
        ]

        for i in range(2, 52):
            var = copy.deepcopy(template)

            item1, item2 = random.choice(items)

            a = random.randint(2, 15)
            b = random.randint(2, 15)
            c = random.randint(2, 15)
            d = random.randint(2, 15)

            forms_proportion = (a * d == b * c)

            var['question_text'] = f"Do these ratios form a proportion?\\n\\n{a} {item1} to {b} {item2}\\n{c} {item1} to {d} {item2}"
            var['correct_answers'] = ["A" if forms_proportion else "B"]

            var['question_number'] = f"2_{i}"
            variations.append(var)

    elif "E3" in tag:  # Solve proportions
        for i in range(2, 52):
            var = copy.deepcopy(template)

            # Generate proportion with solution
            a = random.randint(2, 30)
            b = random.randint(2, 20)
            c = random.randint(2, 20)
            # Calculate d so proportion is valid
            d = (a * c) // b

            var['question_text'] = f"Solve for $s$ in the proportion:\\n\\n$\\frac{{{a}}}{{s}} = \\frac{{{b}}}{{{c}}}$\\n\\n$s = \\_\\_\\_\\_$"
            var['correct_answers'] = [str(d)]

            var['solution_image_tag'] = [
                ["1/5", f"Gr7_25_3_{i}_step_1", f"Shows the proportion equation: {a}/s = {b}/{c}."],
                ["2/5", f"Gr7_25_3_{i}_step_2", f"Shows the cross multiplication setup."],
                ["3/5", f"Gr7_25_3_{i}_step_3", f"Shows the simplified equation."],
                ["4/5", f"Gr7_25_3_{i}_step_4", f"Shows solving for s."]
            ]

            var['question_number'] = f"3_{i}"
            variations.append(var)

    elif "E4" in tag:  # Proportion word problems
        contexts = [
            ("took notes", "pages", "hours of class"),
            ("read", "pages", "minutes"),
            ("typed", "words", "minutes"),
            ("solved", "problems", "hours"),
        ]

        for i in range(2, 52):
            var = copy.deepcopy(template)

            context = random.choice(contexts)
            action, item1, item2 = context

            # Generate proportional relationship
            rate = random.randint(2, 5)
            initial_items = random.randint(10, 30)
            initial_time = initial_items // rate

            target_items = initial_items + random.randint(5, 20)
            target_time = target_items // rate

            var['question_text'] = f"A student {action} a total of {initial_items} {item1} during {initial_time} {item2}.\\n\\nIn all, how many {item2} will the student need before they will have a total of {target_items} {item1}?\\n\\nAssume the relationship is directly proportional.\\n"
            var['correct_answers'] = [str(target_time)]

            var['question_number'] = f"4_{i}"
            variations.append(var)

    return variations[:50]

def save_variations(variations, tag):
    """Save variations to JSON file"""
    filename = f"C:\\Users\\kapil\\numi-scraper\\{tag} variations.json"
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Saved {len(variations)} variations to {filename}")

def main():
    # Load all templates
    all_templates = load_templates()

    # Process each tag group
    tag_groups = {}
    for q in all_templates:
        if 'tag' in q:
            tag = q['tag']
            if tag not in tag_groups:
                tag_groups[tag] = []
            tag_groups[tag].append(q)

    print(f"Found {len(tag_groups)} unique tags")

    # Generate variations for each tag
    for tag, templates in sorted(tag_groups.items()):
        print(f"\nProcessing {tag} with {len(templates)} template(s)")

        # Calculate how many new variations needed
        total_needed = 51
        num_new = total_needed - len(templates)

        variations = []

        if tag == "Gr7_22_E1":
            variations = generate_gr7_22_e1_variations(templates)
        elif tag == "Gr7_22_E2":
            variations = generate_gr7_22_e2_variations(templates)
        elif tag == "Gr7_22_E3":
            variations = generate_gr7_22_e3_variations(templates)
        elif tag == "Gr7_22_E4":
            variations = generate_gr7_22_e4_variations(templates)
        elif tag.startswith("Gr7_23"):
            variations = generate_gr7_23_variations(templates, tag)
        elif tag.startswith("Gr7_24"):
            variations = generate_gr7_24_variations(templates, tag)
        elif tag.startswith("Gr7_25"):
            variations = generate_gr7_25_variations(templates, tag)
        else:
            print(f"Skipping {tag} - needs custom implementation")
            continue

        # Ensure we have the right number of variations
        variations = variations[:num_new]

        if variations:
            save_variations(variations, tag)

if __name__ == "__main__":
    main()
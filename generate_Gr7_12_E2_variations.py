import json
import random
import copy

def load_templates():
    """Load template questions from the original file"""
    with open(r'C:\Users\kapil\numi-scraper\file.json', 'r') as f:
        content = f.read().strip().rstrip(',')
        content = '[' + content + ']'
        data = json.loads(content)

    # Filter for Gr7_12_E2 templates
    templates = [q for q in data if q.get('tag') == 'Gr7_12_E2']
    return templates

def generate_variations(templates, num_variations=49):
    """Generate variations for adding/subtracting integers"""
    variations = []

    # Operations for variations (avoiding template values)
    operations = []

    # Create diverse operations with subtraction of negatives and regular additions
    for a in range(-10, 11):
        for b in range(-10, 11):
            # Skip if this matches any template
            if (a == 2 and b == -3) or (a == -4 and b == 3):
                continue
            # Add interesting operations
            operations.append((a, b, 'subtract' if b < 0 and random.random() > 0.5 else 'add'))

    # Shuffle and select 49 unique operations
    random.shuffle(operations)
    selected_ops = operations[:49]

    # Generate 49 new variations (2_3 through 2_51 and 2_2 through 2_50 based on template)
    for i in range(3, 52):
        template_idx = random.randint(0, len(templates) - 1)
        template = templates[template_idx]
        var = copy.deepcopy(template)

        # Get operation for this variation
        op_idx = i - 3
        a, b, op_type = selected_ops[op_idx]

        # Update question text based on operation type
        if op_type == 'subtract' and b < 0:
            # Subtracting a negative
            var['question_text'] = f"Subtract:\\n\\n{a} dollars - ({b}) = \\_\\_\\_\\_$\\n\\n"
            result = a - b
        else:
            # Regular addition
            var['question_text'] = f"Add:\\n\\n{a} + {b} = ____\\n"
            result = a + b

        # Update correct answer
        var['correct_answers'] = [str(result)]

        # Update solution based on operation type
        if op_type == 'subtract' and b < 0:
            var['solution'] = [
                ["1/4", f"We are subtracting a negative number: {a} - ({b})."],
                ["2/4", f"Subtracting a negative is the same as adding: {a} - ({b}) = {a} + {abs(b)}."],
                ["3/4", f"Now add: {a} + {abs(b)} = {result}."],
                ["4/4", f"So, {a} - ({b}) = {result}."]
            ]
        else:
            # Regular addition solution
            if (a < 0 and b > 0) or (a > 0 and b < 0):
                # Mixed signs
                abs_a = abs(a)
                abs_b = abs(b)
                diff = abs(abs_a - abs_b)
                var['solution'] = [
                    ["1/4", f"We are solving {a} + {b}."],
                    ["2/4", f"One number is {'negative' if a < 0 else 'positive'} ({a}) and one is {'positive' if b > 0 else 'negative'} ({b}).\\nTo solve, find the difference between {abs_a} and {abs_b}: {max(abs_a, abs_b)} - {min(abs_a, abs_b)} = {diff}."],
                    ["3/4", f"Since {abs_a if abs_a > abs_b else abs_b} is bigger than {abs_b if abs_a > abs_b else abs_a} and it's {'negative' if (abs_a > abs_b and a < 0) or (abs_b > abs_a and b < 0) else 'positive'}, the final answer will be {'negative' if result < 0 else 'positive'}."],
                    ["4/4", f"So, {a} + {b} = {result}."]
                ]
            elif a < 0 and b < 0:
                # Both negative
                var['solution'] = [
                    ["1/4", f"We are solving {a} + {b}."],
                    ["2/4", f"Both numbers are negative. When adding negative numbers, add their absolute values: {abs(a)} + {abs(b)} = {abs(a) + abs(b)}."],
                    ["3/4", f"Since both numbers are negative, the result is negative."],
                    ["4/4", f"So, {a} + {b} = {result}."]
                ]
            else:
                # Both positive
                var['solution'] = [
                    ["1/4", f"We are solving {a} + {b}."],
                    ["2/4", f"Both numbers are positive. Simply add them together."],
                    ["3/4", f"{a} + {b} = {result}."],
                    ["4/4", f"So, {a} + {b} = {result}."]
                ]

        # Update question number
        var['question_number'] = f"{template_idx + 1}_{i}"

        variations.append(var)

    return variations

def save_variations(variations, tag):
    """Save variations to JSON file"""
    filename = f"{tag} variations.json"
    with open(filename, 'w') as f:
        json.dump(variations, f, indent=2)
    print(f"Saved {len(variations)} variations to {filename}")

def main():
    # Load templates
    templates = load_templates()
    print(f"Loaded {len(templates)} template(s) for Gr7_12_E2")

    # Generate variations
    variations = generate_variations(templates)

    # Save to file
    save_variations(variations, "Gr7_12_E2")

if __name__ == "__main__":
    main()
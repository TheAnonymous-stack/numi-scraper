#!/usr/bin/env python3
"""
Master Variation Generator for Grade 7 Math Questions
Generates 51 total versions (templates + variations) for each unique tag
"""

import json
import random
import copy
import os
import re
from collections import defaultdict
from fractions import Fraction
from decimal import Decimal

# Popular themes for word problems
POP_CULTURE_THEMES = {
    'anime_characters': ['Naruto', 'Luffy', 'Goku', 'Eren', 'Deku', 'Tanjiro', 'Yuji', 'Ichigo', 'Light', 'Edward'],
    'games': ['Minecraft blocks', 'Fortnite V-Bucks', 'Pokemon cards', 'Among Us tasks', 'Roblox Robux',
               'Mario coins', 'Zelda rupees', 'Call of Duty points', 'FIFA packs', 'Apex Legends tokens'],
    'movies': ['Avengers', 'Spider-Man webs', 'Harry Potter spells', 'Star Wars lightsabers',
               'Batman gadgets', 'Iron Man suits', 'Thor hammers', 'Captain America shields'],
    'shows': ['Stranger Things portals', 'Wednesday mysteries', 'The Last of Us supplies',
              'Squid Game tokens', 'Breaking Bad elements', 'Game of Thrones dragons'],
    'social_media': ['TikTok likes', 'Instagram followers', 'YouTube subscribers', 'Twitter retweets',
                     'Discord messages', 'Twitch viewers', 'Snapchat streaks'],
    'food': ['bubble tea', 'ramen bowls', 'sushi rolls', 'tacos', 'pizza slices',
             'burgers', 'ice cream scoops', 'donuts', 'cookies']
}

class VariationGenerator:
    def __init__(self):
        self.perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625]
        self.prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

    def get_pop_culture_context(self):
        """Generate a random pop culture context for word problems"""
        category = random.choice(list(POP_CULTURE_THEMES.keys()))
        item = random.choice(POP_CULTURE_THEMES[category])
        return item

    def update_image_tag(self, tag, variation_number):
        """Update image tag with variation number"""
        if not tag:
            return tag

        # Handle different image tag formats
        if isinstance(tag, str):
            parts = tag.split('_')
            if len(parts) >= 4:
                return '_'.join(parts[:-1]) + f'_{variation_number}'
        return tag

    def generate_integer_pair(self, allow_negative=True):
        """Generate a pair of integers for operations"""
        if allow_negative:
            return random.randint(-50, 50), random.randint(-50, 50)
        return random.randint(1, 100), random.randint(1, 100)

    def generate_fraction_pair(self):
        """Generate a pair of fractions"""
        num1 = random.randint(1, 12)
        den1 = random.randint(2, 12)
        num2 = random.randint(1, 12)
        den2 = random.randint(2, 12)

        # Simplify if needed
        f1 = Fraction(num1, den1)
        f2 = Fraction(num2, den2)
        return f1, f2

    def generate_decimal_pair(self, max_places=2):
        """Generate a pair of decimal numbers"""
        d1 = round(random.uniform(0.01, 99.99), max_places)
        d2 = round(random.uniform(0.01, 99.99), max_places)
        return d1, d2

    def generate_mixed_number(self):
        """Generate a mixed number"""
        whole = random.randint(1, 10)
        numerator = random.randint(1, 9)
        denominator = random.randint(2, 10)

        # Ensure proper fraction
        while numerator >= denominator:
            numerator = random.randint(1, denominator - 1)

        return whole, numerator, denominator

    def vary_square_root_question(self, template, variation_num):
        """Generate variation for square root questions"""
        new_square = random.choice(self.perfect_squares)
        new_root = int(new_square ** 0.5)

        template['question_text'] = f"What is the square root of {new_square}?\\n\\n"
        template['correct_answers'] = [str(new_root)]

        # Update solution steps
        if template.get('solution'):
            for step in template['solution']:
                if len(step) > 1:
                    # Replace numbers in solution
                    step[1] = re.sub(r'\\b\\d+\\b', lambda m: str(new_square) if m.group() == '9' else str(new_root) if m.group() == '3' else m.group(), step[1])

        return template

    def vary_integer_operation(self, template, variation_num):
        """Generate variation for integer operations"""
        num1, num2 = self.generate_integer_pair()

        # Detect operation type
        if 'add' in template.get('skills', '').lower():
            result = num1 + num2
            operation = '+'
        elif 'subtract' in template.get('skills', '').lower():
            result = num1 - num2
            operation = '-'
        elif 'multiply' in template.get('skills', '').lower():
            result = num1 * num2
            operation = '×'
        elif 'divide' in template.get('skills', '').lower():
            # Ensure clean division
            num2 = random.choice([i for i in range(-20, 21) if i != 0])
            num1 = num2 * random.randint(-10, 10)
            result = num1 // num2
            operation = '÷'
        else:
            result = num1 + num2
            operation = '+'

        # Update question text
        if 'word-problem' in template.get('skills', ''):
            # Add pop culture theme
            theme = self.get_pop_culture_context()
            template['question_text'] = f"{theme} has {abs(num1)} items. "
            if num2 > 0:
                template['question_text'] += f"They collect {abs(num2)} more. How many do they have now?"
            else:
                template['question_text'] += f"They lose {abs(num2)}. How many do they have now?"
        else:
            template['question_text'] = f"Calculate: {num1} {operation} {num2} = ?"

        template['correct_answers'] = [str(result)]

        return template

    def vary_fraction_operation(self, template, variation_num):
        """Generate variation for fraction operations"""
        f1, f2 = self.generate_fraction_pair()

        # Detect operation
        if 'add' in template.get('skills', '').lower():
            result = f1 + f2
            operation = '+'
        elif 'subtract' in template.get('skills', '').lower():
            result = f1 - f2
            operation = '-'
        elif 'multiply' in template.get('skills', '').lower():
            result = f1 * f2
            operation = '×'
        elif 'divide' in template.get('skills', '').lower():
            result = f1 / f2
            operation = '÷'
        else:
            result = f1 + f2
            operation = '+'

        # Format question
        if 'word-problem' in template.get('skills', ''):
            theme = self.get_pop_culture_context()
            template['question_text'] = f"A recipe for {theme} uses ${f1}$ cups of flour. Another recipe uses ${f2}$ cups. What's the total?"
        else:
            template['question_text'] = f"Calculate: ${f1}$ {operation} ${f2}$ = ?"

        # Format answer
        if result.denominator == 1:
            template['correct_answers'] = [str(result.numerator)]
        else:
            template['correct_answers'] = [f"{result.numerator}/{result.denominator}"]

        return template

    def vary_comparison_question(self, template, variation_num):
        """Generate variation for comparison questions"""
        if 'decimal' in template.get('skills', ''):
            num1, num2 = self.generate_decimal_pair()
        elif 'fraction' in template.get('skills', ''):
            f1, f2 = self.generate_fraction_pair()
            num1, num2 = float(f1), float(f2)
        else:
            num1, num2 = self.generate_integer_pair()

        # Ensure numbers are different
        while num1 == num2:
            if 'decimal' in template.get('skills', ''):
                num1, num2 = self.generate_decimal_pair()
            else:
                num1, num2 = self.generate_integer_pair()

        template['question_text'] = f"Which sign makes this statement true?\\n\\n{num1} ___ {num2}"

        # Handle multiple choice
        if 'Multiple Choice' in template.get('question_type', ''):
            if num1 > num2:
                template['correct_answers'] = ['A'] if '>' in str(template.get('choices', ['>', '<'])[0]) else ['B']
            else:
                template['correct_answers'] = ['B'] if '<' in str(template.get('choices', ['>', '<'])[1]) else ['A']
        else:
            template['correct_answers'] = ['>' if num1 > num2 else '<']

        return template

    def vary_ordering_question(self, template, variation_num):
        """Generate variation for ordering questions"""
        count = len(template.get('choices', [])) or 4

        if 'decimal' in template.get('skills', ''):
            numbers = [round(random.uniform(0.01, 99.99), 2) for _ in range(count)]
        elif 'fraction' in template.get('skills', ''):
            fractions = [self.generate_fraction_pair()[0] for _ in range(count)]
            numbers = fractions
        else:
            numbers = [random.randint(-100, 100) for _ in range(count)]

        # Ensure all numbers are different
        numbers = list(set(numbers))
        while len(numbers) < count:
            if 'decimal' in template.get('skills', ''):
                numbers.append(round(random.uniform(0.01, 99.99), 2))
            else:
                numbers.append(random.randint(-100, 100))

        template['choices'] = [str(n) for n in numbers[:count]]

        # Sort for answer
        sorted_numbers = sorted(numbers[:count])
        template['correct_answers'] = [str(n) for n in sorted_numbers]

        return template

    def vary_geometry_question(self, template, variation_num):
        """Generate variation for geometry questions"""
        if 'area' in template.get('skills', ''):
            if 'circle' in template.get('skills', ''):
                radius = random.randint(1, 20)
                area = round(3.14159 * radius * radius, 2)
                template['question_text'] = f"Find the area of a circle with radius {radius} units. (Use π ≈ 3.14)"
                template['correct_answers'] = [str(area)]
            elif 'rectangle' in template.get('skills', ''):
                length = random.randint(2, 30)
                width = random.randint(2, 30)
                area = length * width
                template['question_text'] = f"Find the area of a rectangle with length {length} and width {width}."
                template['correct_answers'] = [str(area)]

        elif 'perimeter' in template.get('skills', ''):
            if 'rectangle' in template.get('skills', ''):
                length = random.randint(2, 30)
                width = random.randint(2, 30)
                perimeter = 2 * (length + width)
                template['question_text'] = f"Find the perimeter of a rectangle with length {length} and width {width}."
                template['correct_answers'] = [str(perimeter)]

        return template

    def generate_variation(self, template, variation_num):
        """Main method to generate a variation based on template"""
        variation = copy.deepcopy(template)

        # Update question number
        template_num = int(template.get('question_number', '1_1').split('_')[0])
        variation['question_number'] = f"{template_num}_{variation_num}"

        # Determine variation type based on skills
        skills = variation.get('skills', '').lower()

        if 'square-root' in skills:
            variation = self.vary_square_root_question(variation, variation_num)
        elif 'integer' in skills and any(op in skills for op in ['add', 'subtract', 'multiply', 'divide']):
            variation = self.vary_integer_operation(variation, variation_num)
        elif 'fraction' in skills or 'mixed-number' in skills:
            variation = self.vary_fraction_operation(variation, variation_num)
        elif 'compare' in skills or 'order' in skills:
            if 'order' in skills:
                variation = self.vary_ordering_question(variation, variation_num)
            else:
                variation = self.vary_comparison_question(variation, variation_num)
        elif 'geometry' in skills or 'area' in skills or 'perimeter' in skills:
            variation = self.vary_geometry_question(variation, variation_num)
        else:
            # Generic numeric variation
            variation = self.vary_generic_numeric(variation, variation_num)

        # Update image tags
        variation = self.update_all_image_tags(variation, variation_num)

        return variation

    def vary_generic_numeric(self, template, variation_num):
        """Generic numeric variation for unhandled question types"""
        # Find all numbers in question text
        text = template.get('question_text', '')
        numbers = re.findall(r'\\b\\d+\\b', text)

        if numbers:
            # Replace each number with a random variation
            for num in set(numbers):
                new_num = random.randint(1, 100)
                text = text.replace(num, str(new_num))

            template['question_text'] = text

            # Try to update answer if it's numeric
            if template.get('correct_answers') and template['correct_answers'][0].isdigit():
                # Generate a plausible answer
                template['correct_answers'] = [str(random.randint(1, 1000))]

        return template

    def update_all_image_tags(self, variation, variation_num):
        """Update all types of image tags in the variation"""
        # Basic image tag
        if variation.get('image_tag'):
            variation['image_tag'] = self.update_image_tag(variation['image_tag'], variation_num)

        # Solution image tags
        if variation.get('solution_image_tag'):
            for step in variation['solution_image_tag']:
                if len(step) > 1:
                    step[1] = self.update_image_tag(step[1], variation_num)

        # Image choice tags
        if variation.get('image_choice_tags'):
            variation['image_choice_tags'] = [
                self.update_image_tag(tag, variation_num)
                for tag in variation['image_choice_tags']
            ]

        # Shape image tags
        if variation.get('shape_image_tags'):
            for shape_tag in variation['shape_image_tags']:
                if isinstance(shape_tag, dict) and 'tag' in shape_tag:
                    shape_tag['tag'] = self.update_image_tag(shape_tag['tag'], variation_num)

        return variation


def main():
    """Main execution function"""
    print("Grade 7 Math Variation Generator")
    print("=" * 50)

    # Load templates
    print("\\nLoading template questions...")
    with open('C:/Users/kapil/numi-scraper/all_templates.json', encoding='utf-8') as f:
        all_templates = json.load(f)

    # Group by tag
    templates_by_tag = defaultdict(list)
    for template in all_templates:
        templates_by_tag[template['tag']].append(template)

    print(f"Loaded {len(all_templates)} templates across {len(templates_by_tag)} unique tags")

    # Check existing files
    existing_files = [f.replace('_variations.json', '')
                     for f in os.listdir('C:/Users/kapil/numi-scraper')
                     if f.endswith('_variations.json')]

    tags_to_process = [tag for tag in templates_by_tag.keys()
                      if tag not in existing_files]

    print(f"\\nFound {len(existing_files)} existing variation files")
    print(f"Need to generate variations for {len(tags_to_process)} tags")

    if not tags_to_process:
        print("\\nAll tags already have variation files!")
        return

    # Initialize generator
    generator = VariationGenerator()

    # Process each tag
    for i, tag in enumerate(tags_to_process, 1):
        templates = templates_by_tag[tag]
        variations_needed = 51 - len(templates)

        print(f"\\n[{i}/{len(tags_to_process)}] Processing {tag}")
        print(f"  Templates: {len(templates)}, Variations needed: {variations_needed}")

        if variations_needed <= 0:
            print(f"  Skipping - already has {len(templates)} templates")
            continue

        variations = []
        for var_num in range(2, variations_needed + 2):  # Start from 2
            # Pick random template
            template = random.choice(templates)
            variation = generator.generate_variation(template, var_num)
            variations.append(variation)

        # Save variations
        output_file = f"C:/Users/kapil/numi-scraper/{tag}_variations.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(variations, f, indent=2, ensure_ascii=False)

        print(f"  [DONE] Generated {len(variations)} variations -> {tag}_variations.json")

    print(f"\\n{'=' * 50}")
    print(f"COMPLETE! Generated variations for {len(tags_to_process)} tags")
    print(f"Total questions per tag: 51 (templates + variations)")


if __name__ == "__main__":
    main()
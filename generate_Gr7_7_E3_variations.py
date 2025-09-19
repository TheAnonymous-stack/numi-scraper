import json
import random
import copy
import math

def gcd(a, b):
    """Calculate the greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate the least common multiple"""
    return abs(a * b) // gcd(a, b)

def simplify_fraction(num, den):
    """Simplify a fraction to lowest terms"""
    g = gcd(num, den)
    return num // g, den // g

def generate_variations():
    # Load the fixed JSON file to get the template
    with open(r'C:\Users\kapil\numi-scraper\file_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    # Find the template with tag Gr7_7_E3
    template = None
    for item in data:
        if item.get('tag') == 'Gr7_7_E3':
            template = item
            break

    if not template:
        print("Template for Gr7_7_E3 not found")
        return

    variations = []

    # Pop culture themed word problems for fractions
    themes = [
        ("Spider-Man's Pizza Palace", "pepperoni pizzas", "mushroom pizzas"),
        ("Hogwarts Express Treats", "chocolate frog pies", "pumpkin pasties"),
        ("Krusty Krab Bakery", "Krabby patty pies", "kelp shake pies"),
        ("Wayne Enterprises Cafe", "Batman berry pies", "Gotham grape pies"),
        ("Stark Industries Diner", "arc reactor apple pies", "vibranium vanilla pies"),
        ("The Shire Bakehouse", "hobbit honey pies", "elvish elderberry pies"),
        ("Asgardian Feast Hall", "thunder berry pies", "frost giant fruit pies"),
        ("Jedi Temple Cafeteria", "force fruit pies", "lightsaber lemon pies"),
        ("Pokemon Center Kitchen", "Pikachu peach pies", "Charmander cherry pies"),
        ("Naruto's Ramen Shop", "ninja noodle pies", "shinobi strawberry pies"),
        ("Demon Slayer Dojo", "breathing technique blueberry pies", "hashira hazelnut pies"),
        ("My Hero Academy Cafe", "quirk quince pies", "hero hazelnut pies"),
        ("Attack on Titan Mess Hall", "scout strawberry pies", "garrison grape pies"),
        ("One Piece Galley", "devil fruit pies", "sea king salmon pies"),
        ("Dragon Ball Diner", "saiyan strawberry pies", "namekian nut pies"),
        ("Wakanda Royal Kitchen", "vibranium violet pies", "heart herb pies"),
        ("X-Men Mansion Kitchen", "mutant mango pies", "cerebro cherry pies"),
        ("Avengers Tower Cafe", "infinity stone pies", "quantum realm quiche"),
        ("Stranger Things Diner", "upside down pies", "demogorgon donuts"),
        ("Rick's Portal Pies", "interdimensional pies", "multiverse muffins"),
        ("Avatar Air Temple", "air nomad apple pies", "earth kingdom pies"),
        ("Fire Nation Palace", "dragon fruit pies", "phoenix pear pies"),
        ("Water Tribe Kitchen", "moon peach pies", "ocean orange pies"),
        ("Frozen's Arendelle Bakery", "ice crystal pies", "summer berry pies"),
        ("Encanto's Casita Kitchen", "miracle mango pies", "magic melon pies"),
        ("Moana's Island Feast", "ocean orange pies", "heart of Te Fiti pies"),
        ("Tangled Tower Kitchen", "golden sun pies", "lantern lemon pies"),
        ("Shrek's Swamp Shack", "ogre onion pies", "donkey date pies"),
        ("Toy Story Pizza Planet", "space ranger pies", "infinity pies"),
        ("Cars Radiator Springs", "piston cup pies", "route 66 raspberry pies"),
        ("Finding Nemo Reef Cafe", "clownfish coconut pies", "blue tang blueberry pies"),
        ("Incredibles Super Diner", "elastigirl elderberry pies", "dash date pies"),
        ("Ratatouille Restaurant", "chef's special pies", "Parisian plum pies"),
        ("Wall-E Space Station", "future fruit pies", "plant pies"),
        ("Up Paradise Falls Cafe", "adventure apple pies", "wilderness walnut pies"),
        ("Inside Out Mind Cafe", "joy jasmine pies", "memory mango pies"),
        ("Coco's Family Kitchen", "Day of Dead pies", "marigold mango pies"),
        ("Luca's Seaside Trattoria", "sea monster seafood pies", "vespa vanilla pies"),
        ("Turning Red Temple", "red panda raspberry pies", "4*Town toffee pies"),
        ("Jujutsu High Cafeteria", "cursed cherry pies", "domain expansion pies"),
        ("Chainsaw Devil Diner", "power peach pies", "contract coconut pies"),
        ("Spy x Family Kitchen", "secret strawberry pies", "mission mango pies"),
        ("Mob's Psychic Parlor", "ESP elderberry pies", "spirit strawberry pies"),
        ("Death Note Cafe", "shinigami apple pies", "justice jasmine pies"),
        ("Tokyo Ghoul Coffee Shop", "ghoul grape pies", "quinque quince pies"),
        ("Bleach Soul Society", "zanpakuto zest pies", "hollow hazelnut pies"),
        ("Fullmetal Bakery", "alchemy apple pies", "philosopher's stone pies"),
        ("Hunter Association", "nen nectarine pies", "greed island grape pies"),
        ("Fairy Tail Guild Hall", "dragon slayer pies", "celestial cherry pies"),
        ("Soul Eater Academy", "death scythe pies", "meister mango pies")
    ]

    # Generate 50 variations
    for i in range(2, 52):
        variation = copy.deepcopy(template)

        # Select random theme
        shop_name, type1, type2 = random.choice(themes)

        # Generate random fractions
        # Ensure denominators are reasonable and different
        denominators = [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30]
        den1, den2 = random.sample(denominators, 2)

        # Generate numerators that are less than denominators
        num1 = random.randint(1, den1 - 1)
        num2 = random.randint(1, den2 - 1)

        # Calculate the sum
        lcd = lcm(den1, den2)
        mult1 = lcd // den1
        mult2 = lcd // den2
        new_num1 = num1 * mult1
        new_num2 = num2 * mult2
        sum_num = new_num1 + new_num2

        # Simplify the result
        simplified_num, simplified_den = simplify_fraction(sum_num, lcd)

        # Format the answer
        if simplified_num < simplified_den:
            # Proper fraction
            answers = [[f"{simplified_num}/{simplified_den}"]]
        else:
            # Mixed number or whole number
            whole = simplified_num // simplified_den
            remainder = simplified_num % simplified_den
            if remainder == 0:
                answers = [[str(whole)]]
            else:
                remainder_simplified, den_simplified = simplify_fraction(remainder, simplified_den)
                answers = [[f"{whole} {remainder_simplified}/{den_simplified}"]]

        # Also accept the unsimplified version and decimal approximation
        answers.append([f"{sum_num}/{lcd}"])
        decimal_value = round(sum_num / lcd, 4)
        answers.append([str(decimal_value)])
        answers.append([str(round(decimal_value, 3))])
        answers.append([str(round(decimal_value, 2))])

        # Update question text
        variation['question_text'] = f"Of the pies that {shop_name} sold last month, $\\frac{{{num1}}}{{{den1}}}$ were {type1} and $\\frac{{{num2}}}{{{den2}}}$ were {type2}. What fraction of the pies sold were either {type1.split()[-1]} or {type2.split()[-1]}?\n\nWrite your answer as a fraction or as a whole or mixed number.\n"

        # Update correct answers
        variation['correct_answers'] = answers
        variation['has_alternative_answers'] = True

        # Generate prime factorizations for the solution
        def prime_factorization(n):
            factors = []
            d = 2
            while d * d <= n:
                while n % d == 0:
                    factors.append(d)
                    n //= d
                d += 1
            if n > 1:
                factors.append(n)
            return factors

        factors1 = prime_factorization(den1)
        factors2 = prime_factorization(den2)

        # Format factorizations
        if len(factors1) == 1:
            fact1_str = str(den1)
        else:
            fact1_str = " x ".join(map(str, factors1))

        if len(factors2) == 1:
            fact2_str = str(den2)
        else:
            fact2_str = " x ".join(map(str, factors2))

        # Calculate LCD explanation
        lcd_factors = []
        all_primes = set(factors1 + factors2)
        for p in sorted(all_primes):
            count = max(factors1.count(p), factors2.count(p))
            lcd_factors.extend([p] * count)
        lcd_str = " x ".join(map(str, lcd_factors))

        # Update solution
        variation['solution'] = [
            ["1/10", f"To find the fraction of pies that were either {type1.split()[-1]} or {type2.split()[-1]}, add $\\frac{{{num1}}}{{{den1}}}$ and $\\frac{{{num2}}}{{{den2}}}$."],
            ["2/10", f"To add these fractions, find the least common denominator (LCD) of {den1} and {den2}."],
            ["3/10", f"The prime factorization of {den1} is {fact1_str}, and for {den2} it is {fact2_str}."],
            ["4/10", f"Use each factor the greatest number of times it appears. Multiply them to get the LCD: {lcd_str} = {lcd}."],
            ["5/10", f"Convert each fraction to have a denominator of {lcd}."],
            ["6/10", ""],
            ["7/10", ""],
            ["8/10", "Now add the fractions:\n"],
            ["9/10", f"So, $\\frac{{{new_num1}}}{{{lcd}}} + \\frac{{{new_num2}}}{{{lcd}}} = \\frac{{{sum_num}}}{{{lcd}}}$.\n\n" + (f"This can be simplified to $\\frac{{{simplified_num}}}{{{simplified_den}}}$." if (simplified_num, simplified_den) != (sum_num, lcd) else "This fraction is already in simplest form.")],
            ["10/10", f"Therefore, $\\frac{{{simplified_num}}}{{{simplified_den}}}$ of the pies were either {type1.split()[-1]} or {type2.split()[-1]}."]
        ]

        # Update solution image tags
        variation['solution_image_tag'] = [
            ["6/10", f"Gr7_7_3_1_{i}_step_6", f"Shows the conversion of {num1}/{den1} to {new_num1}/{lcd} by multiplying both numerator and denominator by {mult1}. The visual equation helps students understand finding equivalent fractions with a common denominator."],
            ["7/10", f"Gr7_7_3_1_{i}_step_7", f"Shows the conversion of {num2}/{den2} to {new_num2}/{lcd} by multiplying both numerator and denominator by {mult2}. This creates the same denominator as the previous fraction for easy addition."],
            ["8/10", f"Gr7_7_3_1_{i}_step_8", f"Shows the final addition: {new_num1}/{lcd} + {new_num2}/{lcd} = {sum_num}/{lcd}. The calculation demonstrates adding fractions with like denominators by adding only the numerators."]
        ]

        # Update question number
        variation['question_number'] = f"3_{i}"

        variations.append(variation)

    # Save variations to JSON file
    with open(r'C:\Users\kapil\numi-scraper\Gr7_7_E3 variations.json', 'w', encoding='utf-8') as f:
        json.dump(variations, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(variations)} variations for Gr7_7_E3")

if __name__ == "__main__":
    generate_variations()
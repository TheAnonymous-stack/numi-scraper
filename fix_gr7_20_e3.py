import json
import re
from fractions import Fraction

def parse_amounts_from_question(question_text):
    """Extract the two amounts from the question text"""
    # Pattern to match fractions or whole numbers
    pattern = r'uses\s+\$([^$]+)\$\s+cups.*?uses\s+\$([^$]+)\$\s+cups'
    match = re.search(pattern, question_text)

    if match:
        amt1_str = match.group(1).strip()
        amt2_str = match.group(2).strip()

        # Parse first amount
        if '/' in amt1_str:
            parts = amt1_str.split('/')
            amt1 = Fraction(int(parts[0]), int(parts[1]))
        else:
            amt1 = Fraction(int(amt1_str), 1)

        # Parse second amount
        if '/' in amt2_str:
            parts = amt2_str.split('/')
            amt2 = Fraction(int(parts[0]), int(parts[1]))
        else:
            amt2 = Fraction(int(amt2_str), 1)

        return amt1, amt2, amt1_str, amt2_str

    return None, None, None, None

def format_mixed_number(frac):
    """Format a fraction as a mixed number if appropriate"""
    if frac.numerator >= frac.denominator and frac.denominator != 1:
        whole = frac.numerator // frac.denominator
        remainder = frac.numerator % frac.denominator
        if remainder == 0:
            return str(whole)
        return f"{whole} {remainder}/{frac.denominator}"
    elif frac.denominator == 1:
        return str(frac.numerator)
    else:
        return f"{frac.numerator}/{frac.denominator}"

def create_addition_solution(amt1, amt2, amt1_str, amt2_str, context):
    """Create proper solution text for addition problems"""
    # Calculate the sum
    total = amt1 + amt2

    # Format amounts for display
    if '/' in amt1_str:
        parts = amt1_str.split('/')
        amt1_display = f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
    else:
        amt1_display = amt1_str

    if '/' in amt2_str:
        parts = amt2_str.split('/')
        amt2_display = f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
    else:
        amt2_display = amt2_str

    solution = []

    # Step 1: Understand the problem
    solution.append([
        "1/4",
        f"We need to find the total amount of flour for both recipes."
    ])

    # Step 2: Set up the addition
    if amt2.denominator == 1:  # Second amount is a whole number
        solution.append([
            "2/4",
            f"We have ${amt1_display}$ cups from the first recipe and ${amt2_display}$ cups from the second recipe.\\n" +
            f"To add these, we first convert ${amt2_display}$ to a fraction with denominator {amt1.denominator}:\\n" +
            f"${amt2_display} = \\frac{{{amt2.numerator * amt1.denominator}}}{{{amt1.denominator}}}$"
        ])
    elif amt1.denominator == amt2.denominator:  # Same denominators
        solution.append([
            "2/4",
            f"We have ${amt1_display}$ cups from the first recipe and ${amt2_display}$ cups from the second recipe.\\n" +
            f"Since they have the same denominator, we can add the numerators directly."
        ])
    else:  # Different denominators
        lcm = (amt1.denominator * amt2.denominator) // Fraction(amt1.denominator, amt2.denominator).denominator
        solution.append([
            "2/4",
            f"We have ${amt1_display}$ cups from the first recipe and ${amt2_display}$ cups from the second recipe.\\n" +
            f"To add these, we need a common denominator of {lcm}:\\n" +
            f"${amt1_display} = \\frac{{{amt1.numerator * (lcm // amt1.denominator)}}}{{{lcm}}}$ and " +
            f"${amt2_display} = \\frac{{{amt2.numerator * (lcm // amt2.denominator)}}}{{{lcm}}}$"
        ])

    # Step 3: Perform the addition
    if amt2.denominator == 1:
        solution.append([
            "3/4",
            f"Now we can add:\\n" +
            f"$\\frac{{{amt1.numerator}}}{{{amt1.denominator}}} + \\frac{{{amt2.numerator * amt1.denominator}}}{{{amt1.denominator}}} = " +
            f"\\frac{{{amt1.numerator + amt2.numerator * amt1.denominator}}}{{{amt1.denominator}}}$"
        ])
    elif amt1.denominator == amt2.denominator:
        solution.append([
            "3/4",
            f"Adding the fractions:\\n" +
            f"$\\frac{{{amt1.numerator}}}{{{amt1.denominator}}} + \\frac{{{amt2.numerator}}}{{{amt2.denominator}}} = " +
            f"\\frac{{{amt1.numerator + amt2.numerator}}}{{{amt1.denominator}}}$"
        ])
    else:
        lcm = (amt1.denominator * amt2.denominator) // Fraction(amt1.denominator, amt2.denominator).denominator
        new_num1 = amt1.numerator * (lcm // amt1.denominator)
        new_num2 = amt2.numerator * (lcm // amt2.denominator)
        solution.append([
            "3/4",
            f"Adding the fractions:\\n" +
            f"$\\frac{{{new_num1}}}{{{lcm}}} + \\frac{{{new_num2}}}{{{lcm}}} = " +
            f"\\frac{{{new_num1 + new_num2}}}{{{lcm}}}$"
        ])

    # Step 4: Final answer
    if total.denominator == 1:
        final_answer = str(total.numerator)
    else:
        final_answer = f"\\frac{{{total.numerator}}}{{{total.denominator}}}"

    mixed = format_mixed_number(total)
    if ' ' in mixed:  # It's a mixed number
        parts = mixed.split()
        whole = parts[0]
        frac_parts = parts[1].split('/')
        mixed_display = f"{whole}\\frac{{{frac_parts[0]}}}{{{frac_parts[1]}}}"
        solution.append([
            "4/4",
            f"The total amount of flour needed for {context} is ${final_answer}$ cups.\\n" +
            f"As a mixed number: ${mixed_display}$ cups."
        ])
    else:
        solution.append([
            "4/4",
            f"The total amount of flour needed for {context} is ${final_answer}$ cups."
        ])

    return solution

# Read the file
with open('Gr7_20_E3_variations.json', 'r') as f:
    data = json.load(f)

# Extract context words from questions
contexts = [
    "YouTube subscribers", "Twitch viewers", "TikTok likes", "burgers", "Naruto episodes",
    "Instagram posts", "Snapchat stories", "Discord messages", "Reddit karma", "Twitter followers",
    "Minecraft builds", "Fortnite wins", "Among Us games", "Roblox creations", "Pokemon cards",
    "Netflix episodes", "Spotify playlists", "Amazon packages", "Tesla rides", "iPhone apps",
    "PlayStation games", "Xbox achievements", "Nintendo stars", "Steam downloads", "Epic victories",
    "Google searches", "Facebook friends", "WhatsApp chats", "Zoom meetings", "Teams calls",
    "Slack messages", "GitHub commits", "Stack Overflow points", "LinkedIn connections", "Pinterest pins",
    "Uber rides", "DoorDash orders", "Airbnb stays", "Venmo payments", "PayPal transfers",
    "Bitcoin trades", "Ethereum stakes", "NFT mints", "Crypto gains", "Stock trades",
    "Marvel movies", "Star Wars episodes", "Harry Potter spells", "Lord of the Rings chapters", "Game of Thrones seasons",
    "Breaking Bad episodes"
]

# Process each quiz
for i, quiz in enumerate(data['quizzes']):
    question_text = quiz['question_text']

    # Parse amounts from question
    amt1, amt2, amt1_str, amt2_str = parse_amounts_from_question(question_text)

    if amt1 and amt2:
        # Calculate correct answer (addition)
        total = amt1 + amt2

        # Set correct answer
        if total.denominator == 1:
            quiz['correct_answers'] = [str(total.numerator)]
        else:
            quiz['correct_answers'] = [f"{total.numerator}/{total.denominator}"]

        # Get context for this question
        context = contexts[i % len(contexts)]

        # Update solution text
        quiz['solution'] = create_addition_solution(amt1, amt2, amt1_str, amt2_str, context)

        # Remove incorrect image tags
        if 'solution_image_tag' in quiz:
            del quiz['solution_image_tag']

# Write the updated data back
with open('Gr7_20_E3_variations.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Fixed Gr7_20_E3_variations.json - {len(data['quizzes'])} entries updated")
print("- Fixed calculations (addition instead of multiplication)")
print("- Corrected answers to match addition problems")
print("- Updated solution text to properly explain addition steps")
print("- Removed incorrect image references")
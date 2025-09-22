import json
import random

def generate_decimal_fraction_conversions():
    """Generate conversion questions between decimals and fractions/mixed numbers for Gr7_6_E1"""

    with open('Gr7_6_E1_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Common fractions and their decimal equivalents
    conversions = [
        ("1/2", "0.5"), ("1/4", "0.25"), ("3/4", "0.75"), ("1/5", "0.2"), ("2/5", "0.4"),
        ("3/5", "0.6"), ("4/5", "0.8"), ("1/8", "0.125"), ("3/8", "0.375"), ("5/8", "0.625"),
        ("7/8", "0.875"), ("1/10", "0.1"), ("3/10", "0.3"), ("7/10", "0.7"), ("9/10", "0.9"),
        ("1/20", "0.05"), ("3/20", "0.15"), ("7/20", "0.35"), ("11/20", "0.55"), ("13/20", "0.65"),
        ("17/20", "0.85"), ("19/20", "0.95"), ("1/25", "0.04"), ("2/25", "0.08"), ("3/25", "0.12"),
        ("4/25", "0.16"), ("6/25", "0.24"), ("7/25", "0.28"), ("8/25", "0.32"), ("9/25", "0.36")
    ]

    # Mixed numbers
    mixed_conversions = [
        ("1 1/2", "1.5"), ("2 1/4", "2.25"), ("3 3/4", "3.75"), ("1 2/5", "1.4"), ("2 3/5", "2.6"),
        ("1 1/8", "1.125"), ("2 3/8", "2.375"), ("3 5/8", "3.625"), ("1 1/10", "1.1"), ("2 7/10", "2.7"),
        ("1 3/20", "1.15"), ("2 11/20", "2.55"), ("3 17/20", "3.85"), ("1 1/25", "1.04"), ("2 6/25", "2.24")
    ]

    all_conversions = conversions + mixed_conversions
    random.shuffle(all_conversions)

    # Generate 51 questions alternating between fraction-to-decimal and decimal-to-fraction
    for i in range(51):
        if i < len(all_conversions):
            frac, dec = all_conversions[i]
        else:
            # Generate additional conversions if needed
            idx = i % len(all_conversions)
            frac, dec = all_conversions[idx]

        if i % 2 == 0:
            # Fraction to decimal
            if ' ' in frac:
                # Mixed number
                parts = frac.split(' ')
                whole = parts[0]
                frac_parts = parts[1].split('/')
                num = frac_parts[0]
                denom = frac_parts[1]
                question_text = f"Convert ${whole}\\frac{{{num}}}{{{denom}}}$ to a decimal."
            else:
                # Regular fraction
                parts = frac.split('/')
                num = parts[0]
                denom = parts[1]
                question_text = f"Convert $\\frac{{{num}}}{{{denom}}}$ to a decimal."

            question = {
                "skills": "convert-between-decimals-and-fractions-or-mixed-numbers",
                "question_text": question_text,
                "question_type": "Fill in the blank",
                "correct_answers": [dec],
                "solution": [
                    [
                        "1/2",
                        f"To convert {'the fraction' if ' ' not in frac else 'the mixed number'} to a decimal, " +
                        ("divide the numerator by the denominator." if ' ' not in frac else "first convert to an improper fraction or calculate directly.")
                    ],
                    [
                        "2/2",
                        f"{'Dividing: ' + frac.replace('/', ' ÷ ') + ' = ' + dec if ' ' not in frac else 'The mixed number equals ' + dec}"
                    ]
                ],
                "tag": "Gr7_6_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }
        else:
            # Decimal to fraction
            question = {
                "skills": "convert-between-decimals-and-fractions-or-mixed-numbers",
                "question_text": f"Convert {dec} to a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [frac],
                "solution": [
                    [
                        "1/2",
                        f"To convert {dec} to a fraction, first write it as a fraction with an appropriate denominator."
                    ],
                    [
                        "2/2",
                        f"Simplifying to lowest terms: {frac}"
                    ]
                ],
                "tag": "Gr7_6_E1",
                "question_number": f"1_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_6_E1_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 decimal-fraction conversion questions for Gr7_6_E1")

def generate_percent_conversions():
    """Generate conversion questions between percents, fractions, and decimals for Gr7_6_E2"""

    with open('Gr7_6_E2_variations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    questions = []

    # Common percent conversions
    percent_conversions = [
        ("25%", "1/4", "0.25"), ("50%", "1/2", "0.5"), ("75%", "3/4", "0.75"),
        ("20%", "1/5", "0.2"), ("40%", "2/5", "0.4"), ("60%", "3/5", "0.6"), ("80%", "4/5", "0.8"),
        ("10%", "1/10", "0.1"), ("30%", "3/10", "0.3"), ("70%", "7/10", "0.7"), ("90%", "9/10", "0.9"),
        ("5%", "1/20", "0.05"), ("15%", "3/20", "0.15"), ("35%", "7/20", "0.35"), ("45%", "9/20", "0.45"),
        ("55%", "11/20", "0.55"), ("65%", "13/20", "0.65"), ("85%", "17/20", "0.85"), ("95%", "19/20", "0.95"),
        ("12.5%", "1/8", "0.125"), ("37.5%", "3/8", "0.375"), ("62.5%", "5/8", "0.625"), ("87.5%", "7/8", "0.875")
    ]

    # Additional conversions to reach 51
    additional_percent = [
        ("2%", "1/50", "0.02"), ("4%", "1/25", "0.04"), ("8%", "2/25", "0.08"), ("12%", "3/25", "0.12"),
        ("16%", "4/25", "0.16"), ("24%", "6/25", "0.24"), ("28%", "7/25", "0.28"), ("32%", "8/25", "0.32"),
        ("36%", "9/25", "0.36"), ("44%", "11/25", "0.44"), ("48%", "12/25", "0.48"), ("52%", "13/25", "0.52"),
        ("56%", "14/25", "0.56"), ("64%", "16/25", "0.64"), ("68%", "17/25", "0.68"), ("72%", "18/25", "0.72"),
        ("76%", "19/25", "0.76"), ("84%", "21/25", "0.84"), ("88%", "22/25", "0.88"), ("92%", "23/25", "0.92"),
        ("96%", "24/25", "0.96"), ("1%", "1/100", "0.01"), ("3%", "3/100", "0.03"), ("6%", "3/50", "0.06"),
        ("7%", "7/100", "0.07"), ("9%", "9/100", "0.09"), ("11%", "11/100", "0.11"), ("13%", "13/100", "0.13"),
        ("14%", "7/50", "0.14")
    ]

    all_conversions = percent_conversions + additional_percent

    for i in range(51):
        conversion_type = i % 3  # Cycle through 3 types of conversions
        percent, fraction, decimal = all_conversions[i % len(all_conversions)]

        if conversion_type == 0:
            # Percent to fraction
            question = {
                "skills": "convert-between-percents-fractions-and-decimals",
                "question_text": f"Convert {percent} to a fraction in lowest terms.",
                "question_type": "Fill in the blank",
                "correct_answers": [fraction],
                "solution": [
                    [
                        "1/3",
                        f"To convert {percent} to a fraction, write it as a fraction over 100."
                    ],
                    [
                        "2/3",
                        f"{percent} = {percent.replace('%', '')}/100"
                    ],
                    [
                        "3/3",
                        f"Simplifying to lowest terms: {fraction}"
                    ]
                ],
                "tag": "Gr7_6_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }
        elif conversion_type == 1:
            # Fraction to percent
            parts = fraction.split('/')
            num = parts[0]
            denom = parts[1]
            question = {
                "skills": "convert-between-percents-fractions-and-decimals",
                "question_text": f"Convert $\\frac{{{num}}}{{{denom}}}$ to a percent.",
                "question_type": "Fill in the blank",
                "correct_answers": [percent],
                "solution": [
                    [
                        "1/2",
                        f"To convert the fraction to a percent, first convert to a decimal, then multiply by 100."
                    ],
                    [
                        "2/2",
                        f"$\\frac{{{num}}}{{{denom}}}$ = {decimal} = {percent}"
                    ]
                ],
                "tag": "Gr7_6_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }
        else:
            # Decimal to percent
            question = {
                "skills": "convert-between-percents-fractions-and-decimals",
                "question_text": f"Convert {decimal} to a percent.",
                "question_type": "Fill in the blank",
                "correct_answers": [percent],
                "solution": [
                    [
                        "1/2",
                        f"To convert a decimal to a percent, multiply by 100 and add the % symbol."
                    ],
                    [
                        "2/2",
                        f"{decimal} × 100 = {percent}"
                    ]
                ],
                "tag": "Gr7_6_E2",
                "question_number": f"2_{i+1}",
                "solution_image_tag": []
            }

        questions.append(question)

    data['quizzes'] = questions

    with open('Gr7_6_E2_variations.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Generated 51 percent conversion questions for Gr7_6_E2")

# Run both fixes
generate_decimal_fraction_conversions()
generate_percent_conversions()
print("Fixed both Gr7_6_E1 and Gr7_6_E2 with proper conversion questions")
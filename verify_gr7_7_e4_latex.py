import json
import re

def verify_gr7_7_e4_latex():
    """Comprehensively verify and report on LaTeX formatting in Gr7_7_E4"""
    print("\n" + "=" * 60)
    print("Verifying Gr7_7_E4 LaTeX formatting...")
    print("=" * 60)

    filename = 'Gr7_7_E4_variations.json'
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    issues_found = []

    for idx, question in enumerate(data['quizzes'], 1):
        q_text = question['question_text']
        q_num = question.get('question_number', f'unknown_{idx}')

        # Check for various potential LaTeX issues
        problems = []

        # Issue 1: Double dollar signs $$
        if '$$' in q_text:
            problems.append("Contains double dollar signs ($$)")

        # Issue 2: Dollar sign followed by another dollar sign with space $ $
        if re.search(r'\$\s+\$', q_text):
            problems.append("Contains separated dollar signs ($ $)")

        # Issue 3: Mixed number without \frac (like $2 5/6$ instead of $2\frac{5}{6}$)
        match_mixed = re.search(r'\$\d+\s+\d+/\d+', q_text)
        if match_mixed:
            problems.append(f"Mixed number without \\frac: {match_mixed.group()}")

        # Issue 4: Fraction without \frac in dollar signs (like $3/4$ instead of $\frac{3}{4}$)
        match_frac = re.search(r'\$[^\\]*\d+/\d+', q_text)
        if match_frac:
            problems.append(f"Fraction without \\frac in LaTeX: {match_frac.group()}")

        # Issue 5: Too many backslashes (\\\\frac instead of \\frac)
        if '\\\\\\\\frac' in q_text:
            problems.append("Contains 4 backslashes before frac")

        # Issue 6: Dollar signs inside parentheses issues like $($\frac or \frac$)
        if re.search(r'\$\(\$\\\\frac', q_text):
            problems.append("Dollar sign after opening parenthesis: $($ pattern")
        if re.search(r'\}\}\$\)', q_text):
            problems.append("Dollar sign before closing parenthesis: $) pattern")

        # Issue 7: Stray dollar signs before operators
        if re.search(r'\\}\\}\$\\s+\\\\(div|times)', q_text):
            problems.append("Dollar sign before operator (\\div or \\times)")

        if problems:
            issues_found.append({
                'question_number': q_num,
                'question_index': idx,
                'problems': problems,
                'question_text': q_text
            })

    # Report findings
    print(f"\nTotal questions examined: {len(data['quizzes'])}")
    print(f"Questions with issues: {len(issues_found)}\n")

    if issues_found:
        print("ISSUES FOUND:")
        print("-" * 60)
        for issue in issues_found:
            print(f"\nQuestion {issue['question_index']} ({issue['question_number']}):")
            for problem in issue['problems']:
                print(f"  - {problem}")
            print(f"  Text preview: {issue['question_text'][:150]}...")
    else:
        print("No LaTeX formatting issues detected!")
        print("\nAll questions have proper LaTeX formatting:")
        print("  - Correct backslash escaping (\\\\frac in JSON)")
        print("  - Proper dollar sign delimiters")
        print("  - No stray or extra dollar signs")
        print("  - Mixed numbers use \\frac notation")

    return len(issues_found)

# Run verification
issues_count = verify_gr7_7_e4_latex()

print("\n" + "=" * 60)
if issues_count == 0:
    print("Verification complete: LaTeX formatting is correct!")
else:
    print(f"Verification complete: {issues_count} questions need fixes")
print("=" * 60)

import json
import re

# Load the JSON data
with open("C:/Users/kapil/numi-scraper/Gr6_55_E1_variations.json", "r") as f:
    data = json.load(f)

# Generate HTML
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade 6 Budget Tables - Complete</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .table-container {
            margin: 30px auto;
            max-width: 600px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            page-break-inside: avoid;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
            font-size: 18px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 0 auto;
        }
        th {
            background-color: #4a90e2;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #3a7bc8;
        }
        td {
            padding: 10px 12px;
            border: 1px solid #ddd;
            background-color: #fff;
        }
        tr:nth-child(even) td {
            background-color: #f9f9f9;
        }
        .amount {
            text-align: right;
            font-weight: bold;
            color: #2c5282;
        }
        .table-id {
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
"""

# Process each quiz
for quiz in data["quizzes"]:
    question_num = quiz["question_number"]
    backend_desc = quiz.get("backend_description", "")
    
    # Extract title
    if "titled" in backend_desc:
        parts = backend_desc.split("titled")[1].split(".")[0]
        title = parts.strip().strip('"').strip("'")
    else:
        title = f"Budget Table {question_num}"
    
    # Parse income and expenses from backend description
    income_items = []
    expenses_items = []
    
    # The backend_description has format like:
    # "Under the Income column, there are three sources listed: 'Item1: $amount1', 'Item2: $amount2'..."
    # "In the Expenses column, there are three listed items: 'Item1: $amount1', 'Item2: $amount2'..."
    
    if "Income" in backend_desc and "Expenses" in backend_desc:
        # Extract income section - look for pattern after "Income column"
        income_pattern = r"Income column[^:]*:\s*([^.]+)\."
        income_match = re.search(income_pattern, backend_desc)
        if income_match:
            income_text = income_match.group(1)
            # Find all 'Item: $amount' patterns
            item_matches = re.findall(r"'([^:]+):\s*\$(\d+)'", income_text)
            for item, amount in item_matches:
                item = item.strip()
                income_items.append((item, amount))
        
        # Extract expenses section - look for pattern after "Expenses column"
        expenses_pattern = r"Expenses column[^:]*:\s*([^.]+)\."
        expenses_match = re.search(expenses_pattern, backend_desc)
        if expenses_match:
            expenses_text = expenses_match.group(1)
            # Find all 'Item: $amount' patterns
            item_matches = re.findall(r"'([^:]+):\s*\$(\d+)'", expenses_text)
            for item, amount in item_matches:
                item = item.strip()
                expenses_items.append((item, amount))
    
    # Create HTML table for this question
    html_content += f"""
<!-- Table {question_num}: {title} -->
<div class="table-container" id="table_{question_num}">
    <h2>{title}</h2>
    <table>
        <thead>
            <tr>
                <th>Income</th>
                <th class="amount">Amount</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for item, amount in income_items:
        html_content += f"""            <tr>
                <td>{item}</td>
                <td class="amount">${amount}</td>
            </tr>
"""
    
    html_content += """        </tbody>
    </table>
    <br>
    <table>
        <thead>
            <tr>
                <th>Expenses</th>
                <th class="amount">Amount</th>
            </tr>
        </thead>
        <tbody>
"""
    
    for item, amount in expenses_items:
        html_content += f"""            <tr>
                <td>{item}</td>
                <td class="amount">${amount}</td>
            </tr>
"""
    
    html_content += f"""        </tbody>
    </table>
    <div class="table-id">Table {question_num}</div>
</div>
"""

html_content += """
</body>
</html>"""

# Save the HTML file
with open("C:/Users/kapil/numi-scraper/Gr6_55_E1_tables.html", "w") as f:
    f.write(html_content)

print("HTML file created with all budget tables!")
print(f"Total tables created: {len(data['quizzes'])}")

# Also create a summary
print("\nFirst 5 tables preview:")
for i, quiz in enumerate(data["quizzes"][:5]):
    backend = quiz.get("backend_description", "")
    print(f"\nQuestion {quiz['question_number']}:")
    print(f"  Description preview: {backend[:100]}...")
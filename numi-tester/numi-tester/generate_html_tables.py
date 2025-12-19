import os

html_dir = r"c:\Users\kapil\Documents\numi-tester\html"
os.makedirs(html_dir, exist_ok=True)

def create_html_table(filename, rows, headers, highlight_idx=None):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;
            font-family: Arial, sans-serif;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .highlight {{
            background-color: #ffffcc;
        }}
    </style>
</head>
<body>
    <table>
        <tr>
"""
    for header in headers:
        html += f"            <th>{header}</th>\n"
    html += "        </tr>\n"

    for idx, row in enumerate(rows):
        css_class = ' class="highlight"' if idx == highlight_idx else ''
        html += f"        <tr{css_class}>\n"
        for cell in row:
            html += f"            <td>{cell}</td>\n"
        html += "        </tr>\n"

    html += """    </table>
</body>
</html>"""

    filepath = os.path.join(html_dir, filename + ".html")
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {filename}.html")

# Template 3 & 4: Perimeter → MAX/MIN area tables
perimeters_t3 = [20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 16, 18]
for i, perim in enumerate(perimeters_t3, 26):
    half_p = perim // 2
    rows = []
    max_area = 0
    max_idx = 0
    for long in range(half_p, 0, -1):
        short = half_p - long
        if short > 0 and short <= long:
            area = long * short
            rows.append([str(long), str(short), f"{area}cm²"])
            if area > max_area:
                max_area = area
                max_idx = len(rows) - 1

    create_html_table(f"Gr56_1_{i}_step_3", rows,
                     ["Long side", "Short side", "Area<br>(long side x short side)"],
                     max_idx)

perimeters_t4 = [20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48, 16]
for i, perim in enumerate(perimeters_t4, 39):
    half_p = perim // 2
    rows = []
    min_area = float('inf')
    min_idx = 0
    for long in range(half_p, 0, -1):
        short = half_p - long
        if short > 0 and short <= long:
            area = long * short
            rows.append([str(long), str(short), f"{area}cm²"])
            if area < min_area:
                min_area = area
                min_idx = len(rows) - 1

    create_html_table(f"Gr56_1_{i}_step_3", rows,
                     ["Long side", "Short side", "Area<br>(long side x short side)"],
                     min_idx)

# Template 5: Area + context → perimeter (closest factors)
areas_t5 = [24, 30, 36, 40, 48, 60, 72, 20, 18, 28, 32, 42, 54]
for i, area in enumerate(areas_t5, 1):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    rows = []
    min_diff = float('inf')
    min_idx = 0
    for idx, (short, long) in enumerate(factors):
        diff = long - short
        rows.append([str(long), str(short), f"{area}cm²", f"{long} - {short} = {diff}"])
        if diff < min_diff:
            min_diff = diff
            min_idx = idx

    create_html_table(f"Gr56_2_{i}_step_2", rows,
                     ["Long side", "Short side", "Area<br>(long side × short side)", "Difference"],
                     min_idx)

# Template 6: Area → count rectangles
areas_t6 = [25, 49, 16, 36, 64, 81, 100, 12, 18, 20, 28, 32]
for i, area in enumerate(areas_t6, 14):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    rows = []
    for short, long in factors:
        rows.append([str(long), str(short), f"{area}cm²"])

    create_html_table(f"Gr56_2_{i}_step_2", rows,
                     ["Long side", "Short side", "Area<br>(long side × short side)"])

# Template 7: Area → MAX perimeter
areas_t7 = [24, 30, 36, 40, 48, 60, 72, 20, 18, 28, 32, 42, 54]
for i, area in enumerate(areas_t7, 26):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    rows = []
    max_perim = 0
    max_idx = 0
    for idx, (short, long) in enumerate(factors):
        perim = 2 * (long + short)
        rows.append([str(long), str(short), f"{area}cm²", f"2({long}) + 2({short}) = {2*long} + {2*short} = {perim} cm"])
        if perim > max_perim:
            max_perim = perim
            max_idx = idx

    create_html_table(f"Gr56_2_{i}_step_2", rows,
                     ["Long side", "Short side", "Area", "Perimeter"],
                     max_idx)

# Template 8: Area → MIN perimeter
areas_t8 = [24, 30, 36, 40, 48, 60, 72, 20, 18, 28, 32, 42]
for i, area in enumerate(areas_t8, 39):
    factors = [(a, area//a) for a in range(1, int(area**0.5) + 1) if area % a == 0]
    rows = []
    min_perim = float('inf')
    min_idx = 0
    for idx, (short, long) in enumerate(factors):
        perim = 2 * (long + short)
        rows.append([str(long), str(short), f"{area}cm²", f"2({long}) + 2({short}) = {2*long} + {2*short} = {perim} cm"])
        if perim < min_perim:
            min_perim = perim
            min_idx = idx

    create_html_table(f"Gr56_2_{i}_step_2", rows,
                     ["Long side", "Short side", "Area", "Perimeter"],
                     min_idx)

print(f"\nAll HTML tables created successfully!")



import re
def decode_text(text, section):
    text = clear_table_text(text, section)
    text = clear_chart_text(text, section)
    text = clear_diagram_wrapper_text(text, section)

    text = format_fraction(text)
    return text.replace("\xa0", "").replace("\t", "")

def clear_table_text(text, section):

    # Table text still doesn't get removed :((( 
    table_elements = section.query_selector_all("table")
    if len(table_elements) > 0:
        print("Found table elements")

        filteredText = text
        # Get the inner text of each table
        table_texts = [table.inner_text() for table in table_elements]
        for table_text in table_texts:

            print(f"table_text: {table_text}")
            print(f"table_text is in question_text: {table_text in filteredText}")
            filteredText = filteredText.replace(table_text, "")
        print(f"filteredText: {filteredText}")
        return filteredText
    else:
        print("Can't find table elements")
        return text

def clear_chart_text(text, section):
    # Table text still doesn't get removed :((( 
    chart_elements = section.query_selector_all("div.qPVTable")
    if len(chart_elements) > 0:
        print("Found chart elements")
        filteredText = text
        # Get the inner text of each table
        chart_texts = [chart.inner_text() for chart in chart_elements]
        for chart_text in chart_texts:
            print(f"chart_text: {chart_text}")
            print(f"chart_text is in solution: {chart_text in filteredText}")
            filteredText = filteredText.replace(chart_text, "")
        print(f"filteredText: {filteredText}")
        return filteredText
    else:
        print("Can't find chart elements")
        return text

def clear_diagram_wrapper_text(text, section):
    # Table text still doesn't get removed :((( 
    diagram_elements = section.query_selector_all("div.diagramWrapper")
    if len(diagram_elements) > 0:
        print("Found diagram elements")
        filteredText = text
        # Get the inner text of each table
        diagram_texts = [diagram.inner_text() for diagram in diagram_elements]
        for diagram_text in diagram_texts:
            filteredText = filteredText.replace(diagram_text, "")
        return filteredText
    else:
        print("Can't find diagram elements")

        return text


def format_fraction(text):


    return re.sub(r'\n(\d+)\n(\d+)\n', replacer, text)

def replacer(match):
    numerator = match.group(1)
    denominator = match.group(2)
    return f"$\\frac{{{numerator}}}{{{denominator}}}$"


import re
def decode_text(text, page):
    section = page.query_selector("section.ixl-practice-crate")
    text = clear_table_text(text, section)
    text = format_fraction(text)
    return text.replace("\xa0", "").replace("\t", "")

def clear_table_text(text, section):
    # Table text still not get removed :((( 
    table_elements = section.query_selector_all("table")
    if len(table_elements) > 0:
        filteredText = text
        # Get the inner text of each table
        table_texts = [table.inner_text() for table in table_elements]
        for table_text in table_texts:
            filteredText = filteredText.replace(table_text, "")
        return filteredText
    else:
        return text


def format_fraction(text):
    return re.sub(r'\n(\d+)\n(\d+)\n', replacer, text)

def replacer(match):
    numerator = match.group(1)
    denominator = match.group(2)
    return f"$\\frac{{{numerator}}}{{{denominator}}}$"
def check_fill_in_the_blank(page):
    hasFITB = len(page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn"))
    hasMCQ = len(page.query_selector_all("div.question-component section.ixl-practice-crate div.LaidOutTiles"))
    return hasFITB and (not hasMCQ)
    
def check_multiple_choices(page):
    hasFITB = len(page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn"))
    hasMCQ = len(page.query_selector_all("div.question-component section.ixl-practice-crate div.LaidOutTiles"))
    return hasMCQ and (not hasFITB)

def check_fill_in_the_blank_and_multiple_choices(page):
    hasFITB = len(page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn"))
    hasMCQ = len(page.query_selector_all("div.question-component section.ixl-practice-crate div.LaidOutTiles"))
    return hasMCQ and hasFITB
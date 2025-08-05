def check_fill_in_the_blank(page):
    hasFITB = len(page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn"))
    hasMCQ = len(page.query_selector_all("div.question-component section.ixl-practice-crate div.LaidOutTiles"))
    return hasFITB and (not hasMCQ)
    
def check_multiple_choices(page):
    hasFITB = len(page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn"))
    hasMCQ = len(page.query_selector_all("div.question-component section.ixl-practice-crate div.LaidOutTiles"))
    return hasMCQ and (not hasFITB)

def check_ordering_items(page):
    return page.is_visible(
        "section.ixl-practice-crate div.order-items-container",
        timeout=10_000
    )

def check_drag_and_drop(page):
    return page.is_visible(
        "section.ixl-practice-crate div.dragAndDropContainer.dragAndDropSortingContainer",
        timeout=10_000
    )
def check_fill_in_the_blank(page):
    return page.is_visible(
        "section.ixl-practice-crate input.fillIn",
        timeout=10_000
    )

def check_multiple_choices(page):
    return page.is_visible(
        "section.ixl-practice-crate div.LaidOutTiles",
        timeout=10_000
    )

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
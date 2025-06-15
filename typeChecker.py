def check_fill_in_the_blank(page):
    try:
        res = page.wait_for_selector("section.ixl-practice-crate input.fillIn", timeout=10000)
        return True if res else False
    except TimeoutError:
        return False

def check_multiple_choices(page):
    try:
        res = page.wait_for_selector("section.ixl-practice-crate div.LaidOutTiles", timeout=10000)
        return True if res else False
    except TimeoutError:
        return False
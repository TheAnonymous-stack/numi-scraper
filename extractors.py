import base64
from playwright.sync_api import TimeoutError
from textFormat import decode_text
def extract_question_text(page, json):
    # Wait for question section
    section = page.query_selector("div.question-component section.ixl-practice-crate")

    # Extract text
    text = decode_text(section.inner_text()) # gets all rendered (visible) text
    
    json["question_text"] = text

def extract_answer_fill_in_the_blank(page, json, code):
    
    
    # Fill wrong answer into input inside .math.section
    print("Locating the input field...")
    fill_in = page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn")
    for blank in fill_in:
        blank.fill("m")
        print("Wrong answer 'm' entered.")

    try:
        # Click the Submit button
        print("Clicking the Submit button...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return False

    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
    except TimeoutError:
        print("Correct answer section did not appear.")
        return False

    try:
        print("Extracting correct answer...")
        section = page.query_selector("div.correct-answer.ixl-practice-crate")
        value = decode_text(section.inner_text())
        input_boxes = page.query_selector_all("div.correct-answer.ixl-practice-crate input.fillIn")
        if input_boxes:
            for box in input_boxes:
                value += decode_text(box.evaluate("e => e.value"))
        json['correct_answers'] = [value]
        extract_answer_explanation(page, json, code)
        # section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
        # explanation = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
        # json['solution'] = format_explanation(explanation)
        return True
    except Exception as e:
        print(f"Failed to extract correct answer: {e}")
        return False

def extract_answer_multiple_choices(page, json, code):
    try:
        print("Collecting all options...")
        crate = page.query_selector("section.ixl-practice-crate")
        image_options = crate.wait_for_selector(
            "div.math div.responsive-info-higher-order-component div.LaidOutTiles div.TileSkinClassic.FLOAT",
            timeout=5000)
        if image_options:
            image_options = crate.query_selector_all(
                "div.math div.responsive-info-higher-order-component div.LaidOutTiles div.TileSkinClassic.FLOAT")
        options = page.query_selector_all("section.ixl-practice-crate div.responsive-info-higher-order-component div.LaidOutTiles div.SelectableTile.MULTIPLE_CHOICE")
        if not options:
            options = page.query_selector_all("section.ixl-practice-crate div.responsive-info-higher-order-component div.LaidOutTiles div.SelectableTile.MULTIPLE_SELECT")
    except TimeoutError as e:
        print("Error occurred while collecting options", e)
        return
    
    try:
        print("Extracting all options...")
        image_exists = page.locator("section.ixl-practice-crate "
    "div.math "
    "div.responsive-info-higher-order-component "
    "div.LaidOutTiles "
    "div.TileSkinClassic.FLOAT")
        if image_options and image_exists.count() > 0:
            json["image_choice_tags"] = []
            for i, option in enumerate(image_options):
                option.screenshot(path=f"Grade4_Images/Grade4_{code.split('.')[0]}/Grade4_{code}_{chr(i+65)}.png")
                json["image_choice_tags"].append(f'Grade4_{code}_{chr(i+65)}')
        else:
            json["choices"] = []
            for i, option in enumerate(options):
                class_attr = option.get_attribute("class")
                if "nonInteractive" not in class_attr.split():
                    json["choices"].append(decode_text(option.inner_text()))
                
    except Exception as e:
        print("Error while extracting options:", e)
        return
    
    try:
        # Click the Submit button
        print("Clicking the Submit button...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return
    try:
        res = page.wait_for_selector("div.ixl-modal-inside div.ixl-modal-content h3.hd", timeout=8000)
        text = decode_text(res.inner_text())
        if "Incomplete" in text:
            print("Confirming submission of ordering items...")
            confirm_button = page.get_by_label("Incomplete Answer").get_by_role("button", name="Submit")
            confirm_button.click()
            print("Submission confirmed.")
    except TimeoutError:
        print("No pop up confirmation found, something went wrong")
        return
    
    try:
        print("Extracting correct answer...")
        res = page.wait_for_selector("div.answer-box h2.feedback-header.correct", timeout=8000)
        try:
                options = page.query_selector_all("div.answer-box div.LaidOutTiles div.SelectableTile.MULTIPLE_CHOICE")
                if not options:
                    options = page.query_selector_all(
                        "div.answer-box div.LaidOutTiles div.SelectableTile.MULTIPLE_SELECT")
                i = 0
                num_answer = 0
                json["correct_answers"] = []
                while i < len(options):
                    class_attr = options[i].get_attribute("class")
                    if "selected" in class_attr.split():
                        num_answer += 1
                        json["correct_answers"].append(chr(i+65))
                        print("Saved the index of the answer in options")
                    i += 1

                if num_answer > 1:
                    json["question_type"] = "Multiple Choice with Multiple Answers"
                extract_answer_explanation(page, json, code)
                # section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
                # explanation = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
                # json['solution'] = format_explanation(explanation)
                
            
        except Exception as e:
                print("Error while searching for answer:", e)
                return

    except Exception as e:
        print(f"Error while extracting correct answer: {e}")
        return

def fill_in_the_blank_and_multiple_choices_loop(page, json):
    extract_question_text(page, json)
    try:
        print("Collecting all options...")
        options = page.query_selector_all("section.ixl-practice-crate div.responsive-info-higher-order-component div.LaidOutTiles div.SelectableTile.MULTIPLE_CHOICE")

    except TimeoutError:
        print("Error occurred while collecting options")
        return
    
    try:
        print("Taking screenshots of all options...")
        json["choices"] = []
        for i, option in enumerate(options):
            class_attr = option.get_attribute("class")
            if "nonInteractive" not in class_attr.split():
                json["choices"].append(decode_text(option.inner_text()))
                # image_bytes = option.screenshot()
                # option.screenshot(path=f"option{i}.png")
                # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
                # json["choices"].append(image_b64)
    except Exception as e:
        print("Error while taking screenshots of options:", e)
        return
    
    try:
        print("Clicking first option")
        selected_option = options[0]
        selected_option.click()
    except Exception as e:
        print("Error occurred while clicking first option:", e)
        return
    
    
    input_boxes = page.query_selector_all("div.question-component section.ixl-practice-crate input.fillIn")
    for box in input_boxes:
        box.fill("m")
        print("Wrong answer 'm' entered")
    
    try:
        # Click the Submit button
        print("Clicking the Submit button...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return
    try:
        print("Checking if selected option is false...")
        res = page.wait_for_selector("div.answer-box h2.feedback-header.correct", timeout=8000)
        text = decode_text(res.inner_text())
        if "Sorry" in text:
            print("Selected option is confirmed to be false")
            try:
                options = page.query_selector_all("div.answer-box div.correct-answer.ixl-practice-crate")
                answerFound = False
                i = 1
                json["correct_answers"] = []
                while not answerFound:
                    class_attr = options[i].get_attribute("class")
                    if "selected" in class_attr.split():
                        json["correct_answers"].append(chr(65 + i))

                        print("Saved the index of the answer in options")
                        answerFound = True
                    i += 1
                section = page.query_selector("div.correct-answer.ixl-practice-crate")
                value = decode_text(section.inner_text())
                input_boxes = page.query_selector_all("div.correct-answer.ixl-practice-crate input.fillIn")
                if input_boxes:
                    for box in input_boxes:
                        value += box.evaluate("e => e.value")
                json['correct_answers'].append(value)

                section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
                explanation = decode_text(section.inner_text())
                json['solution'] = explanation

                return True # Selected wrong option and extracted answer with full explanation
            
            except Exception as e:
                print("Error while searching for answer:", e)
                return

    except TimeoutError:
        print("Selected the right option. Reloading for a different question...")
        return False
    
    

def extract_answer_fill_in_the_blank_and_multiple_choices(page, json):
    gotWrongOption = fill_in_the_blank_and_multiple_choices_loop(page, json)
    while not gotWrongOption:
        page.reload()
        gotWrongOption = fill_in_the_blank_and_multiple_choices_loop(page, json)
    
def extract_answer_sorting_drag_and_drop(page, json, code):
    try:
        print("Collecting all drag and drop items...")
        crate = page.query_selector("section.ixl-practice-crate")
        options = crate.query_selector_all(
            "div.ddItemBankDropSlot.dropArea")

    except TimeoutError:
        print("Error occurred while collecting drag and drop items")
        return

    try:
        print("Collecting all drag and drop categories...")
        categories = crate.query_selector_all(
            "div.binsContainer div.bin.dropArea")
    except TimeoutError:
        print("Error occurred while collecting drag and drop categories")
        return

    try:
        print("Storing all drag and drop items...")
        # code = page.query_selector("nav.breadcrumb-nav.site-nav-breadcrumb.unzoom.practice-breadcrumb.responsive div.breadcrumb-selected").inner_text().replace("\xa0", "").split(" ")[0]
        # folder_name = f"Grade4_Images/Grade4_{code.split('.')[0]}/Grade4_{code}"
        # json["items_image_folder"] = folder_name
        json["sorting_items"] = []
        for i, option in enumerate(options):
            json["sorting_items"].append(
                decode_text(option.inner_text()))
            # image_bytes = option.screenshot()
            # option.screenshot(path=f"drag_and_drop_item{i}.png")
            # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            # json["drag_and_drop_items"].append(image_b64)
    except Exception as e:
        print("Error while saving drag and drop items: ", e)
        return

    try:
        print("Taking all drag and drop categories...")
        json["categories"] = []
        for i, option in enumerate(categories):
            json["categories"].append(
                decode_text(option.inner_text()))
            # image_bytes = option.screenshot()
            # option.screenshot(path=f"drag_and_drop_categories{i}.png")
            # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            # json["categories"].append(image_b64)
    except Exception as e:
        print("Error while taking drag and drop items:", e)
        return

    try:
        print("Clicking submit button right away...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return

    # There exists a pop up so need to confirm submission
    try:
        res = page.wait_for_selector("div.ixl-modal-inside div.ixl-modal-content h3.hd", timeout=8000)
        text = decode_text(res.inner_text())
        if "Incomplete" in text:
            print("Confirming submission of ordering items...")
            confirm_button = page.get_by_label("Incomplete Answer").get_by_role("button", name="Submit")
            confirm_button.click()
            print("Submission confirmed.")
    except TimeoutError:
        print("No pop up confirmation found, something went wrong")
        return

    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
        print("Extracting correct sorting...")
        answers = page.query_selector_all("div.correct-answer.ixl-practice-crate div.dragAndDropContainer div.bin.dropArea")
        if answers:
            print("saving of the correct sorting...")
            sorted_values = {}
            for answer in answers:
                category = answer.query_selector("div.binHeader").inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
                correct_items = answer.query_selector_all("div.binContentRow")
                if category not in sorted_values:
                    sorted_values[category] = []
                for item in correct_items:
                    item = decode_text(item.inner_text())
                    if item != "":
                        sorted_values[category].append(item)
            json["correct_answers"] = [sorted_values]
            print("Correct order extracted and saved.")
            extract_answer_explanation(page, json, code)
            print("Extracted answer explanation.")
            return
    except TimeoutError:
        print("Correct answer section did not appear.")
        return

def extract_answer_pattern_drag_and_drop(page, json, code):
    crate = page.query_selector("section.ixl-practice-crate")
    # find shape options first
    stacks = crate.query_selector("div.gc-card-stacks")
    # take screenshot of each stack
    print("Taking screenshot of each stack...")
    json["shape_image_tags"] = []
    options = {}
    for i, stack in enumerate(stacks):
        card = stack.query_selector("div.gc-card-stack-top.interactive")
        pathName = f"Grade4_Images/Grade4_{code.split('.')[0]}/Grade4_{code}_{chr(i + 65)}.png"
        card.screenshot(path=pathName)
        json["shape_image_tags"].append(pathName)
        label = card.query_locator("svg").get_attribute("aria-label")
        options[label] = chr(i + 65)
    print("Finish taking screenshot of each stack")
    
    print("Getting setup sequence...")
    row = crate.query_selector("div.gc-card-row")
    json["sequence"] = []
    for card in row:
        value = card.get_attribute("aria-label")
        if "blank" in value:
            json["sequence"].append("empty")
        else:
            json["sequence"].append(options[value])
    print("Finish getting setup sequence")

    # click "Submit" button
    print("Clicking submit button...")
    submit_button = page.get_by_role("button", name="Submit")
    submit_button.click()
    print("Submit button clicked.")
    try:
        res = page.wait_for_selector("div.ixl-modal-inside div.ixl-modal-content h3.hd", timeout=8000)
        text = decode_text(res.inner_text())
        if "Incomplete" in text:
            print("Confirming submission of ordering items...")
            confirm_button = page.get_by_label("Incomplete Answer").get_by_role("button", name="Submit")
            confirm_button.click()
            print("Submission confirmed.")
    except TimeoutError:
        print("No pop up confirmation found, something went wrong")
        return
    
    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
    except Exception as e:
        print(f"Error occurred while waiting for the correct answer to appear: {e}")
    
    try:
        print("Extracting correct answer...")
        row = page.query_selector("div.correct-answer.ixl-practice-crate div.gc-card-row")
        json["correct_answers"] = [[]]
        res = json["correct_answers"][0]
        for card in row:
            value = card.get_attribute("aria-label")
            res.append(options[value])
        print("Finish extracting correct answer")

    except Exception as e:
        print(f"Error occurred while extracting the correct answer to appear: {e}")


    json["solution"] = []


def extract_answer_ordering_items(page, json, code):
    try:
        print("Collecting all items...")
        crate = page.query_selector("section.ixl-practice-crate")
        options = crate.query_selector_all(
            "div.order-items-item.order-items-numbers")

    except TimeoutError:
        print("Error occurred while collecting ordering items")
        return

    try:
        print("Saving all ordering items...")
        json["order_items"] = []
        for i, option in enumerate(options):
            # option = option.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
            json["order_items"].append(
                decode_text(option.inner_text()))
    except Exception as e:
        print("Error while saving ordering items:", e)
        return

    try:
        print("Clicking submit button right away...")
        submit_button = page.get_by_role("button", name="Submit")
        submit_button.click()
        print("Submit button clicked.")
    except Exception as e:
        print(f"Error clicking the Submit button: {e}")
        return

    # There exists a pop up so need to confirm submission
    try:
        res = page.wait_for_selector("div.ixl-modal-inside div.ixl-modal-content h3.hd", timeout=8000)
        text = decode_text(res.inner_text())
        if "Incomplete" in text:
            print("Confirming submission of ordering items...")
            confirm_button = page.get_by_label("Incomplete Answer").get_by_role("button", name="Submit")
            confirm_button.click()
            print("Submission confirmed.")
    except TimeoutError:
        print("No pop up confirmation found, something went wrong")
        return

    try:
        print("Waiting for the correct answer section to appear...")
        page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
        print("Correct answer section appeared.")
        # extract_answer_explanation(page, json)
        print("Extracting correct number order...")
        answers = page.query_selector_all("section.solve-box section.ixl-practice-crate div.order-items-container.interactive div.order-items-item.order-items-numbers")
        if answers:
            print("Taking saving the correct order...")
            json["correct_answers"] = []
            for answer in answers:
                json["correct_answers"].append(
                    decode_text(answer.inner_text()))
            print("Correct order extracted and saved.")
    except TimeoutError:
        print("Correct answer section did not appear.")
        return

    extract_answer_explanation(page, json, code)
    return
    # try:
    #     section = page.query_selector("div.explanation-box section.tab-box.web.optional-tab-box.solve-box")
    #     explanation = section.inner_text().replace("\xa0", "").replace("\t", "").encode('utf-8').decode('unicode_escape')
    #     json['solution'] = format_explanation(explanation)
    # except Exception as e:
    #     print(f"Error while extracting full solution: {e}")
    #     return

def format_explanation(explanation):
    list = explanation.split(".")
    total = len(list)
    res = []
    for i, sentence in enumerate(list):
        sentence_list = []
        sentence_list.append(f"{i + 1}/{total}")
        sentence_list.append(sentence+".")
        res.append(sentence_list)
    return res

def extract_answer_explanation(page, json, code):
    try:
        print("Extracting answer explanation...")
        res = page.wait_for_selector("section.solve-box section.ixl-practice-crate", timeout=5000)
        explanation = decode_text(res.inner_text())
        json["solution"] = format_explanation(explanation)
        print("Explanation text extracted.")
        canvas = res.query_selector_all("canvas")
        svg = res.query_selector_all("svg")
        table = res.query_selector_all("table")
        fraction_bar = res.query_selector_all("div.fractionBarContainer")
        math_list = res.query_selector_all("div.mathList")
        selectable_grid = res.query_selector_all("div.selectableGridContainerWrapper")
        if canvas:
            extract_answer_explanation_images(page, json, canvas, code)
        if svg:
            extract_answer_explanation_images(page, json, svg, code)
        if table:
            extract_answer_explanation_images(page, json, table, code)
        if fraction_bar:
            extract_answer_explanation_images(page, json, fraction_bar, code)
        if math_list:
            extract_answer_explanation_images(page, json, math_list, code)
        if selectable_grid:
            extract_answer_explanation_images(page, json, selectable_grid, code)
        return
    except Exception as e:
        print("An error occurred while extracting the explanation:", e)
        return

def extract_answer_explanation_images(page, json, visuals, code):
    try:
        print("Extracting answer explanation with graphics as image...")
        for i, option in enumerate(visuals):
            option.screenshot(path=f"Grade5_Images/Grade5_{code.split('.')[0]}/Grade5_{code}_solution_{i}.png")
            json["solution_image_tag"] = f"Grade5_{code}_solution_{i}"
            # image_bytes = option.screenshot()
            # option.screenshot(path=f"option{i}.png")
            # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
            # json["explanation_image_tag"].append(image_b64)
        # image_bytes = res.screenshot(path=f"answer_explanation_image_tag.png")
        # image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        # json["explanation_image_tag"] = image_b64
        print("explanation images extracted.")
    except Exception as e:
        print("An error occurred while extracting the graphics from the explanation:", e)
        return
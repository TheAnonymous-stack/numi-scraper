from playwright.sync_api import sync_playwright

def screenshot_question_section(url, output_path="question.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        counter = 1
        page = browser.new_page()
        for _ in range(50):
            output_path=f"question{str(counter)}.png"
            counter+=1
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)

                # Attempt to close the ad using the 'explore-btn' button
                try:
                    page.wait_for_selector("button.explore-btn", timeout=3000)
                    page.click("button.explore-btn")
                    print("Ad closed via 'explore-btn'")
                except:
                    print("No ad found or already dismissed.")

                # Screenshot the question section
                section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)
                section.screenshot(path=output_path)
            except:
                print(f"question{counter-1} failed")
        print(f"Screenshots saved to {output_path}")

        browser.close()

def extract_question_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        # Optional: dismiss ad
        try:
            page.wait_for_selector("button.explore-btn", timeout=3000)
            page.click("button.explore-btn")
        except:
            pass

        # Wait for question section
        section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)

        # Extract *visible* text
        text = section.inner_text()  # gets all rendered (visible) text

        # Alternatively, to get *all* text including hidden:
        # text = section.evaluate("e => e.textContent")

        print(text)
        browser.close()
        return text

def extract_correct_answer_fill_in_the_blank(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to True if you don't need to see the browser
        page = browser.new_page()

        try:
            print("Navigating to the page...")
            page.goto(url, timeout=15000)
        except TimeoutError:
            print("Timeout while loading the page.")
            browser.close()
            return
        
        # Attempt to close the ad using the 'explore-btn' button
        try:
            page.wait_for_selector("button.explore-btn", timeout=3000)
            page.click("button.explore-btn")
            print("Ad closed via 'explore-btn'")
        except:
            print("No ad found or already dismissed.")

        # Wait for question section
        section = page.wait_for_selector("section.ixl-practice-crate", timeout=5000)

        # Extract *visible* text
        text = section.inner_text()  # gets all rendered (visible) text
        print("Question is:", text)
        try:
            # Fill wrong answer into input inside .math.section
            print("Locating the input field...")
            fill_in = page.wait_for_selector("section.ixl-practice-crate input.fillIn", timeout=20000)
            fill_in.fill("m")
            print("Wrong answer 'm' entered.")
        except TimeoutError:
            print("Could not find the input field inside '.math.section'.")
            browser.close()
            return

        try:
            # Click the Submit button
            print("Clicking the Submit button...")
            submit_button = page.get_by_role("button", name="Submit")
            submit_button.click()
            print("Submit button clicked.")
        except Exception as e:
            print(f"Error clicking the Submit button: {e}")
            browser.close()
            return

        try:
            print("Waiting for the correct answer section to appear...")
            page.wait_for_selector("div.correct-answer.ixl-practice-crate", timeout=7000)
            print("Correct answer section appeared.")
        except TimeoutError:
            print("Correct answer section did not appear.")
            browser.close()
            return

        try:
            print("Extracting correct answer...")
            value = page.eval_on_selector("div.correct-answer.ixl-practice-crate input.fillIn", "el => el.value")
            print("Correct answer extracted:", value)
        except Exception as e:
            print(f"Failed to extract correct answer: {e}")

        browser.close()


question_url = "https://ca.ixl.com/math/grade-5/spell-word-names-for-numbers-up-to-1-000-000"
extract_correct_answer_fill_in_the_blank(question_url)
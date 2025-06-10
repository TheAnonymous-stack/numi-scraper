from playwright.sync_api import sync_playwright

def screenshot_question_section(url, output_path="question.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

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
        print(f"Screenshot saved to {output_path}")

        browser.close()
        

question_url = "https://ca.ixl.com/math/grade-5/use-compensation-to-add"
screenshot_question_section(question_url)




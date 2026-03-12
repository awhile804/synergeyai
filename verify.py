from playwright.sync_api import sync_playwright

def verify_labels():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock window.localStorage.setItem to select a mock project
        # and handle dialogs automatically (e.g. alert)
        page.add_init_script("window.localStorage.setItem('selectedProject', 'mock_project');")
        page.on('dialog', lambda dialog: dialog.accept())

        page.goto("file:///app/index.html")

        # 1. Test Filter Section Label
        page.wait_for_selector('label[for="searchInput"]')
        page.click('label[for="searchInput"]')

        # Evaluate if the searchInput is currently focused
        is_focused = page.evaluate("document.activeElement.id === 'searchInput'")
        if not is_focused:
            print("ERROR: Clicking 'Search' label did not focus 'searchInput'.")
            exit(1)

        print("SUCCESS: Clicking 'Search' label focused 'searchInput'.")

        # 2. Test Add Story Modal Labels
        # Open modal first
        page.click('#addStoryBtn')
        # Explicitly wait for modal content to be visible. The modal overlay id is addStoryModal
        page.wait_for_selector('#addStoryModal', state="visible")

        # Click on the label
        page.wait_for_selector('label[for="newStoryText"]', state="visible")
        page.click('label[for="newStoryText"]')

        is_focused = page.evaluate("document.activeElement.id === 'newStoryText'")
        if not is_focused:
            print("ERROR: Clicking 'User Story' label did not focus 'newStoryText'.")
            exit(1)

        print("SUCCESS: Clicking 'User Story' label focused 'newStoryText'.")

        browser.close()

if __name__ == "__main__":
    verify_labels()

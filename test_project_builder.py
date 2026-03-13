import sys
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("file:///app/project-builder.html")

        # Check existing row
        remove_btns = page.query_selector_all(".remove-row-btn")
        for btn in remove_btns:
            aria_label = btn.get_attribute("aria-label")
            if aria_label != "Remove row":
                print(f"Error: Existing button missing aria-label. Found: {aria_label}")
                sys.exit(1)

        # Add a new row
        page.click("button.add-row-btn:has-text('+ Add Output')")

        # Check all rows again
        remove_btns_after = page.query_selector_all(".remove-row-btn")
        if len(remove_btns_after) <= len(remove_btns):
            print("Error: Row was not added.")
            sys.exit(1)

        for btn in remove_btns_after:
            aria_label = btn.get_attribute("aria-label")
            if aria_label != "Remove row":
                print(f"Error: New or existing button missing aria-label. Found: {aria_label}")
                sys.exit(1)

        print("Test passed: All remove buttons have the correct aria-label.")
        browser.close()

if __name__ == "__main__":
    run_test()

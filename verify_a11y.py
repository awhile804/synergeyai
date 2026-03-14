from playwright.sync_api import sync_playwright

def test_a11y_labels():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Testing index.html...")
        page.goto("file:///app/index.html")

        # Test .modal-close
        modal_close_btns = page.query_selector_all('.modal-close')
        for btn in modal_close_btns:
            assert btn.get_attribute('aria-label') == 'Close modal', "Missing or incorrect aria-label on .modal-close"
        print(f"  Verified {len(modal_close_btns)} .modal-close buttons.")

        # Trigger rendering of action buttons by mocking Firebase and generating a table row,
        # or just search the raw HTML if we want to be simpler, but let's test project-builder first

        print("Testing project-builder.html...")
        page.goto("file:///app/project-builder.html")
        remove_row_btns = page.query_selector_all('.remove-row-btn')
        for btn in remove_row_btns:
            assert btn.get_attribute('aria-label') == 'Remove row', "Missing or incorrect aria-label on .remove-row-btn"
        print(f"  Verified {len(remove_row_btns)} initial .remove-row-btn buttons.")

        # Click an "add row" button to test the JS template strings
        page.click('button:has-text("+ Add Output")')
        remove_row_btns_after = page.query_selector_all('.remove-row-btn')
        assert len(remove_row_btns_after) > len(remove_row_btns), "Failed to add new row"
        assert remove_row_btns_after[-1].get_attribute('aria-label') == 'Remove row', "Missing or incorrect aria-label on dynamically added .remove-row-btn"
        print("  Verified dynamically added .remove-row-btn.")


        print("Testing sprint-planner.html...")
        page.goto("file:///app/sprint-planner.html")
        close_btn = page.query_selector('.close-btn')
        assert close_btn.get_attribute('aria-label') == 'Close detail view', "Missing or incorrect aria-label on .close-btn"
        print("  Verified .close-btn.")

        browser.close()
        print("All tests passed!")

if __name__ == "__main__":
    test_a11y_labels()

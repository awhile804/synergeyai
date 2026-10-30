from playwright.sync_api import sync_playwright
import os

def run_cuj(page):
    page.goto(f"file://{os.path.abspath('transcript-analyzer.html')}")
    page.wait_for_timeout(500)

    # Inject mock state for Playwright testing
    page.evaluate('''
        window.CATEGORIES = {
            new_tasks: { id: 'new_tasks', title: 'New Tasks', icon: '📝', color: 'var(--success)' },
        };
        suggestions = [{
            id: 1,
            status: 'pending',
            category: 'new_tasks',
            meta: {},
            data: { title: 'Test Suggestion' }
        }];
        document.getElementById('resultsSection').classList.add('visible');
        renderSuggestions();
    ''')
    page.wait_for_timeout(1000)

    # Verify buttons have the ARIA labels and title we added
    approve_btn = page.locator("button[aria-label='Approve suggestion']")
    edit_btn = page.locator("button[aria-label='Edit suggestion']")
    reject_btn = page.locator("button[aria-label='Reject suggestion']")

    assert approve_btn.is_visible()
    assert edit_btn.is_visible()
    assert reject_btn.is_visible()

    assert approve_btn.get_attribute("title") == "Approve suggestion"
    assert edit_btn.get_attribute("title") == "Edit suggestion"
    assert reject_btn.get_attribute("title") == "Reject suggestion"

    page.wait_for_timeout(500)
    page.screenshot(path="/home/jules/verification/screenshots/verification.png")
    page.wait_for_timeout(1000)

if __name__ == "__main__":
    os.makedirs("/home/jules/verification/screenshots", exist_ok=True)
    os.makedirs("/home/jules/verification/videos", exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )
        page = context.new_page()
        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()

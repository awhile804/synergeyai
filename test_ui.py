import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Handle dialogs automatically to avoid blocking
        page.on("dialog", lambda dialog: dialog.accept())

        # Load the index page directly without mock DB first
        # We need the real functions to initialize
        await page.goto("file:///app/index.html")
        await page.wait_for_load_state('domcontentloaded')

        print("--- Testing ARIA Labels ---")

        # Make project available
        await page.evaluate("localStorage.setItem('selectedProject', 'test-project')")

        # Test modal close button
        await page.evaluate("openAddStoryModal()")

        close_btn = page.locator('#addStoryModal .modal-close')
        await close_btn.wait_for(state='visible')
        aria_label = await close_btn.get_attribute('aria-label')
        print(f"Modal close button aria-label: {aria_label}")
        assert aria_label == 'Close'

        print("\n--- Testing Loading States ---")

        # Add mock DB inside the browser context so async operations actually run but use mock
        await page.evaluate("""
            window.db = {
                collection: () => ({
                    doc: () => ({
                        get: async () => new Promise(resolve => setTimeout(() => resolve({
                            exists: true,
                            data: () => ({ userStories: [] })
                        }), 500)),
                        update: async () => new Promise(resolve => setTimeout(resolve, 500))
                    })
                })
            };
        """)

        # Add Story Loading state
        await page.fill('#newStoryText', 'Test Story')
        await page.fill('#newStoryEpic', 'Test Epic')

        save_btn = page.locator('#saveNewStoryBtn')
        await save_btn.click()

        is_disabled = await save_btn.is_disabled()
        print(f"Is save button disabled during operation?: {is_disabled}")
        assert is_disabled == True

        html_content = await save_btn.inner_html()
        print(f"Button HTML during operation: {html_content}")
        assert "ai-loading" in html_content

        # Wait for finally block to execute
        await page.wait_for_timeout(1000)

        is_disabled_after = await save_btn.is_disabled()
        print(f"Is save button disabled after operation?: {is_disabled_after}")
        assert is_disabled_after == False

        text_after = await save_btn.inner_text()
        print(f"Button text after operation: {text_after}")
        assert "Add User Story" in text_after

        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())

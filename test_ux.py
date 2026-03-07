import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Mock Firebase responses and add delay to simulate network latency
        await page.add_init_script("""
            window.mockFirebase = true;
            window.localStorage.setItem('selectedProject', 'test-project');

            // Mock alert to prevent dialog hanging
            window.alert = function(msg) { console.log('Alert called:', msg); };

            // Re-mock firebase after it loads to ensure we intercept it
            document.addEventListener("DOMContentLoaded", () => {
                const delayedPromise = () => new Promise(resolve => setTimeout(resolve, 500));

                window.db = {
                    collection: function() {
                        return {
                            doc: function() {
                                return {
                                    get: async function() {
                                        return {
                                            exists: true,
                                            data: () => ({ userStories: [], sprintData: [] })
                                        };
                                    },
                                    update: async function(data) {
                                        await delayedPromise();
                                        return true;
                                    },
                                    onSnapshot: function() {
                                        return function unsubscribe() {};
                                    }
                                };
                            },
                            get: async function() {
                                return {
                                    forEach: function(cb) {
                                        cb({ id: 'test-project', data: () => ({ config: { name: 'Test' } }) });
                                    },
                                    size: 1
                                };
                            }
                        };
                    }
                };
            });
        """)

        print("Navigating to index.html...")
        await page.goto("file:///app/index.html")
        await page.wait_for_load_state('domcontentloaded')

        # Test 1: Add New User Story Button
        print("\nTesting 'Add New User Story' button loading state...")
        # The modal is hidden, we must open it first to make fields visible
        await page.click("#addStoryBtn")
        await page.wait_for_selector("#newStoryText", state="visible")

        # Fill in required fields to pass validation
        await page.fill("#newStoryText", "As a test user, I want to save a story.")
        await page.fill("#newStoryEpic", "Test Epic")

        # Click the button
        print("Clicking Add User Story...")

        # We don't await the click yet because we need to check the state immediately after
        click_task = asyncio.create_task(page.click("#saveNewStoryBtn", force=True))

        # Give it a tiny bit of time for the JS to execute and update the DOM
        await asyncio.sleep(0.1)

        # Check if button is disabled
        is_disabled = await page.evaluate("document.getElementById('saveNewStoryBtn').disabled")
        print(f"Is Add Story button disabled? {is_disabled}")

        # Check if spinner is present
        has_spinner = await page.evaluate("document.getElementById('saveNewStoryBtn').querySelector('.ai-loading') !== null")
        print(f"Does Add Story button have spinner? {has_spinner}")

        # Check inline styles on spinner for contrast (yellow background)
        spinner_styles = await page.evaluate("""
            const spinner = document.getElementById('saveNewStoryBtn').querySelector('.ai-loading');
            spinner ? {
                borderColor: spinner.style.borderColor,
                borderTopColor: spinner.style.borderTopColor
            } : null
        """)
        print(f"Spinner contrast styles: {spinner_styles}")

        # Wait for the click/save operation to complete (our mock takes 500ms)
        await click_task
        await asyncio.sleep(0.6)

        # Check if button state is restored
        is_disabled_after = await page.evaluate("document.getElementById('saveNewStoryBtn').disabled")
        has_spinner_after = await page.evaluate("document.getElementById('saveNewStoryBtn').querySelector('.ai-loading') !== null")
        btn_text_after = await page.evaluate("document.getElementById('saveNewStoryBtn').innerHTML")

        print(f"Is Add Story button disabled after completion? {is_disabled_after}")
        print(f"Does Add Story button have spinner after completion? {has_spinner_after}")
        print(f"Restored button text: '{btn_text_after.strip()}'")

        # Test 2: Project Settings Button
        print("\nTesting 'Project Settings' button loading state...")

        # We must open the modal first
        await page.evaluate("openProjectSettingsModal()")
        await page.wait_for_selector("#saveSettingsBtn", state="visible")

        # Click the button
        print("Clicking Save Settings...")

        # We don't await the click yet because we need to check the state immediately after
        click_task = asyncio.create_task(page.click("#saveSettingsBtn", force=True))

        # Give it a tiny bit of time for the JS to execute and update the DOM
        await asyncio.sleep(0.1)

        # Check if button is disabled
        is_disabled = await page.evaluate("document.getElementById('saveSettingsBtn').disabled")
        print(f"Is Save Settings button disabled? {is_disabled}")

        # Check if spinner is present
        has_spinner = await page.evaluate("document.getElementById('saveSettingsBtn').querySelector('.ai-loading') !== null")
        print(f"Does Save Settings button have spinner? {has_spinner}")

        # Wait for the click/save operation to complete
        await click_task
        await asyncio.sleep(0.6)

        # Check if button state is restored
        is_disabled_after = await page.evaluate("document.getElementById('saveSettingsBtn').disabled")
        has_spinner_after = await page.evaluate("document.getElementById('saveSettingsBtn').querySelector('.ai-loading') !== null")
        btn_text_after = await page.evaluate("document.getElementById('saveSettingsBtn').innerHTML")

        print(f"Is Save Settings button disabled after completion? {is_disabled_after}")
        print(f"Does Save Settings button have spinner after completion? {has_spinner_after}")
        print(f"Restored button text: '{btn_text_after.strip()}'")

        await browser.close()
        print("\nVerification complete!")

if __name__ == "__main__":
    asyncio.run(run())

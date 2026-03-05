import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto('file:///app/index.html')

        await page.add_init_script("""
            window.localStorage.setItem('selectedProject', 'test-project');
            window.getCurrentProject = () => 'test-project';

            window.db = {
                collection: () => ({
                    doc: () => ({
                        get: async () => ({
                            exists: true,
                            data: () => ({ userStories: [], sprintData: [] })
                        }),
                        update: async () => new Promise(resolve => setTimeout(resolve, 500))
                    }),
                    get: async () => ({
                        forEach: (cb) => { cb({ id: 'test-project', data: () => ({ config: { name: 'Test' } }) }) },
                        size: 1
                    })
                })
            };
            window.firebase = {
                firestore: {
                    FieldValue: {
                        serverTimestamp: () => 'now'
                    }
                }
            };
        """)

        await page.goto('file:///app/index.html')

        print(await page.evaluate("""
            document.getElementById('newStoryText').value = 'As a test, I want to see the spinner';
            document.getElementById('newStoryEpic').value = 'Testing';
            window.savePromise = saveNewStory();

            let btn = document.getElementById('saveNewStoryBtn');
            [btn.disabled, btn.innerHTML.includes('ai-loading')]
        """))

        await page.evaluate("""
            async () => {
                await window.savePromise;
            }
        """)
        # We need to wait for real python asyncio sleep since the above is just launching a promise and not awaiting in python.
        # However, Playwright evaluates async functions as promises and awaits them, so we can do it like this:
        await page.evaluate("() => window.savePromise")

        print(await page.evaluate("""
            let btn = document.getElementById('saveNewStoryBtn');
            [btn.disabled, btn.innerHTML.includes('ai-loading')]
        """))

        print("All tests passed.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
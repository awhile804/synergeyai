import asyncio
from playwright.async_api import async_playwright
import re

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # We navigate to about:blank to test the HTML generation function independently
        await page.goto("about:blank")

        # Extract the function to test
        with open('transcript-analyzer.html', 'r') as f:
            content = f.read()

        render_function = re.search(r'function renderSuggestionCard\(suggestion\) \{.*?return `.*?`;\n        \}', content, re.DOTALL)
        render_edit_form = re.search(r'function renderEditForm\(suggestion\) \{.*?return `.*?`;\n        \}', content, re.DOTALL)

        if not render_function or not render_edit_form:
            print("Could not find render functions!")
            return

        # Add necessary global variables and the function
        await page.evaluate("""
            window.CATEGORIES = {
                'new_tasks': {title: 'New Tasks', icon: '📝'},
                'modifications': {title: 'Modifications', icon: '🔄'}
            };
            window.suggestions = [
                {
                    id: 1,
                    status: 'pending',
                    category: 'new_tasks',
                    data: { title: 'Test suggestion 1' },
                    meta: { epic: 'Test Epic', priority: 'High' }
                },
                {
                    id: 2,
                    status: 'approved',
                    category: 'modifications',
                    data: { title: 'Test suggestion 2' },
                    meta: { epic: 'Test Epic' }
                },
                {
                    id: 3,
                    status: 'rejected',
                    category: 'new_tasks',
                    data: { title: 'Test suggestion 3' },
                    meta: {}
                }
            ];

            window.renderSuggestionCard = """ + render_function.group(0) + """;
            window.renderEditForm = """ + render_edit_form.group(0) + """;

            window.escapeHtml = function(text) {
                if (!text) return '';
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
        """)

        # Test the rendering
        for i in range(3):
            html = await page.evaluate(f"window.renderSuggestionCard(window.suggestions[{i}])")
            await page.set_content(html)

            print(f"--- Suggestion {i+1} ---")

            if i == 0: # Pending
                btn_approve = await page.query_selector("button[aria-label='Approve suggestion']")
                print(f"Approve button title: {await btn_approve.get_attribute('title')}")

                btn_edit = await page.query_selector("button[aria-label='Edit suggestion']")
                print(f"Edit button title: {await btn_edit.get_attribute('title')}")

                btn_reject = await page.query_selector("button[aria-label='Reject suggestion']")
                print(f"Reject button title: {await btn_reject.get_attribute('title')}")

            elif i == 1: # Approved
                btn_undo = await page.query_selector("button[aria-label='Undo approval']")
                print(f"Undo approval button title: {await btn_undo.get_attribute('title')}")

            elif i == 2: # Rejected
                btn_undo = await page.query_selector("button[aria-label='Undo rejection']")
                print(f"Undo rejection button title: {await btn_undo.get_attribute('title')}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

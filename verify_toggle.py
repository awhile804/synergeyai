import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Testing index.html...")
        await page.goto("file:///app/index.html", wait_until="domcontentloaded")

        # Mock getCurrentProject and DB to allow openProjectSettingsModal to work
        await page.evaluate("""
            window.getCurrentProject = () => 'test-project';
            window.db = {
                collection: () => ({
                    doc: () => ({
                        get: async () => ({
                            exists: true,
                            data: () => ({ settings: {} })
                        }),
                        update: async () => {}
                    })
                })
            };
        """)

        # Test GitHub Token Toggle
        await page.evaluate("openProjectSettingsModal()")
        await page.wait_for_selector("#projectSettingsModal.visible")

        github_input = page.locator("#settingsGitHubToken")
        github_btn = page.locator("#settingsGitHubToken + button")

        assert await github_input.get_attribute("type") == "password", "GitHub token should initially be password"
        assert await github_btn.text_content() == "Show", "GitHub token button should initially be 'Show'"

        await github_btn.click()
        assert await github_input.get_attribute("type") == "text", "GitHub token should be text after click"
        assert await github_btn.text_content() == "Hide", "GitHub token button should be 'Hide' after click"

        await github_btn.click()
        assert await github_input.get_attribute("type") == "password", "GitHub token should be password after second click"
        assert await github_btn.text_content() == "Show", "GitHub token button should be 'Show' after second click"

        # Test OpenAI Key Toggle
        openai_input = page.locator("#settingsOpenAIKey")
        openai_btn = page.locator("#settingsOpenAIKey + button")

        assert await openai_input.get_attribute("type") == "password", "OpenAI token should initially be password"
        assert await openai_btn.text_content() == "Show", "OpenAI token button should initially be 'Show'"

        await openai_btn.click()
        assert await openai_input.get_attribute("type") == "text", "OpenAI token should be text after click"
        assert await openai_btn.text_content() == "Hide", "OpenAI token button should be 'Hide' after click"

        # Change state and reopen the modal again to check reset state
        await github_btn.click() # changes back to text
        await page.evaluate("closeProjectSettingsModal()")
        await asyncio.sleep(0.5)

        await page.evaluate("openProjectSettingsModal()")
        await page.wait_for_selector("#projectSettingsModal.visible")

        assert await github_input.get_attribute("type") == "password", "GitHub token should be password after reopen"
        assert await github_btn.text_content() == "Show", "GitHub token button should be 'Show' after reopen"
        assert await openai_input.get_attribute("type") == "password", "OpenAI token should be password after reopen"
        assert await openai_btn.text_content() == "Show", "OpenAI token button should be 'Show' after reopen"

        print("index.html tests passed.")

        print("Testing transcript-analyzer.html...")
        await page.goto("file:///app/transcript-analyzer.html", wait_until="domcontentloaded")

        api_key_input = page.locator("#apiKeyInput")
        api_key_btn = page.locator("#apiKeyInput + button")

        assert await api_key_input.get_attribute("type") == "password", "API key should initially be password"
        assert await api_key_btn.text_content() == "Show", "API key button should initially be 'Show'"

        await api_key_btn.click()
        assert await api_key_input.get_attribute("type") == "text", "API key should be text after click"
        assert await api_key_btn.text_content() == "Hide", "API key button should be 'Hide' after click"

        print("transcript-analyzer.html tests passed.")

        await browser.close()

asyncio.run(run())

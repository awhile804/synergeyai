from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Same mock Firebase setup to load index.html without errors
        page.add_init_script("""
            window.firebase = {
                initializeApp: function() { return {}; },
                firestore: function() {
                    return {
                        collection: function(colName) {
                            return {
                                get: async function() {
                                    return { forEach: function(cb) { cb({ id: 'mock', data: () => ({ config: { name: 'Mock' } }) }); }, size: 1 };
                                },
                                doc: function() {
                                    return {
                                        get: async function() { return { exists: true, data: () => ({ config: {}, userStories: [], sprintData: [] }) }; },
                                        onSnapshot: function(cb) { return function() {}; }
                                    };
                                }
                            };
                        }
                    };
                }
            };
            window.localStorage.setItem('selectedProject', 'mock_project');
        """)

        page.route("**/*firebase*", lambda route: route.abort())
        page.goto("file:///app/index.html")

        # Wait for the page to load
        page.wait_for_selector(".filters-section", state="attached")

        # Test filter labels
        page.click("label[for='searchInput']")
        assert page.evaluate("document.activeElement.id") == "searchInput", "searchInput not focused by label"

        page.click("label[for='epicFilter']")
        assert page.evaluate("document.activeElement.id") == "epicFilter", "epicFilter not focused by label"

        # Open Add Story modal and test a label
        page.click("#addStoryBtn")
        page.wait_for_selector("#addStoryModal.visible")

        page.click("label[for='newStoryText']")
        assert page.evaluate("document.activeElement.id") == "newStoryText", "newStoryText not focused by label"

        page.click("label[for='newStoryEpic']")
        assert page.evaluate("document.activeElement.id") == "newStoryEpic", "newStoryEpic not focused by label"

        page.click("button[aria-label='Close add story modal']")

        # Open Settings modal and test a label
        page.click(".settings-btn")
        page.wait_for_selector("#projectSettingsModal.visible")

        page.click("label[for='settingsGitHubRepo']")
        assert page.evaluate("document.activeElement.id") == "settingsGitHubRepo", "settingsGitHubRepo not focused by label"

        print("All label verification tests passed successfully!")

        browser.close()

if __name__ == "__main__":
    verify()

import time
from playwright.sync_api import sync_playwright

def verify_ui_changes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Add init script to mock Firebase and localStorage
        page.add_init_script("""
            window.localStorage.setItem('selectedProject', 'mock_project');
            window.firebase = {
                initializeApp: function() {},
                firestore: Object.assign(function() {
                    return {
                        collection: function(col) {
                            return {
                                doc: function(docId) {
                                    return {
                                        get: function() {
                                            return new Promise((resolve) => {
                                                resolve({
                                                    exists: true,
                                                    data: function() {
                                                        return {
                                                            userStories: [
                                                                {
                                                                    Story_ID: "US-001",
                                                                    User_Story: "As a user, I want to login.",
                                                                    Epic: "Auth",
                                                                    Status: "Yet to start",
                                                                    Effort_Required: 5
                                                                }
                                                            ],
                                                            sprintData: [
                                                                {Sprint: 1, Theme: "Foundation"}
                                                            ],
                                                            settings: {
                                                                githubRepo: "mock/repo",
                                                                githubToken: "token",
                                                                githubBranch: "main",
                                                                openaiKey: "sk-mock"
                                                            }
                                                        };
                                                    }
                                                });
                                            });
                                        },
                                        update: function() {
                                            return new Promise(resolve => setTimeout(resolve, 500));
                                        },
                                        onSnapshot: function(callback) {
                                            // Provide initial data
                                            callback({
                                                exists: true,
                                                data: function() {
                                                    return {
                                                        userStories: [
                                                            {
                                                                Story_ID: "US-001",
                                                                User_Story: "As a user, I want to login.",
                                                                Epic: "Auth",
                                                                Status: "Yet to start",
                                                                Effort_Required: 5
                                                            }
                                                        ]
                                                    };
                                                }
                                            });
                                            return function() {};
                                        }
                                    };
                                },
                                get: function() {
                                    return new Promise((resolve) => {
                                        resolve({
                                            forEach: function(callback) {
                                                callback({ id: 'mock_project', data: () => ({ config: { name: 'Mock Project' } }) });
                                            },
                                            size: 1
                                        });
                                    });
                                }
                            };
                        }
                    };
                }, {
                    FieldValue: { serverTimestamp: function() { return 'timestamp'; } }
                })
            };
        """)

        # Navigate to the page
        page.goto("http://localhost:8000/index.html")
        page.wait_for_load_state('domcontentloaded')

        # Test "Add User Story"
        print("Testing Add User Story button...")
        page.click("#addStoryBtn")
        page.wait_for_selector("#addStoryModal", state="visible")
        page.fill("#newStoryText", "New story test")
        page.fill("#newStoryEpic", "New epic")

        save_new_btn = page.locator("#saveNewStoryBtn")
        assert save_new_btn.is_visible()

        # Click save and check intermediate loading state
        save_new_btn.click()
        assert save_new_btn.is_disabled()
        assert page.locator("#saveNewStoryBtn .ai-loading").is_visible()
        assert "Saving..." in save_new_btn.inner_text()

        # Wait for operation to complete (simulated 500ms delay in mock update)
        time.sleep(1)

        # In the app, modal closes immediately, but let's check the button state directly
        assert not save_new_btn.is_disabled()
        assert "Add User Story" in save_new_btn.inner_text()

        # Reopen to test reset state
        page.click("#addStoryBtn")
        page.wait_for_selector("#addStoryModal", state="visible")
        assert not save_new_btn.is_disabled()
        assert "Add User Story" in save_new_btn.inner_text()
        page.click("#addStoryModal .modal-close")

        # Wait a moment for UI to settle
        time.sleep(0.5)

        # Test "Edit User Story"
        print("Testing Edit User Story button...")
        page.evaluate("openEditStoryModal('US-001')") # Explicitly call JS to open modal since click on table might be flaky due to mock
        page.wait_for_selector("#editStoryModal", state="visible")
        page.fill("#editStoryText", "Updated story")
        page.fill("#editStoryEpic", "Updated epic")

        save_edit_btn = page.locator("#saveEditStoryBtn")
        assert save_edit_btn.is_visible()

        save_edit_btn.click()
        assert save_edit_btn.is_disabled()
        assert page.locator("#saveEditStoryBtn .ai-loading").is_visible()
        assert "Saving..." in save_edit_btn.inner_text()

        time.sleep(1)

        # Reopen to test reset state
        page.evaluate("openEditStoryModal('US-001')")
        page.wait_for_selector("#editStoryModal", state="visible")
        assert not save_edit_btn.is_disabled()
        assert "Save Changes" in save_edit_btn.inner_text()
        page.click("#editStoryModal .modal-close")

        # Handle alert in project settings mock
        page.on("dialog", lambda dialog: dialog.accept())

        # Wait a moment for UI to settle
        time.sleep(0.5)

        # Test "Project Settings"
        print("Testing Project Settings button...")
        page.click(".settings-btn")
        page.wait_for_selector("#projectSettingsModal", state="visible")

        save_settings_btn = page.locator("#saveSettingsBtn")
        assert save_settings_btn.is_visible()

        save_settings_btn.click()
        assert save_settings_btn.is_disabled()
        assert page.locator("#saveSettingsBtn .ai-loading").is_visible()
        assert "Saving..." in save_settings_btn.inner_text()

        time.sleep(1)

        # Reopen to test reset state
        page.click(".settings-btn")
        page.wait_for_selector("#projectSettingsModal", state="visible")
        assert not save_settings_btn.is_disabled()
        assert "Save Settings" in save_settings_btn.inner_text()

        print("All tests passed!")
        browser.close()

if __name__ == "__main__":
    verify_ui_changes()

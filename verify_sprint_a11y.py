from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Mock Firebase fully as per memory constraints
        page.add_init_script("""
            window.firebase = {
                initializeApp: function() { return {}; },
                firestore: function() {
                    const db = {
                        collection: function(colName) {
                            return {
                                get: async function() {
                                    if (colName === 'projects') {
                                        return {
                                            forEach: function(cb) {
                                                cb({ id: 'mock_project', data: () => ({ config: { name: 'Mock Project' } }) });
                                            },
                                            size: 1
                                        };
                                    }
                                    return { forEach: function() {}, size: 0 };
                                },
                                doc: function(docId) {
                                    return {
                                        get: async function() {
                                            return {
                                                exists: true,
                                                data: () => ({
                                                    config: { name: 'Mock Project' },
                                                    sprintData: [
                                                        {
                                                            Sprint: 1,
                                                            Type: 'Task',
                                                            Description: 'Mock Task',
                                                            Status: 'Not Started'
                                                        }
                                                    ],
                                                    effortData: { summary: {}, modules: [] }
                                                })
                                            };
                                        },
                                        onSnapshot: function(cb) {
                                            cb({
                                                exists: true,
                                                data: () => ({
                                                    config: { name: 'Mock Project' },
                                                    sprintData: [
                                                        {
                                                            Sprint: 1,
                                                            Type: 'Task',
                                                            Description: 'Mock Task',
                                                            Status: 'Not Started'
                                                        }
                                                    ],
                                                    effortData: { summary: {}, modules: [] }
                                                })
                                            });
                                            return function() {}; // unsubscribe
                                        }
                                    };
                                }
                            };
                        }
                    };
                    return db;
                }
            };
            window.localStorage.setItem('selectedProject', 'mock_project');
        """)

        # Abort CDN requests for real firebase scripts as they might conflict
        page.route("**/*firebase*", lambda route: route.abort())

        page.goto("file:///app/sprint-planner.html")

        # Open sprint detail modal
        page.wait_for_selector(".view-tab.active", state="attached")
        page.evaluate("openSprintDetail(1)")

        # Verify close button accessibility
        close_btn = page.locator(".sprint-detail-panel .close-btn")
        assert close_btn.get_attribute("aria-label") == "Close sprint details", "Close button aria-label missing or incorrect"
        assert close_btn.get_attribute("title") == "Close sprint details", "Close button title missing or incorrect"

        # Verify expand button initial accessibility
        expand_btn = page.locator("#expand-btn-0")
        assert expand_btn.get_attribute("aria-label") == "Toggle task details", "Expand button aria-label missing or incorrect"
        assert expand_btn.get_attribute("title") == "Toggle task details", "Expand button title missing or incorrect"
        assert expand_btn.get_attribute("aria-expanded") == "false", "Expand button aria-expanded initial state incorrect"
        assert expand_btn.get_attribute("aria-controls") == "task-body-0", "Expand button aria-controls missing or incorrect"

        # Click expand button and verify state changes
        expand_btn.click()
        assert expand_btn.get_attribute("aria-expanded") == "true", "Expand button aria-expanded state not updated after click"

        # Click again to close and verify state changes
        expand_btn.click()
        assert expand_btn.get_attribute("aria-expanded") == "false", "Expand button aria-expanded state not updated after second click"

        print("Sprint Planner accessibility tests passed successfully!")

        browser.close()

if __name__ == "__main__":
    verify()

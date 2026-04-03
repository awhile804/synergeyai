from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use context to easily record video
        context = browser.new_context(record_video_dir="/home/jules/verification/videos/")
        page = context.new_page()

        # Fully mock firebase to prevent hanging
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
                                                    userStories: [],
                                                    sprintData: [
                                                        { Sprint: 1, Type: 'Task', Description: 'Mock Task 1', Status: 'In Progress', Start_Date: '2024-01-01', End_Date: '2024-01-05', Duration: 5 }
                                                    ],
                                                    effortData: { modules: [], summary: {} }
                                                })
                                            };
                                        },
                                        onSnapshot: function(cb) {
                                            cb({
                                                exists: true,
                                                data: () => ({
                                                    config: { name: 'Mock Project' },
                                                    userStories: [],
                                                    sprintData: [
                                                        { Sprint: 1, Type: 'Task', Description: 'Mock Task 1', Status: 'In Progress', Start_Date: '2024-01-01', End_Date: '2024-01-05', Duration: 5 }
                                                    ],
                                                    effortData: { modules: [], summary: {} }
                                                })
                                            });
                                            return function() {};
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

        page.route("**/*firebase*", lambda route: route.abort())
        page.goto("file:///app/sprint-planner.html")

        # Open sprint detail modal
        # Since the page creates sprint-0 card based on the mock data which lacks sprint definition but has tasks with Sprint=1
        # Let's just wait for the page to load by waiting for overview tab to be active
        page.wait_for_selector(".view-tab.active")

        # Manually trigger openSprintDetail(1)
        page.evaluate("openSprintDetail(1)")

        page.wait_for_selector("#sprintDetailOverlay.show")

        close_btn = page.locator(".close-btn")
        assert close_btn.get_attribute("aria-label") == "Close sprint details", "Close button missing aria-label"

        expand_btn = page.locator(".detail-task-expand")
        assert expand_btn.get_attribute("aria-label") == "Toggle task details", "Expand button missing aria-label"
        assert expand_btn.get_attribute("aria-expanded") == "false", "Expand button aria-expanded should be false initially"

        # Click the expand button directly
        expand_btn.click()

        # Verify expanded
        assert expand_btn.get_attribute("aria-expanded") == "true", "Expand button aria-expanded should be true after click"

        # Click row to toggle
        page.locator(".detail-task-header").click()
        assert expand_btn.get_attribute("aria-expanded") == "false", "Expand button aria-expanded should be false after toggling off"

        page.screenshot(path="/home/jules/verification/screenshots/sprint_planner_accessibility.png", full_page=True)

        print("Accessibility verification passed!")

        # Close explicitly to save video
        page.close()
        context.close()
        browser.close()

if __name__ == "__main__":
    verify()
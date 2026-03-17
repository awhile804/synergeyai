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
                                                    userStories: [
                                                        { Story_ID: 'US-001', User_Story: 'Test Story', Status: 'In Progress' }
                                                    ],
                                                    sprintData: []
                                                })
                                            };
                                        },
                                        onSnapshot: function(cb) {
                                            cb({
                                                exists: true,
                                                data: () => ({
                                                    config: { name: 'Mock Project' },
                                                    userStories: [
                                                        { Story_ID: 'US-001', User_Story: 'Test Story', Status: 'In Progress' }
                                                    ],
                                                    sprintData: []
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

        page.goto("file:///app/index.html")

        # Wait for the table to render the mock data
        page.wait_for_selector(".stories-table tr#row-0", state="attached")

        # Verify modal close buttons
        modals_close = page.locator(".modal-close")
        assert modals_close.count() == 3, f"Expected 3 modal close buttons, found {modals_close.count()}"

        # We know the order from HTML: Add Story, Edit Story, Project Settings
        assert modals_close.nth(0).get_attribute("aria-label") == "Close add story modal", "Add Story close button aria-label missing or incorrect"
        assert modals_close.nth(1).get_attribute("aria-label") == "Close edit story modal", "Edit Story close button aria-label missing or incorrect"
        assert modals_close.nth(2).get_attribute("aria-label") == "Close project settings modal", "Project Settings close button aria-label missing or incorrect"

        # Verify action buttons in the row
        row = page.locator(".stories-table tr#row-0")

        edit_btn = row.locator(".action-btn.edit")
        assert edit_btn.get_attribute("aria-label") == "Edit story US-001", "Edit button aria-label missing or incorrect"

        complete_btn = row.locator(".action-btn.complete")
        assert complete_btn.get_attribute("aria-label") == "Mark story US-001 complete", "Complete button aria-label missing or incorrect"

        delete_btn = row.locator(".action-btn.delete")
        assert delete_btn.get_attribute("aria-label") == "Delete story US-001", "Delete button aria-label missing or incorrect"

        print("All accessibility tests passed successfully!")

        browser.close()

if __name__ == "__main__":
    verify()

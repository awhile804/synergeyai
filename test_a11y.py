import os
import sys
import time
from playwright.sync_api import sync_playwright

def verify_a11y():
    print("Starting Playwright a11y verification...")

    # Path to the local HTML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_url = f"file://{current_dir}/index.html"

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Abort requests to external scripts to avoid flakiness and ensure mocks persist
        def abort_cdn(route):
            if "firebasejs" in route.request.url or "gstatic" in route.request.url:
                route.abort()
            else:
                route.continue_()

        page.route("**/*", abort_cdn)

        # Add init script to mock Firebase and automatically bypass project selection
        page.add_init_script("""
            window.firebase = {
                initializeApp: () => ({}),
                firestore: () => ({
                    collection: () => ({
                        doc: () => ({
                            get: () => Promise.resolve({
                                exists: true,
                                data: () => ({
                                    config: { name: "Mock Project" },
                                    userStories: [
                                        {
                                            Story_ID: "US-001",
                                            User_Story: "Test Story",
                                            Epic: "Test Epic",
                                            Feature: "Test Feature",
                                            Status: "In Progress",
                                            Priority: "High"
                                        }
                                    ]
                                })
                            }),
                            onSnapshot: (cb) => {
                                cb({
                                    exists: true,
                                    data: () => ({
                                        userStories: [
                                            {
                                                Story_ID: "US-001",
                                                User_Story: "Test Story",
                                                Epic: "Test Epic",
                                                Feature: "Test Feature",
                                                Status: "In Progress",
                                                Priority: "High"
                                            }
                                        ]
                                    })
                                });
                                return () => {};
                            }
                        }),
                        get: () => Promise.resolve({
                            size: 1,
                            forEach: (cb) => {
                                cb({
                                    id: "mock_project",
                                    data: () => ({ config: { name: "Mock Project" } })
                                });
                            }
                        })
                    })
                })
            };
            window.localStorage.setItem('selectedProject', 'mock_project');
        """)

        # Load the page
        print(f"Loading {file_url}...")
        page.goto(file_url)

        # Automatically accept dialogs to prevent hanging
        page.on("dialog", lambda dialog: dialog.accept())

        print("Checking .modal-close buttons...")
        # Verify modal close buttons have aria-label
        close_buttons = page.locator(".modal-close")
        count = close_buttons.count()
        assert count == 3, f"Expected 3 modal-close buttons, found {count}"

        labels = [
            "Close add story modal",
            "Close edit story modal",
            "Close project settings modal"
        ]

        for i in range(count):
            label = close_buttons.nth(i).get_attribute("aria-label")
            assert label == labels[i], f"Expected label '{labels[i]}', found '{label}'"

        print("Checking action buttons in table...")
        # Wait for the table to populate with the mock data
        page.wait_for_selector(".action-btn.edit")

        # Verify action buttons have correct aria-labels
        edit_btn = page.locator(".action-btn.edit").first
        edit_label = edit_btn.get_attribute("aria-label")
        assert edit_label == "Edit story US-001", f"Expected Edit story US-001, found {edit_label}"

        complete_btn = page.locator(".action-btn.complete").first
        complete_label = complete_btn.get_attribute("aria-label")
        assert complete_label == "Mark story US-001 complete", f"Expected Mark story US-001 complete, found {complete_label}"

        delete_btn = page.locator(".action-btn.delete").first
        delete_label = delete_btn.get_attribute("aria-label")
        assert delete_label == "Delete story US-001", f"Expected Delete story US-001, found {delete_label}"

        print("Checking toggle expansion logic...")
        # Verify details toggle has initial aria-expanded="false" and aria-controls
        details_btn = page.locator(".action-btn.details").first

        # In the render we gave it an id like details-btn-0
        assert details_btn.get_attribute("aria-expanded") == "false", "Expected aria-expanded to be false initially"
        assert details_btn.get_attribute("aria-controls") == "expanded-0", "Expected aria-controls to be expanded-0"

        # Click the toggle
        details_btn.click()

        # Verify it changes to true
        assert details_btn.get_attribute("aria-expanded") == "true", "Expected aria-expanded to be true after clicking"

        # The expanded content should be visible (display: table-row)
        expanded_row = page.locator("#expanded-0")
        assert expanded_row.is_visible(), "Expected expanded row to be visible"

        print("All a11y tests passed!")
        browser.close()

if __name__ == "__main__":
    verify_a11y()

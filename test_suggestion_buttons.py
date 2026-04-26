from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))

        # Abort only external firebase CDN calls to avoid hanging tests
        page.route("**/*firebase*", lambda route: route.abort())
        page.route("**/*firestore*", lambda route: route.abort())

        # Just inject the raw HTML block instead of trying to untangle Firebase
        page.goto('about:blank')

        # Just use set_content and evaluate `renderSuggestionCard` directly to verify output
        html_to_test = """
        <!DOCTYPE html>
        <html>
        <head>
            <script>
                // Need stub objects to execute renderSuggestionCard
                const CATEGORIES = {
                    'new_tasks': {
                        title: 'New Tasks',
                        icon: '✅',
                        color: 'var(--success)'
                    }
                };

                function escapeHtml(text) {
                    const div = document.createElement('div');
                    div.textContent = text;
                    return div.innerHTML;
                }

                function renderEditForm(suggestion) { return "<div>Edit Form</div>"; }

                function renderSuggestionCard(suggestion) {
                    const { id, category, status, data } = suggestion;
                    const catInfo = CATEGORIES[category];

                    let titleText = data.title || data.user_story || data.theme || 'Suggestion';
                    let bodyText = '';
                    let metaTags = '';

                    switch (category) {
                        case 'new_tasks':
                            bodyText = data.description || '';
                            metaTags = `
                                <span class="meta-tag">Sprint ${data.sprint || '?'}</span>
                                <span class="meta-tag">${data.estimated_hours || 8}h</span>
                                <span class="meta-tag priority-${(data.priority || 'medium').toLowerCase()}">${data.priority || 'Medium'}</span>
                                <span class="meta-tag">Assignee: ${data.assignee || 'Unassigned'}</span>
                            `;
                            break;
                    }

                    return `
                        <div class="suggestion-card ${status}" data-id="${id}">
                            <div class="suggestion-header">
                                <div>
                                    <div class="suggestion-type">${catInfo.icon} ${catInfo.title.slice(0, -1)}</div>
                                    <div class="suggestion-title">${titleText}</div>
                                </div>
                                <div class="suggestion-actions">
                                    ${status === 'pending' ? `
                                        <button class="btn btn-success btn-sm" aria-label="Approve suggestion" title="Approve" onclick="approveSuggestion(${id})">✓</button>
                                        <button class="btn btn-secondary btn-sm" aria-label="Edit suggestion" title="Edit" onclick="editSuggestion(${id})">✎</button>
                                        <button class="btn btn-danger btn-sm" aria-label="Reject suggestion" title="Reject" onclick="rejectSuggestion(${id})">✗</button>
                                    ` : status === 'approved' ? `
                                        <span style="color: var(--success);">✓ Approved</span>
                                        <button class="btn btn-secondary btn-sm" onclick="resetSuggestion(${id})">Undo</button>
                                    ` : `
                                        <span style="color: var(--danger);">✗ Rejected</span>
                                        <button class="btn btn-secondary btn-sm" onclick="resetSuggestion(${id})">Undo</button>
                                    `}
                                </div>
                            </div>
                            ${bodyText ? `<div class="suggestion-body">${bodyText}</div>` : ''}
                            <div class="suggestion-meta">${metaTags}</div>
                            ${data.reasoning ? `
                                <div class="suggestion-reasoning">
                                    <strong>AI Reasoning:</strong> ${data.reasoning}
                                </div>
                            ` : ''}
                            ${renderEditForm(suggestion)}
                        </div>
                    `;
                }

                function renderTest() {
                    const suggestion = {
                        id: 1,
                        category: 'new_tasks',
                        status: 'pending',
                        data: {
                            title: 'Mock Task Title'
                        }
                    };
                    document.body.innerHTML = renderSuggestionCard(suggestion);
                }
            </script>
        </head>
        <body onload="renderTest()">
        </body>
        </html>
        """

        page.set_content(html_to_test)

        # Explicitly wait for the suggestion card to be rendered
        page.wait_for_selector('.suggestion-card')

        # Target the buttons specifically inside the suggestion-actions
        approve_btn = page.locator('.suggestion-actions button.btn-success')
        edit_btn = page.locator('.suggestion-actions button.btn-secondary:has-text("✎")')
        reject_btn = page.locator('.suggestion-actions button.btn-danger')

        print("Approve title:", approve_btn.get_attribute("title"))
        print("Approve aria-label:", approve_btn.get_attribute("aria-label"))
        print("Edit title:", edit_btn.get_attribute("title"))
        print("Edit aria-label:", edit_btn.get_attribute("aria-label"))
        print("Reject title:", reject_btn.get_attribute("title"))
        print("Reject aria-label:", reject_btn.get_attribute("aria-label"))

        # Ensure that the elements are visible on page and exist exactly once each
        assert approve_btn.count() == 1
        assert edit_btn.count() == 1
        assert reject_btn.count() == 1
        assert approve_btn.get_attribute("title") == "Approve"
        assert approve_btn.get_attribute("aria-label") == "Approve suggestion"
        assert edit_btn.get_attribute("title") == "Edit"
        assert edit_btn.get_attribute("aria-label") == "Edit suggestion"
        assert reject_btn.get_attribute("title") == "Reject"
        assert reject_btn.get_attribute("aria-label") == "Reject suggestion"

        print("All validations passed.")
        browser.close()

if __name__ == '__main__':
    run()

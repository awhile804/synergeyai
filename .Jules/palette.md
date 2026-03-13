
## 2024-05-18 - Added `aria-label` to dynamic row removal buttons
**Learning:** Dynamically generated rows in forms often use icon-only buttons (like an `×`) for removal. It is critical to ensure that both the static HTML template and the JavaScript code that generates new rows include `aria-label` attributes for these buttons so they remain accessible to screen readers.
**Action:** When adding or generating dynamic form rows with icon-only actions, always verify that the template strings in JS maintain the necessary `aria-label` attributes.

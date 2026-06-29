## 2026-06-29 - Adding accessibility labels to dynamically generated icon buttons
**Learning:** Icon-only buttons rendered via JavaScript template literals lack context for screen readers and lack visual tooltips for users.
**Action:** Ensure dynamically generated UI elements like action buttons explicitly include both `aria-label` and `title` attributes.

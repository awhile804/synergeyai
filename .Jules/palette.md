## 2024-05-20 - Add ARIA Labels and Titles to Icon-Only Buttons
**Learning:** Dynamically generated UI elements, such as action buttons rendered via JavaScript template literals, often miss basic accessibility attributes like `aria-label` and `title`. This is especially common for icon-only buttons (like ✓, ✎, ✗).
**Action:** Always ensure that any icon-only button created dynamically via JavaScript includes an `aria-label` for screen reader users and a matching `title` attribute to provide native visual hover tooltips for other users.

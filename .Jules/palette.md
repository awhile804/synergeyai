## 2024-05-30 - Add ARIA attributes to expandable table rows
**Learning:** Toggle buttons that expand or collapse content (such as row details) must implement `aria-expanded` attributes to reflect their current state and `aria-controls` linked to the expanded element's ID for accessibility.
**Action:** When creating expandable rows or panels, always include `aria-expanded` and `aria-controls` on the toggle button, and update `aria-expanded` dynamically via JavaScript when the state changes.

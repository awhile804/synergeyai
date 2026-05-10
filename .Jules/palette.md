## 2024-05-10 - Accessibility Check
**Learning:** This app frequently uses toggle buttons that expand or collapse content (such as row details), but they lack aria-expanded attributes to reflect their current state, and aria-controls linked to the expanded element's ID for accessibility.
**Action:** Add aria-expanded and aria-controls attributes to toggle buttons, and dynamically update aria-expanded via JavaScript when the state changes.

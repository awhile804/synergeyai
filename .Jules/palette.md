## 2024-05-24 - [ARIA Labels on Dynamic Icon Buttons]
**Learning:** Dynamically generated UI elements created via JavaScript template strings (e.g., suggestion actions in `transcript-analyzer.html`) often lack `aria-label` and `title` attributes for icon-only action buttons.
**Action:** Always include both `aria-label` and `title` attributes for icon-only action buttons to ensure screen reader compatibility and visual hover tooltips.

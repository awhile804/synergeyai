## 2026-06-26 - [A11y on Dynamic Icon Buttons]
**Learning:** Dynamically generated UI elements created via JavaScript template strings frequently miss `aria-label` and `title` attributes for icon-only action buttons.
**Action:** Always explicitly include both `aria-label` (for screen readers) and `title` (for visual hover tooltips) when rendering icon-only buttons in template strings.

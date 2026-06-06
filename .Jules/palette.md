## 2024-05-24 - Accessibility for Icon-Only Action Buttons in Dynamic Lists
**Learning:** When generating repetitive UI elements via JavaScript template strings (like action buttons in suggestion cards), developers often omit `aria-label` and `title` attributes on icon-only buttons, reducing accessibility for screen readers and hiding context for sighted users.
**Action:** Always add both `aria-label` and `title` attributes to dynamically generated icon-only action buttons.

## 2024-05-23 - Accessibility for Dynamically Generated Icon Buttons
**Learning:** Icon-only action buttons rendered via JavaScript template strings (e.g., suggestion actions) are frequently overlooked for accessibility. Without ARIA labels, screen readers just announce the icon character, and without title attributes, visual users lack context.
**Action:** Always include both `aria-label` (for screen readers) and `title` (for visual tooltips) attributes when creating icon-only action buttons in JavaScript template literals to ensure complete accessibility.

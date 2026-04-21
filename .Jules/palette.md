## 2026-04-21 - Accessibility for Dynamically Generated Icon-Only Buttons
**Learning:** Dynamically generated icon-only buttons in template strings require explicit `aria-label` and `title` attributes. Without them, screen readers cannot interpret the button's purpose, and sighted users lack hover tooltips to understand what the icons represent.
**Action:** Always add `aria-label` (for screen readers) and `title` (for hover tooltips) to icon-only buttons, even when they are generated dynamically within JavaScript template literals.

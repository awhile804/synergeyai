## 2024-05-24 - [Add ARIA labels to icon-only buttons]
**Learning:** Icon-only buttons (like "×", "✓", "✎", "✗"), both static and dynamically generated via JavaScript template strings, often lack accessible names, making them difficult for screen reader users to understand and missing visual hover tooltips for sighted users.
**Action:** Ensure all icon-only buttons include both `aria-label` (for screen readers) and `title` (for visual hover tooltips) attributes to improve overall accessibility and usability.

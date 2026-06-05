## 2024-06-05 - Dual Accessibility for Icon-Only Buttons
**Learning:** Dynamically generated icon-only action buttons (e.g., in `transcript-analyzer.html`) need both `aria-label` (for screen reader announcements) and `title` (for native visual hover tooltips) to ensure the interface is accessible and usable for all users.
**Action:** When adding or auditing icon-only buttons created via template strings, consistently verify and apply both `aria-label` and `title` attributes.

## 2024-05-18 - Add ARIA Labels to Remove Row Buttons
**Learning:** Found dynamic row deletion buttons using `×` without an accessible name or tooltip.
**Action:** Always verify icon-only buttons in template literal structures include `aria-label` and `title` to ensure they're accessible to screen readers and mouse users.

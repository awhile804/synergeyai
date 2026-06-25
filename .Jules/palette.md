## 2024-05-15 - Missing ARIA Labels on Icon-Only Buttons
**Learning:** Dynamically generated UI buttons (like action icons in tables or suggestions) often lack accessibility attributes since they are built via JavaScript template literals and can easily be overlooked.
**Action:** Always verify that icon-only buttons created dynamically have `aria-label` and `title` attributes injected in the template strings to ensure screen reader compatibility and proper visual hover tooltips.

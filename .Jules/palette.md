## 2026-06-22 - Accessible Icon-only Action Buttons
**Learning:** Dynamically generated UI elements created via JavaScript template strings containing icon-only buttons lack inherent context for screen readers and lack visual tooltips for users.
**Action:** explicitly include both aria-label and title attributes on dynamically generated icon-only action buttons to ensure screen reader compatibility and clear visual hover states.

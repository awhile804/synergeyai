
## 2024-05-17 - Icon-only buttons need labels
**Learning:** Dynamically generated icon-only action buttons (e.g., approve/reject/edit) must have both `aria-label` for screen readers and `title` for visual hover tooltips to be fully accessible.
**Action:** Always add matching `aria-label` and `title` attributes when creating icon-only buttons in JavaScript template literals.

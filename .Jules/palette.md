## 2026-06-15 - Dynamic Element Accessibility
**Learning:** Icon-only buttons rendered via inline JavaScript template literals frequently lack accessibility attributes. Because they aren't static in the DOM, they are easy to miss during visual audits and traditional linting.
**Action:** When creating or editing dynamic UI rendering functions (e.g., renderCard, addRow), always include `aria-label` and `title` on any icon-based action buttons to ensure screen reader support and hover tooltips.

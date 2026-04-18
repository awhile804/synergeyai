## 2026-04-18 - Dynamic Icon-Only Buttons Accessibility
**Learning:** Icon-only buttons (like remove '×' or approve '✓') frequently miss `aria-label` attributes when dynamically generated via JS template literals.
**Action:** Always verify dynamically injected HTML strings for proper accessibility attributes on interactive elements.

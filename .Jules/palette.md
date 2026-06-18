## 2026-06-18 - ARIA labels on dynamic icon-only buttons
**Learning:** Dynamically generated UI elements created via JavaScript template strings (like suggestion actions) often miss accessibility attributes because they skip standard static HTML linting. Icon-only buttons must always include both aria-label for screen readers and title for visual hover tooltips.
**Action:** Always verify inline JS template literals for icon-only action buttons and explicitly inject aria-label and title attributes.

## 2026-05-25 - Icon-Only Button Accessibility in Dynamic JS Templates
**Learning:** Dynamically generated UI elements created via JavaScript template strings (e.g., suggestion actions in `transcript-analyzer.html`) often miss accessibility attributes because they fall outside traditional HTML linting. Screen readers cannot interpret plain icon characters like '✓' or '✎'.
**Action:** Always explicitly include both `aria-label` for screen readers and `title` for visual hover tooltips when generating icon-only action buttons dynamically.

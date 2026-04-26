## 2024-05-14 - ARIA and Title Labels for Dynamic Action Buttons
**Learning:** Dynamically generated UI elements created via JavaScript template strings (e.g., action buttons in `transcript-analyzer.html`) must explicitly include both `aria-label` and `title` attributes for icon-only action buttons. This ensures screen reader compatibility and visual hover tooltips.
**Action:** When creating or modifying template literal functions like `renderSuggestionCard()` that generate icon-only buttons, always add both `aria-label` and `title` properties immediately.

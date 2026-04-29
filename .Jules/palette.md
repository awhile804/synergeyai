## 2024-06-25 - ARIA Labels on Dynamically Generated Template Literal UI

**Learning:** When using JavaScript template literals to dynamically render complex DOM structures (like the `renderSuggestionCard` in `transcript-analyzer.html` or form rows in `project-builder.html`), icon-only buttons (`×`, `✓`, `✎`, `✗`) are completely inaccessible to screen readers and lack visual context on hover unless explicitly annotated.

**Action:** Always include both `aria-label` (for screen readers) and `title` (for visual hover tooltips) on all icon-only buttons, whether they are hardcoded in the initial HTML or injected later via JavaScript. This pattern ensures full accessibility compliance and improves usability for all users interacting with generated content.

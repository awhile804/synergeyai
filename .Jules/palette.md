## 2024-03-24 - Dynamic UI Elements and Accessibility Attributes
**Learning:** Dynamically generated UI elements created via JavaScript template strings (like action buttons in suggestion cards or dynamically added table rows) often miss critical accessibility attributes (ARIA labels, titles) because they aren't part of the initial HTML scan.
**Action:** Always ensure that icon-only buttons injected dynamically include both `aria-label` for screen readers and `title` for hover tooltips to maintain accessibility and discoverability.

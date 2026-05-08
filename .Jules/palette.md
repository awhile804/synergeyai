
## 2024-05-08 - Accessible Dynamic Action Icons
**Learning:** When generating suggestion action buttons (approve, edit, reject) dynamically via template strings, icon-only buttons (`✓`, `✎`, `✗`) create a significant usability gap. Screen readers announce nothing meaningful, and visual users lose context on hover.
**Action:** Always include both `aria-label` (for screen readers) and `title` (for native visual tooltips) on all dynamically injected icon-only buttons within template literals.

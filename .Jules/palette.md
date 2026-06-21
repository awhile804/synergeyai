
## 2024-05-19 - Add ARIA expanded and controls to interactive regions
**Learning:** Expandable table rows or accordions must include the `aria-expanded` attribute on the toggle button, dynamically updated via JavaScript based on their state, and use `aria-controls` linked to the expanded content's ID to ensure proper screen reader compatibility.
**Action:** Always add proper ARIA states (`aria-expanded` and `aria-controls`) and keyboard interaction handlers (`role="button"`, `tabindex="0"`, `onkeydown` for enter/space) to custom expandable UI components.

## 2026-05-30 - Added aria-expanded to Details toggle button
**Learning:** When building expandable table rows or accordions, setting `aria-expanded` on the toggle button and linking it via `aria-controls` to the expanded content's ID ensures screen readers understand the relationship and the current state of the content.
**Action:** Ensure all dynamically expanding UI elements have `aria-expanded` updated via JavaScript based on their state, and establish connection using `aria-controls`.

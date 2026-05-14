## 2026-05-14 - Dynamic aria-expanded for Toggle Buttons
**Learning:** Toggle buttons that expand or collapse sections must implement both `aria-expanded` indicating the current state, and `aria-controls` pointing to the expanded element's ID, to be fully accessible. The `aria-expanded` state must be updated dynamically via JS.
**Action:** When creating expanding/collapsing list rows or accordions, ensure corresponding JS toggles the `aria-expanded` attribute.

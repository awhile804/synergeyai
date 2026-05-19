## 2026-05-19 - ARIA toggle attributes on nested buttons
**Learning:** Avoid adding `role="button"` to wrapper elements if they contain native `<button>` elements inside them (violates WCAG). Place ARIA attributes (`aria-expanded`, `aria-controls`) and an `onclick` with `event.stopPropagation()` on the dedicated inner button for screen reader/keyboard accessibility, while safely keeping a plain `onclick` on the wrapper to maintain a large click target for pointer users.
**Action:** Adding ARIA toggles to native button with `stopPropagation()` inside a clickable wrapper element.

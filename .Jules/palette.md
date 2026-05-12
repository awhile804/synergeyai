## 2024-05-12 - Aria Expanded Pattern on Toggle Elements
**Learning:** Avoid adding `role="button"` to wrapper elements (like `div` headers) that contain nested native interactive elements, as it violates WCAG and creates confusing behavior for screen readers.
**Action:** Always delegate ARIA attributes (`aria-expanded`, `aria-controls`) and event handlers with `event.stopPropagation()` to dedicated inner button elements to maintain robust accessibility without compromising the large click targets for pointer users.

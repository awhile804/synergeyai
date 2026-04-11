## 2024-05-24 - Expander Buttons ARIA States

**Learning:** When using toggle buttons to expand or collapse nested content blocks (such as row details in tables or task cards), visually relying on `.show` or `.expanded` CSS classes is insufficient for accessibility. The interactive components (`<button>`) need an explicit structural relationship with the content they control to support screen readers, especially when click events are also bound to larger visual wrappers (like card headers) for pointer users.

**Action:** Consistently enforce the pattern of defining `aria-controls="[target-id]"` and dynamically toggling `aria-expanded="true/false"` directly on the dedicated interactive `<button>` elements in template strings and their corresponding toggle functions. When the wrapper has an `onclick` event, ensure the inner button's `onclick` uses `event.stopPropagation()` so its focus and click behavior remain independent and semantically correct for keyboard users.

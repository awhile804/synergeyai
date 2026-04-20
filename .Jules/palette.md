## 2024-04-20 - Accessible Dropdown Toggles in Wrapper Elements
**Learning:** Adding `role="button"` to wrapper elements containing native `<button>`s violates WCAG guidelines.
**Action:** Place `aria-expanded` and `aria-controls` directly on the inner `<button>` with an `onclick="event.stopPropagation();"` handler to preserve screen reader accessibility, while allowing a plain `onclick` on the wrapper to keep the larger click target for pointer users.

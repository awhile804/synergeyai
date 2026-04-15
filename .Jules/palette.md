
## 2024-05-24 - Accessibility for Task Toggles
**Learning:** When dealing with clickable wrapper elements containing dedicated inner expand/collapse buttons (like `.detail-task-header` and `.detail-task-expand`), ARIA attributes (`aria-expanded`, `aria-controls`, `aria-label`) should be placed on the specific inner button rather than the wrapper element to comply with WCAG. It is also important to use `event.stopPropagation()` on the inner button's `onclick` to prevent triggering redundant events from the wrapper.
**Action:** Always ensure ARIA toggle state attributes are bound to specific `button` elements instead of generic `div` wrappers, even if the wrapper handles the generic click. Dynamically update `aria-expanded` via JavaScript when toggling.

## 2024-05-01 - Nested Toggle Buttons
**Learning:** Wrapper elements (like div headers) shouldn't be used as buttons if they contain native <button> elements inside them (violates WCAG). Instead, we must place ARIA attributes (aria-expanded, aria-controls) and an onclick with event.stopPropagation() on the inner button.
**Action:** When adding toggle buttons within clickable rows, ensure the specific button has aria-expanded, aria-controls, and stopPropagation() so the screen reader interprets the button correctly and clicking it doesn't trigger the wrapper's generic click.

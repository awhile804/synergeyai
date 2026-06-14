## 2024-06-14 - [Aria-Expanded attributes on accordions/details rows]
**Learning:** For dynamic content like table rows expanding or accordions expanding, screen reader compatibility requires the aria-expanded attribute on the toggle button itself and the aria-controls attribute to link it to the expanded content's ID.
**Action:** Always verify that expand/collapse toggle buttons update their aria-expanded state dynamically in the corresponding toggle javascript functions.

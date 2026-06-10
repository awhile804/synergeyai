## 2024-05-24 - Dynamically Generated Icon Buttons Accessibility
**Learning:** Icon-only action buttons generated via JavaScript template strings (e.g., table rows, suggestion actions) often miss critical accessibility attributes, making them inaccessible to screen readers and lacking visual hover context for sighted users.
**Action:** When adding `aria-label` to dynamically generated icon-only buttons for screen readers, simultaneously add a matching `title` attribute to provide a native hover tooltip for visual users.

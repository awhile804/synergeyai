## 2024-04-16 - Initial Entry
## 2024-04-16 - Add ARIA label and title to remove row buttons
**Learning:** Icon-only buttons used for repeating UI actions (like removing a dynamically added row) must have both `aria-label` for screen readers and `title` for sighted users (tooltips).
**Action:** Always add `aria-label` and `title` to icon-only buttons, specifically in dynamically generated JavaScript template literals where they are often missed.

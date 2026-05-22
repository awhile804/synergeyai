## 2024-05-24 - Added ARIA labels to dynamically generated suggestion buttons
**Learning:** When using dynamic JavaScript template strings to generate action UI (like the suggestion buttons in transcript-analyzer.html), it is essential to embed both `aria-label` and `title` attributes simultaneously to guarantee accessibility and visual tooltips, otherwise screen readers receive zero context from icon-only text.
**Action:** Always include both `aria-label` and `title` on button generation logic as standard procedure in this repository's dynamic views.

## 2024-05-14 - Dynamically Generated Icon-Only Buttons
**Learning:** Icon-only action buttons (Approve, Edit, Reject) rendered dynamically via JavaScript template literals in dashboards like `transcript-analyzer.html` often lack accessibility attributes, making them inaccessible to screen readers and lacking visual tooltips for pointer users.
**Action:** Consistently add both `aria-label` and `title` attributes to all icon-only buttons injected via JS template literals to ensure robust accessibility and UX.

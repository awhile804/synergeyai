## 2023-11-09 - Accessible Icon-only Action Buttons
**Learning:** Icon-only action buttons (like ✓, ✎, ✗, ×) require explicit `aria-label` attributes for screen readers and `title` attributes for sighted users to understand their purpose, especially when dynamically generated in template strings where they might be missed by static analysis tools.
**Action:** When adding or updating dynamically generated lists or tables with inline action buttons, explicitly add both `aria-label` and `title` attributes to ensure they are accessible to all users.

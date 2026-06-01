## 2024-06-01 - Missing ARIA Labels on Dynamically Generated Icon-Only Buttons
**Learning:** Icon-only buttons dynamically generated via JavaScript string templates (e.g., in `project-builder.html` and `transcript-analyzer.html`) often lack accessibility attributes like `aria-label` and `title`. Screen readers cannot interpret these buttons without text context.
**Action:** When auditing or implementing dynamic UI generation, ensure that any icon-only button injected via JS includes explicit `aria-label` (for screen readers) and `title` (for visual hover tooltips) attributes.

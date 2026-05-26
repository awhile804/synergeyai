## 2026-05-26 - Adding accessibility tags to icon-only buttons in transcript-analyzer.html
**Learning:** Icon-only action buttons (✓, ✎, ✗) within JavaScript template literals in dynamic UI lists are easy to miss during static accessibility checks, but are critical for screen reader users and those needing tooltips to understand context.
**Action:** When working on dynamic content rendering using JavaScript strings, explicitly check for and add `aria-label` and `title` to all icon-only buttons as part of the implementation pattern.

## 2024-05-24 - Dynamic Template String Accessibility
**Learning:** Icon-only action buttons generated within JavaScript template literals often miss accessibility attributes because they bypass static HTML linting. Without `aria-label` and `title`, screen readers cannot announce their purpose, and users lose hover tooltips.
**Action:** When dynamically rendering interactive UI elements, explicitly inject both `aria-label` (for screen readers) and `title` (for visual hover) alongside the icon.

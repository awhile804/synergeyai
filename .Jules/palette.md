## 2024-03-21 - [Forms Accessibility]
**Learning:** Forms across the application follow a `<div class="form-group">` structure where `<label>` elements must explicitly include a `for` attribute matching the associated input's `id` to ensure screen reader and keyboard accessibility. Currently they lack this.
**Action:** Add `for` attributes to all labels referencing the id of their input.

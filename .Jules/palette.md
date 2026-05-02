## 2026-05-02 - Dynamic Password Visibility Toggles
**Learning:** Hardcoded 'Show' text on password toggles creates a confusing UX when the password is inadvertently left visible, leading to privacy concerns. Resetting state when reopening modals is crucial for a consistent experience.
**Action:** Always implement dynamic 'Show'/'Hide' text based on input state by passing 'this' to the onclick handler, and ensure state is reset when the modal is reopened.

## 2026-07-12 - Secure Token Visibility Pattern
**Learning:** Password/token inputs within modals require visibility toggles to reset their state upon modal reopen to maintain user privacy.
**Action:** Always implement 'Show/Hide' toggle buttons with `type="button"` passing `this` to inline handlers, and ensure modal initialization logic explicitly reverts inputs to `type="password"`.

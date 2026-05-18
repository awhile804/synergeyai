## 2026-05-18 - Reset Sensitive Input Visibility State
**Learning:** When modals containing sensitive inputs (like API keys or tokens) with visibility toggles ('Show' / 'Hide') are reopened, maintaining the previous visibility state can lead to unintended privacy exposure. Users expect modals to reopen in a secure, default state.
**Action:** Always explicitly reset password/token inputs to `type="password"` and reset the corresponding toggle button text to 'Show' in the modal initialization/open functions, regardless of the state they were left in when previously closed.

## 2024-05-18 - Password toggle state feedback
**Learning:** Adding dynamic text feedback ("Show"/"Hide") to password visibility toggle buttons is a low-effort, high-impact UX win that provides clear system status confirmation.
**Action:** When implementing password toggles, ensure the button text updates to reflect the action the user can take (e.g., "Hide" when the password is visible). Pass the button context (`this`) directly in the `onclick` handler to easily update its text without additional DOM queries.

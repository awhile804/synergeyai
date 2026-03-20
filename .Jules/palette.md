## 2024-05-18 - Resetting UI State in Modals
**Learning:** In architectures where modals are hidden via CSS display toggling rather than DOM removal, the state of the modal elements (e.g. disabled buttons, loading text) must be explicitly reset. If the user closes and reopens a modal, the stale state from a previous action will persist unless reverted.
**Action:** When implementing loading states or temporary visual changes in modals, always use a `finally` block (or equivalent cleanup logic) to revert the element to its original state so that it is fresh the next time the modal is displayed.

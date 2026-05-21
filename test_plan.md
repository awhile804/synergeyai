1. **Update toggle buttons in `index.html`**
   - Modify the `onclick` attribute of the 'Show' buttons for GitHub and OpenAI keys to pass `this` and add `type="button"`.
   - Update `toggleGitHubTokenVisibility(btn)` and `toggleOpenAIKeyVisibility(btn)` functions to change the text of the button between 'Show' and 'Hide'.
   - Update `openProjectSettingsModal()` to reset the input types to 'password' and button texts to 'Show' when opening the modal.
2. **Document UX Learning**
   - Create/Update `.Jules/palette.md` to document the learning about resetting state and dynamic button text for password toggles.
3. **Pre-commit checks**
   - Run verification scripts like `python verify.py` to ensure all tests are green.
   - Run `frontend_verification_instructions` and create a playwright script for visual verification of the settings modal toggles, capture screenshots, and use `frontend_verification_complete`.
4. **Submit PR**
   - Submit the changes using the commit message format `🎨 Palette: [UX improvement]`.

from pages.base_page import BasePage

# ─────────────────────────────────────────────────────────
# LoginPage — Authentication
#
# Python equivalent of LoginPage.js
# Same selectors, same logic, different syntax.
# ─────────────────────────────────────────────────────────

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.username_field = page.get_by_placeholder("Username")
        self.password_field = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator(".oxd-alert-content-text")

    def goto(self):
        super().goto("/web/index.php/auth/login")

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
        self.page.wait_for_url("**/dashboard/**", timeout=30000)

    def login_with_credentials(self, credentials):
        self.login(credentials["username"], credentials["password"])

    def login_expecting_failure(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()

    def get_error_message(self):
        self.error_message.wait_for(state="visible", timeout=5000)
        return self.error_message.inner_text()

    def verify_login_successful(self):
        self.page.wait_for_url("**/dashboard/**", timeout=30000)
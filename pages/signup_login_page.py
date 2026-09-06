from pages.base_page import BasePage


class SignupLoginPage(BasePage):
    NEW_USER_HEADING = "text=New User Signup!"
    LOGIN_HEADING = "text=Login to your account"
    SIGNUP_NAME = "input[data-qa='signup-name']"
    SIGNUP_EMAIL = "input[data-qa='signup-email']"
    SIGNUP_BUTTON = "button[data-qa='signup-button']"
    LOGIN_EMAIL = "input[data-qa='login-email']"
    LOGIN_PASSWORD = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGIN_ERROR = "text=Your email or password is incorrect!"
    SIGNUP_ERROR = "text=Email Address already exist!"

    def is_new_user_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.NEW_USER_HEADING))

    def is_login_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.LOGIN_HEADING))

    def sign_up(self, name: str, email: str):
        self.fill(self.page.locator(self.SIGNUP_NAME), name)
        self.fill(self.page.locator(self.SIGNUP_EMAIL), email)
        self.click(self.page.locator(self.SIGNUP_BUTTON))

    def login(self, email: str, password: str):
        self.fill(self.page.locator(self.LOGIN_EMAIL), email)
        self.fill(self.page.locator(self.LOGIN_PASSWORD), password)
        self.click(self.page.locator(self.LOGIN_BUTTON))

    def is_login_error_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.LOGIN_ERROR))

    def is_signup_error_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.SIGNUP_ERROR))

from pages.base_page import BasePage


class HomePage(BasePage):
    LOGO = "img[alt='Website for automation practice']"
    NAV_SIGNUP_LOGIN = "a[href='/login']"
    NAV_PRODUCTS = "a[href='/products']"
    NAV_TEST_CASES = "a[href='/test_cases']"
    NAV_CONTACT_US = "a[href='/contact_us']"
    NAV_LOGOUT = "a[href='/logout']"
    NAV_DELETE_ACCOUNT = "a[href='/delete_account']"
    LOGGED_IN_AS = "a:has-text('Logged in as')"
    SUBSCRIBE_HEADING = "text=SUBSCRIPTION"
    SUBSCRIBE_EMAIL_INPUT = "#susbscribe_email"
    SUBSCRIBE_BUTTON = "#subscribe"
    SUBSCRIBE_SUCCESS = "#success-subscribe .alert-success"

    def open(self):
        self.goto("/")

    def is_home_page_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.LOGO))

    def open_signup_login(self):
        self.click(self.page.locator(self.NAV_SIGNUP_LOGIN))
        self.wait_for_url_contains("/login")

    def open_products(self):
        self.click(self.page.locator(self.NAV_PRODUCTS))
        self.wait_for_url_contains("/products")

    def open_test_cases(self):
        self.click(self.page.locator(self.NAV_TEST_CASES))
        self.wait_for_url_contains("/test_cases")

    def open_contact_us(self):
        self.click(self.page.locator(self.NAV_CONTACT_US))
        self.wait_for_url_contains("/contact_us")

    def logout(self):
        self.click(self.page.locator(self.NAV_LOGOUT))

    def delete_account(self):
        self.click(self.page.locator(self.NAV_DELETE_ACCOUNT))

    def is_logged_in_as_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.LOGGED_IN_AS))

    def scroll_to_footer(self):
        self.scroll_to_bottom()

    def subscribe(self, email: str):
        self.fill(self.page.locator(self.SUBSCRIBE_EMAIL_INPUT), email)
        self.click(self.page.locator(self.SUBSCRIBE_BUTTON))

    def is_subscribe_success_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.SUBSCRIBE_SUCCESS))

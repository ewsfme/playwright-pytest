from pages.base_page import BasePage


class SignupPage(BasePage):
    ACCOUNT_INFO_HEADING = "text=Enter Account Information"
    GENDER_MR = "#id_gender1"
    PASSWORD = "#password"
    DAYS = "#days"
    MONTHS = "#months"
    YEARS = "#years"
    NEWSLETTER = "#newsletter"
    OPTIN = "#optin"
    FIRST_NAME = "#first_name"
    LAST_NAME = "#last_name"
    COMPANY = "#company"
    ADDRESS1 = "#address1"
    ADDRESS2 = "#address2"
    COUNTRY = "#country"
    STATE = "#state"
    CITY = "#city"
    ZIPCODE = "#zipcode"
    MOBILE_NUMBER = "#mobile_number"
    CREATE_ACCOUNT_BUTTON = "button[data-qa='create-account']"

    def is_account_info_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.ACCOUNT_INFO_HEADING))

    def fill_account_information(self, data: dict):
        self.click(self.page.locator(self.GENDER_MR))
        self.fill(self.page.locator(self.PASSWORD), data["password"])
        self.page.locator(self.DAYS).select_option(data["dob_day"])
        self.page.locator(self.MONTHS).select_option(data["dob_month"])
        self.page.locator(self.YEARS).select_option(data["dob_year"])
        self.click(self.page.locator(self.NEWSLETTER))
        self.click(self.page.locator(self.OPTIN))
        self.fill(self.page.locator(self.FIRST_NAME), data["first_name"])
        self.fill(self.page.locator(self.LAST_NAME), data["last_name"])
        self.fill(self.page.locator(self.COMPANY), data["company"])
        self.fill(self.page.locator(self.ADDRESS1), data["address1"])
        self.fill(self.page.locator(self.ADDRESS2), data["address2"])
        self.page.locator(self.COUNTRY).select_option(data["country"])
        self.fill(self.page.locator(self.STATE), data["state"])
        self.fill(self.page.locator(self.CITY), data["city"])
        self.fill(self.page.locator(self.ZIPCODE), data["zipcode"])
        self.fill(self.page.locator(self.MOBILE_NUMBER), data["mobile_number"])

    def submit(self):
        self.click(self.page.locator(self.CREATE_ACCOUNT_BUTTON))

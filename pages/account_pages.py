from pages.base_page import BasePage


class AccountCreatedPage(BasePage):
    HEADING = "[data-qa='account-created']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"

    def is_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.HEADING))

    def click_continue(self):
        self.click(self.page.locator(self.CONTINUE_BUTTON))


class AccountDeletedPage(BasePage):
    HEADING = "[data-qa='account-deleted']"
    CONTINUE_BUTTON = "[data-qa='continue-button']"

    def is_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.HEADING))

    def click_continue(self):
        self.click(self.page.locator(self.CONTINUE_BUTTON))

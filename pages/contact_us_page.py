from pages.base_page import BasePage


class ContactUsPage(BasePage):
    HEADING = "text=GET IN TOUCH"
    NAME = "input[data-qa='name']"
    EMAIL = "input[data-qa='email']"
    SUBJECT = "input[data-qa='subject']"
    MESSAGE = "textarea[data-qa='message']"
    UPLOAD_FILE = "input[name='upload_file']"
    SUBMIT_BUTTON = "input[data-qa='submit-button']"
    SUCCESS_MESSAGE = ".status.alert-success"
    HOME_BUTTON = "a:has-text('Home')"

    def is_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.HEADING))

    def fill_form(self, name: str, email: str, subject: str, message: str):
        self.fill(self.page.locator(self.NAME), name)
        self.fill(self.page.locator(self.EMAIL), email)
        self.fill(self.page.locator(self.SUBJECT), subject)
        self.fill(self.page.locator(self.MESSAGE), message)

    def upload_file(self, file_path: str):
        self.page.locator(self.UPLOAD_FILE).set_input_files(file_path)

    def submit(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.click(self.page.locator(self.SUBMIT_BUTTON))

    def is_success_message_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.SUCCESS_MESSAGE))

    def go_home(self):
        self.click(self.page.locator(self.HOME_BUTTON).first)

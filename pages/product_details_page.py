from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    PRODUCT_NAME = ".product-information h2"
    CATEGORY = "text=Category:"
    AVAILABILITY = "text=Availability:"
    CONDITION = "text=Condition:"
    BRAND = "text=Brand:"

    def is_details_visible(self) -> bool:
        return (
            self.is_visible(self.page.locator(self.PRODUCT_NAME))
            and self.is_visible(self.page.locator(self.CATEGORY))
            and self.is_visible(self.page.locator(self.AVAILABILITY))
            and self.is_visible(self.page.locator(self.CONDITION))
            and self.is_visible(self.page.locator(self.BRAND))
        )

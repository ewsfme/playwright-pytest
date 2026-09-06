from pages.base_page import BasePage


class ProductsPage(BasePage):
    ALL_PRODUCTS_HEADING = "text=ALL PRODUCTS"
    SEARCH_INPUT = "#search_product"
    SEARCH_BUTTON = "#submit_search"
    SEARCHED_PRODUCTS_HEADING = "text=SEARCHED PRODUCTS"
    PRODUCT_ITEMS = ".product-image-wrapper"
    VIEW_PRODUCT_LINKS = "a:has-text('View Product')"

    def is_all_products_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.ALL_PRODUCTS_HEADING))

    def search_product(self, name: str):
        self.fill(self.page.locator(self.SEARCH_INPUT), name)
        self.click(self.page.locator(self.SEARCH_BUTTON))

    def is_searched_products_heading_visible(self) -> bool:
        return self.is_visible(self.page.locator(self.SEARCHED_PRODUCTS_HEADING))

    def searched_products_count(self) -> int:
        # Products render via AJAX after the search click; wait for the
        # first one instead of counting instantly (a race that showed up
        # as flaky "assert False" on slower-rendering browsers).
        self.is_visible(self.page.locator(self.PRODUCT_ITEMS))
        return self.page.locator(self.PRODUCT_ITEMS).count()

    def view_product(self, index: int = 0):
        # Same AJAX-timing concern as above: make sure items are on the
        # page before trying to click into one of them.
        self.is_visible(self.page.locator(self.PRODUCT_ITEMS))
        self.click(self.page.locator(self.VIEW_PRODUCT_LINKS).nth(index))
        self.wait_for_url_contains("/product_details")

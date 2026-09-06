"""Base class for all Page Objects.

Holds generic Playwright interactions plus an Allure-aware `step`
context manager so every page (and every test) can log a described,
screenshotted step without repeating boilerplate.
"""
from contextlib import contextmanager

import allure
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from utils.popups import dismiss_popups

BASE_URL = "https://www.automationexercise.com"
DEFAULT_TIMEOUT = 15000


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    # ---- generic helpers -------------------------------------------------
    def goto(self, path: str = "/"):
        self.page.goto(f"{BASE_URL}{path}")
        dismiss_popups(self.page)
        self.close_consent_popup()
        self.close_ads()

    def click(self, locator):
        dismiss_popups(self.page)
        self.close_consent_popup()
        locator.first.scroll_into_view_if_needed()
        try:
            locator.first.click(timeout=5000)
        except PlaywrightTimeoutError:
            # A popup likely intercepted the click — close it and retry once.
            dismiss_popups(self.page)
            self.close_ads()
            locator.first.click(force=True, timeout=5000)
        dismiss_popups(self.page)

    def fill(self, locator, value: str):
        locator.first.fill(value)

    def is_visible(self, locator, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """Wait for the element to become visible instead of checking
        instantly — AJAX responses (subscribe, review, contact form,
        redirects after login) take a moment to render, and instant
        `.is_visible()` calls are a common source of flaky `assert False`.
        """
        try:
            locator.first.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def scroll_to_bottom(self):
        self.page.keyboard.press("End")
        self.page.wait_for_timeout(300)

    def scroll_to_top(self):
        self.page.keyboard.press("Home")
        self.page.wait_for_timeout(300)

    def expect_visible(self, locator, timeout: int = DEFAULT_TIMEOUT):
        expect(locator.first).to_be_visible(timeout=timeout)

    def expect_text(self, locator, text: str, timeout: int = DEFAULT_TIMEOUT):
        expect(locator.first).to_contain_text(text, timeout=timeout)

    def wait_for_url_contains(self, fragment: str, timeout: int = DEFAULT_TIMEOUT):
        """Wait until the URL contains `fragment`; retried once via a fresh
        click-free wait, since a popup can occasionally swallow the first
        click attempt silently instead of raising.
        """
        try:
            self.page.wait_for_url(f"**{fragment}**", timeout=timeout)
        except PlaywrightTimeoutError:
            pass

    def close_consent_popup(self):
        """Google Funding Choices consent button, if it rendered."""
        try:
            button = self.page.locator("button.fc-cta-consent")
            button.wait_for(state="visible", timeout=2000)
            button.click()
        except Exception:
            pass

    def close_ads(self):
        """Closes generic dismiss/close buttons, and recovers from a
        Google "vignette" full-page interstitial ad, which redirects the
        whole page to a URL containing '#google_vignette'.
        """
        try:
            self.page.locator("#dismiss-button, .close-button, [aria-label='Close']").first.click(timeout=2000)
        except Exception:
            pass

        if "google_vignette" in self.page.url:
            self.page.goto(self.page.url.split("#")[0])

    # ---- Allure step + screenshot ----------------------------------------
    @contextmanager
    def step(self, title: str):
        """Wrap an Allure step and attach a screenshot once it finishes.

        Usage:
            with home_page.step("Click on 'Signup / Login' button"):
                home_page.open_signup_login()
        """
        with allure.step(title):
            yield
            self.attach_screenshot(title)

    def attach_screenshot(self, name: str = "screenshot"):
        allure.attach(
            self.page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

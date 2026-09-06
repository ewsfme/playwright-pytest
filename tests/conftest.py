import allure
import pytest

from pages.home_page import HomePage
from pages.signup_login_page import SignupLoginPage
from pages.signup_page import SignupPage
from pages.account_pages import AccountCreatedPage, AccountDeletedPage
from pages.contact_us_page import ContactUsPage
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetailsPage
from utils.popups import block_ads


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
        ),
        "locale": "en-US",
    }


@pytest.fixture(autouse=True)
def _block_ad_requests(context):
    block_ads(context)
    yield


@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def signup_login_page(page):
    return SignupLoginPage(page)


@pytest.fixture
def signup_page(page):
    return SignupPage(page)


@pytest.fixture
def account_created_page(page):
    return AccountCreatedPage(page)


@pytest.fixture
def account_deleted_page(page):
    return AccountDeletedPage(page)


@pytest.fixture
def contact_us_page(page):
    return ContactUsPage(page)


@pytest.fixture
def products_page(page):
    return ProductsPage(page)


@pytest.fixture
def product_details_page(page):
    return ProductDetailsPage(page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot and tag the browser name in Allure for every test,
    and make sure a failure is always accompanied by a final-state screenshot.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        page_fixture = item.funcargs.get("page")
        browser_option = item.config.getoption("--browser")
        browser_name = browser_option[0] if isinstance(browser_option, list) and browser_option else (browser_option or "chromium")
        allure.dynamic.tag(str(browser_name))

        if page_fixture is not None:
            try:
                allure.attach(
                    page_fixture.screenshot(full_page=True),
                    name="final-state" if report.passed else "failure-state",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                pass
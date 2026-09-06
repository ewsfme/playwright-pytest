import allure
import pytest

from utils.data_generator import (
    random_account_data,
    random_contact_message,
    random_email,
    random_name,
    random_password,
)


def _register_new_account(home_page, signup_login_page, signup_page, account_created_page):
    """Shared registration flow used by several test cases."""
    name = random_name()
    email = random_email()
    account_data = random_account_data()

    with home_page.step("Click on 'Signup / Login' button"):
        home_page.open_signup_login()

    with signup_login_page.step("Verify 'New User Signup!' is visible"):
        assert signup_login_page.is_new_user_heading_visible()

    with signup_login_page.step(f"Enter name '{name}' and email '{email}'"):
        signup_login_page.sign_up(name, email)

    with signup_page.step("Verify 'ENTER ACCOUNT INFORMATION' is visible"):
        assert signup_page.is_account_info_heading_visible()

    with signup_page.step("Fill account information details"):
        signup_page.fill_account_information(account_data)
        signup_page.submit()

    with account_created_page.step("Verify that 'ACCOUNT CREATED!' is visible"):
        assert account_created_page.is_heading_visible()
        account_created_page.click_continue()

    return email, account_data["password"]


def _delete_account(home_page, account_deleted_page):
    with home_page.step("Click 'Delete Account' button"):
        home_page.delete_account()

    with account_deleted_page.step("Verify that 'ACCOUNT DELETED!' is visible"):
        assert account_deleted_page.is_heading_visible()
        account_deleted_page.click_continue()


@allure.feature("Account management")
class TestAccountManagement:

    @allure.story("Test Case 1: Register User")
    def test_case_01_register_user(
        self, home_page, signup_login_page, signup_page, account_created_page, account_deleted_page
    ):
        with home_page.step("Navigate to home page"):
            home_page.open()

        with home_page.step("Verify that home page is visible successfully"):
            assert home_page.is_home_page_visible()

        _register_new_account(home_page, signup_login_page, signup_page, account_created_page)

        with home_page.step("Verify that 'Logged in as username' is visible"):
            assert home_page.is_logged_in_as_visible()

        _delete_account(home_page, account_deleted_page)

    @allure.story("Test Case 2: Login User with correct email and password")
    def test_case_02_login_correct_credentials(
        self, home_page, signup_login_page, signup_page, account_created_page, account_deleted_page
    ):
        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        email, password = _register_new_account(home_page, signup_login_page, signup_page, account_created_page)

        with home_page.step("Verify that 'Logged in as username' is visible after registration"):
            assert home_page.is_logged_in_as_visible()

        with home_page.step("Click 'Logout' button"):
            home_page.logout()

        with signup_login_page.step("Verify 'Login to your account' is visible"):
            assert signup_login_page.is_login_heading_visible()

        with signup_login_page.step("Enter correct email address and password"):
            signup_login_page.login(email, password)

        with home_page.step("Verify that 'Logged in as username' is visible"):
            assert home_page.is_logged_in_as_visible()

        _delete_account(home_page, account_deleted_page)

    @allure.story("Test Case 3: Login User with incorrect email and password")
    @pytest.mark.parametrize("email,password", [(random_email(), random_password())])
    def test_case_03_login_incorrect_credentials(self, home_page, signup_login_page, email, password):
        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        with home_page.step("Click on 'Signup / Login' button"):
            home_page.open_signup_login()

        with signup_login_page.step("Verify 'Login to your account' is visible"):
            assert signup_login_page.is_login_heading_visible()

        with signup_login_page.step(f"Enter incorrect email '{email}' and password"):
            signup_login_page.login(email, password)

        with signup_login_page.step("Verify error 'Your email or password is incorrect!' is visible"):
            assert signup_login_page.is_login_error_visible()

    @allure.story("Test Case 4: Logout User")
    def test_case_04_logout_user(
        self, home_page, signup_login_page, signup_page, account_created_page, account_deleted_page
    ):
        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        email, password = _register_new_account(home_page, signup_login_page, signup_page, account_created_page)

        with home_page.step("Click on 'Signup / Login' button"):
            home_page.logout()

        with signup_login_page.step("Verify 'Login to your account' is visible"):
            assert signup_login_page.is_login_heading_visible()

        with signup_login_page.step("Enter correct email address and password"):
            signup_login_page.login(email, password)

        with home_page.step("Verify that 'Logged in as username' is visible"):
            assert home_page.is_logged_in_as_visible()

        with home_page.step("Click 'Logout' button"):
            home_page.logout()

        with signup_login_page.step("Verify that user is navigated to login page"):
            assert signup_login_page.is_login_heading_visible()

    @allure.story("Test Case 5: Register User with existing email")
    def test_case_05_register_existing_email(
        self, home_page, signup_login_page, signup_page, account_created_page, account_deleted_page
    ):
        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        email, password = _register_new_account(home_page, signup_login_page, signup_page, account_created_page)

        with home_page.step("Log out so the email can be re-entered as a guest"):
            home_page.logout()

        with signup_login_page.step("Verify 'New User Signup!' is visible"):
            assert signup_login_page.is_new_user_heading_visible()

        with signup_login_page.step(f"Enter name and already registered email '{email}'"):
            signup_login_page.sign_up(random_name(), email)

        with signup_login_page.step("Verify error 'Email Address already exist!' is visible"):
            assert signup_login_page.is_signup_error_visible()

        with home_page.step("Navigate to home page and log back in to clean up the account"):
            home_page.open()
            home_page.open_signup_login()

        with signup_login_page.step("Log in with the original email and password"):
            signup_login_page.login(email, password)

        with home_page.step("Verify that 'Logged in as username' is visible"):
            assert home_page.is_logged_in_as_visible()

        _delete_account(home_page, account_deleted_page)


@allure.feature("Site navigation")
class TestNavigation:

    @allure.story("Test Case 6: Contact Us Form")
    def test_case_06_contact_us_form(self, home_page, contact_us_page, tmp_path):
        message = random_contact_message()
        upload_file = tmp_path / "attachment.txt"
        upload_file.write_text("Sample attachment for Contact Us form test.")

        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        with home_page.step("Click on 'Contact Us' button"):
            home_page.open_contact_us()

        with contact_us_page.step("Verify 'GET IN TOUCH' is visible"):
            assert contact_us_page.is_heading_visible()

        with contact_us_page.step("Enter name, email, subject and message"):
            contact_us_page.fill_form(**message)

        with contact_us_page.step("Upload file"):
            contact_us_page.upload_file(str(upload_file))

        with contact_us_page.step("Click 'Submit' button and confirm dialog"):
            contact_us_page.submit()

        with contact_us_page.step("Verify success message is visible"):
            assert contact_us_page.is_success_message_visible()

        with contact_us_page.step("Click 'Home' button and verify landed on home page"):
            contact_us_page.go_home()
            assert home_page.is_home_page_visible()

    @allure.story("Test Case 7: Verify Test Cases Page")
    def test_case_07_verify_test_cases_page(self, home_page):
        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        with home_page.step("Click on 'Test Cases' button"):
            home_page.open_test_cases()

        with home_page.step("Verify user is navigated to test cases page successfully"):
            assert "test_cases" in home_page.page.url


@allure.feature("Products")
class TestProducts:

    @allure.story("Test Case 8: Verify All Products and product detail page")
    def test_case_08_all_products_and_detail_page(self, home_page, products_page, product_details_page):
        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        with home_page.step("Click on 'Products' button"):
            home_page.open_products()

        with products_page.step("Verify user is navigated to ALL PRODUCTS page successfully"):
            assert products_page.is_all_products_visible()

        with products_page.step("Click on 'View Product' of first product"):
            products_page.view_product(0)

        with product_details_page.step(
            "Verify product details are visible: name, category, price, availability, condition, brand"
        ):
            assert product_details_page.is_details_visible()

    @allure.story("Test Case 9: Search Product")
    def test_case_09_search_product(self, home_page, products_page):
        search_term = "Dress"

        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        with home_page.step("Click on 'Products' button"):
            home_page.open_products()

        with products_page.step("Verify user is navigated to ALL PRODUCTS page successfully"):
            assert products_page.is_all_products_visible()

        with products_page.step(f"Enter product name '{search_term}' and click search button"):
            products_page.search_product(search_term)

        with products_page.step("Verify 'SEARCHED PRODUCTS' is visible"):
            assert products_page.is_searched_products_heading_visible()

        with products_page.step("Verify all the products related to search are visible"):
            assert products_page.searched_products_count() > 0


@allure.feature("Subscription")
class TestSubscription:

    @allure.story("Test Case 10: Verify Subscription in home page")
    def test_case_10_subscription_home_page(self, home_page):
        email = random_email()

        with home_page.step("Navigate to home page"):
            home_page.open()
            assert home_page.is_home_page_visible()

        with home_page.step("Scroll down to footer"):
            home_page.scroll_to_footer()

        with home_page.step("Verify text 'SUBSCRIPTION' is visible"):
            assert home_page.is_visible(home_page.page.locator(home_page.SUBSCRIBE_HEADING))

        with home_page.step(f"Enter email '{email}' and click arrow button"):
            home_page.subscribe(email)

        with home_page.step("Verify success message 'You have been successfully subscribed!' is visible"):
            assert home_page.is_subscribe_success_visible()

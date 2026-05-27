"""
Login page object for OrangeHRM.
"""

from utils.base_page import BasePage
from data.test_data import OrangeHRMTestData
import logging

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Page object for OrangeHRM login page."""

    # Selectors
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = "[role='alert']"  # More generic alert selector
    FORM_CONTAINER = "div[class*='login']"  # More flexible form selector

    def __init__(self, page):
        """Initialize login page."""
        super().__init__(page)

    def wait_for_page_load(self) -> None:
        """Wait for login page to load."""
        logger.info("Waiting for login page to load")
        self.wait_for_element(self.FORM_CONTAINER)

    def enter_username(self, username: str) -> None:
        """Enter username in login form."""
        logger.info(f"Entering username: {username}")
        self.fill(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        """Enter password in login form."""
        logger.info(f"Entering password")
        self.fill(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        """Click login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Complete login flow."""
        logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        logger.info("Retrieving error message")
        locator = self.page.locator(
            ".oxd-alert-content-text"
        )
        try:
            locator.wait_for(state="visible", timeout=5000)
            return locator.text_content().strip()
        except:
            logger.warning("Error message not found")
            return ""

    def is_error_displayed(self) -> bool:
        error = self.page.locator(".oxd-alert-content-text")

        try:
            error.wait_for(state="visible", timeout=7000)
            return error.is_visible()
        except:
            return False


    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled."""
        logger.info("Checking if login button is enabled")
        return self.is_enabled(self.LOGIN_BUTTON)

    def login_with_valid_credentials(self) -> None:
        """Login with default valid admin credentials."""
        logger.info("Logging in with valid admin credentials")
        self.login(
            OrangeHRMTestData.VALID_ADMIN_USERNAME,
            OrangeHRMTestData.VALID_ADMIN_PASSWORD,
        )

    def login_with_invalid_credentials(self) -> None:
        """Login with invalid credentials."""
        logger.info("Logging in with invalid credentials")
        self.login(OrangeHRMTestData.INVALID_USERNAME, OrangeHRMTestData.INVALID_PASSWORD)

"""
Dashboard page object for OrangeHRM.
"""

from utils.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class DashboardPage(BasePage):
    """Page object for OrangeHRM dashboard."""

    # Selectors
    DASHBOARD_HEADER = "h1"
    USER_PROFILE_AREA = ".oxd-topbar-header-userarea"
    MAIN_NAVIGATION = ".oxd-sidepanel-body"
    USER_DROPDOWN = ".oxd-userdropdown-tab"
    PIM_MENU = "a:has-text('PIM')"
    LEAVE_MENU = "a:has-text('Leave')"
    ADMIN_MENU = "a:has-text('Admin')"
    LOGOUT_OPTION = "a:has-text('Logout')"

    def __init__(self, page):
        """Initialize dashboard page."""
        super().__init__(page)

    def wait_for_dashboard_load(self) -> None:
        """Wait for dashboard to load completely."""
        logger.info("Waiting for dashboard to load")
        self.wait_for_element(self.MAIN_NAVIGATION)

    def is_user_logged_in(self) -> bool:
        """Check if user is logged in by checking profile area."""
        logger.info("Checking if user is logged in")
        return self.is_visible(self.USER_PROFILE_AREA)

    def get_dashboard_title(self) -> str:
        """Get dashboard page title."""
        logger.info("Getting dashboard title")
        return self.get_page_title()

    def is_main_navigation_visible(self) -> bool:
        """Check if main navigation menu is visible."""
        logger.info("Checking if main navigation is visible")
        return self.is_visible(self.MAIN_NAVIGATION)

    def click_pim_menu(self) -> None:
        """Click on PIM menu."""
        logger.info("Clicking PIM menu")
        self.click(self.PIM_MENU)
        self.wait_for_navigation()

    def click_leave_menu(self) -> None:
        """Click on Leave menu."""
        logger.info("Clicking Leave menu")
        self.click(self.LEAVE_MENU)
        self.wait_for_navigation()

    def click_admin_menu(self) -> None:
        """Click on Admin menu."""
        logger.info("Clicking Admin menu")
        self.click(self.ADMIN_MENU)
        self.wait_for_navigation()

    def click_user_profile(self) -> None:
        """Click on user profile dropdown."""
        logger.info("Clicking user profile dropdown")
        self.click(self.USER_DROPDOWN)

    def logout(self) -> None:
        """Logout from dashboard."""
        logger.info("Logging out")
        self.click_user_profile()
        self.wait_for_element(self.LOGOUT_OPTION)
        self.click(self.LOGOUT_OPTION)
        self.wait_for_navigation()

    def navigate_to_pim(self) -> None:
        """Navigate to PIM section."""
        logger.info("Navigating to PIM section")
        self.click_pim_menu()

    def navigate_to_leave(self) -> None:
        """Navigate to Leave section."""
        logger.info("Navigating to Leave section")
        self.click_leave_menu()

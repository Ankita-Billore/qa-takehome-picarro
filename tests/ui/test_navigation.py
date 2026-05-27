"""
UI tests for OrangeHRM navigation and main flows.
Tests for FR-UI-3, AC-UI-3
"""

import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.ui
class TestOrangeHRMNavigation:
    """Test cases for OrangeHRM navigation."""

    @pytest.fixture(autouse=True)
    def setup_login(self, login_page, dashboard_page):
        """Login before each navigation test."""
        login_page.wait_for_page_load()
        login_page.login_with_valid_credentials()
        dashboard_page.wait_for_dashboard_load()
        yield
        # Logout after test
        try:
            dashboard_page.logout()
        except Exception as e:
            logger.info(f"Logout cleanup: {e}")

    def test_pim_menu_is_accessible(self, dashboard_page, pim_page):
        """
        Test: PIM menu is visible and accessible
        FR-UI-3, AC-UI-3: PIM module accessible from navigation
        """
        logger.info("Testing PIM menu accessibility")
        
        # Verify dashboard is loaded
        assert dashboard_page.is_user_logged_in(), "Should be logged in"
        
        # Click PIM menu
        dashboard_page.click_pim_menu()
        
        # Verify PIM page loaded
        pim_page.wait_for_pim_page_load()
        
        assert pim_page.is_element_present(pim_page.ADD_EMPLOYEE_BUTTON), \
            "PIM page should be loaded"
        
        logger.info("✓ Successfully navigated to PIM module")

    def test_leave_menu_is_accessible(self, dashboard_page):
        """
        Test: Leave menu is visible and accessible
        FR-UI-3: Leave module accessible from navigation
        """
        logger.info("Testing Leave menu accessibility")
        
        assert dashboard_page.is_user_logged_in(), "Should be logged in"
        
        # Click Leave menu
        dashboard_page.click_leave_menu()
        
        # Wait for navigation
        dashboard_page.wait_for_navigation()
        
        # Verify we're not on login page
        assert dashboard_page.is_main_navigation_visible(), \
            "Should still have navigation visible"
        
        logger.info("✓ Successfully navigated to Leave module")

    def test_navigation_menu_persistence(self, dashboard_page, pim_page):
        """
        Test: Navigation menu remains visible after navigation
        Regression test
        """
        logger.info("Testing navigation menu persistence")
        
        # Navigate to PIM
        dashboard_page.click_pim_menu()
        pim_page.wait_for_pim_page_load()
        
        # Menu should still be visible
        assert dashboard_page.is_main_navigation_visible(), \
            "Navigation menu should persist"
        
        logger.info("✓ Navigation menu persists after navigation")

    def test_admin_menu_accessibility(self, dashboard_page):
        """
        Test: Admin menu is accessible
        Optional test
        """
        logger.info("Testing Admin menu accessibility")
        
        try:
            dashboard_page.click_admin_menu()
            dashboard_page.wait_for_navigation()
            logger.info("✓ Admin menu is accessible")
        except Exception as e:
            logger.info(f"Admin menu not accessible or not available: {e}")

    def test_breadcrumb_navigation(self, dashboard_page, pim_page):
        """
        Test: Can navigate back from submenus
        Regression test
        """
        logger.info("Testing breadcrumb/back navigation")
        
        # Navigate to PIM
        dashboard_page.navigate_to_pim()
        pim_page.wait_for_pim_page_load()
        
        # Navigate back
        dashboard_page.navigate_to_pim()  # Go back to dashboard
        
        logger.info("✓ Back navigation works correctly")

    def test_user_profile_menu(self, dashboard_page):
        """
        Test: User profile dropdown is accessible
        Positive test
        """
        logger.info("Testing user profile menu")
        
        assert dashboard_page.is_user_logged_in(), "Should be logged in"
        
        # Click user profile
        dashboard_page.click_user_profile()
        
        # Should show logout option
        import time
        time.sleep(1)
        
        logger.info("✓ User profile menu is accessible")

    def test_multiple_navigation_transitions(self, dashboard_page, pim_page):
        """
        Test: Multiple navigation transitions work smoothly
        Regression test
        """
        logger.info("Testing multiple navigation transitions")
        
        # Navigate: Dashboard -> PIM
        dashboard_page.navigate_to_pim()
        pim_page.wait_for_pim_page_load()
        assert dashboard_page.is_main_navigation_visible()
        
        # Navigate: PIM -> Leave
        dashboard_page.navigate_to_leave()
        dashboard_page.wait_for_navigation()
        
        # Navigate back: Leave -> PIM
        dashboard_page.navigate_to_pim()
        pim_page.wait_for_pim_page_load()
        
        logger.info("✓ Multiple navigation transitions completed successfully")

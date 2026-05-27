"""
PIM page object for OrangeHRM.
"""

from utils.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class PIMPage(BasePage):
    """Page object for OrangeHRM PIM section."""

    # Selectors
    ADD_EMPLOYEE_BUTTON = "button:has-text('Add')"
    EMPLOYEE_LIST = ".orangehrm-container"
    SEARCH_INPUT = "input[placeholder='Employee Name']"
    EMPLOYEE_TABLE = ".oxd-table-body"
    EMPLOYEE_LIST_MENU = "a:has-text('Employee List')"

    def __init__(self, page):
        """Initialize PIM page."""
        super().__init__(page)

    def wait_for_pim_page_load(self) -> None:
        """Wait for PIM page to load."""
        logger.info("Waiting for PIM page to load")
        self.wait_for_element(self.ADD_EMPLOYEE_BUTTON)

    def click_add_employee(self) -> None:
        """Click Add Employee button."""
        logger.info("Clicking Add Employee button")
        self.click(self.ADD_EMPLOYEE_BUTTON)
        self.wait_for_navigation()

    def search_employee(self, employee_name: str) -> None:
        """Search employee by name."""
        logger.info(f"Searching for employee: {employee_name}")

        # Wait for page readiness
        self.page.wait_for_load_state("networkidle")

        # OrangeHRM has multiple text inputs;
        # Employee Name is usually first visible input
        search_box = self.page.locator(
            "input[placeholder='Type for hints...']"
        ).first

        search_box.wait_for(timeout=15000)

        search_box.fill(employee_name)

        self.page.keyboard.press("Enter")

        self.page.wait_for_timeout(3000)

        logger.info("✓ Search executed")

    def is_employee_table_visible(self) -> bool:
        """Check if employee table is visible."""
        logger.info("Checking if employee table is visible")
        return self.is_visible(self.EMPLOYEE_TABLE)

    def get_employee_count(self) -> int:
        """Get number of employees in the list."""
        logger.info("Getting employee count from table")
        # Selects all table rows with data
        return self.get_element_count(".oxd-table-row")

    def is_employee_in_list(self, employee_name: str) -> bool:
        logger.info(f"Checking if employee '{employee_name}' is in list")

        try:
            self.page.wait_for_timeout(3000)

            employee = self.page.locator(
                f"text={employee_name}"
            ).first

            return employee.is_visible()

        except Exception as e:
            logger.warning(f"Employee not found: {e}")
            return False
        
    def go_to_employee_list(self):
        """Navigate to Employee List page."""
        logger.info("Navigating to Employee List")

        self.click(self.EMPLOYEE_LIST_MENU)

        # Wait for URL change instead of input
        self.page.wait_for_url(
            "**/pim/viewEmployeeList*",
            timeout=15000
        )

        self.page.wait_for_load_state("networkidle")

        logger.info("✓ Employee List page loaded")

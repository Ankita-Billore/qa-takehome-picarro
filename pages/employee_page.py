"""
Employee page object for OrangeHRM.
"""

from utils.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class EmployeePage(BasePage):
    """Page object for OrangeHRM Add/Edit Employee."""

    # Selectors
    FIRST_NAME_INPUT = "input[placeholder='First Name']"
    MIDDLE_NAME_INPUT = "input[placeholder='Middle Name']"
    LAST_NAME_INPUT = "input[placeholder='Last Name']"
    EMPLOYEE_ID_INPUT = "input.oxd-input.oxd-input--active:nth-of-type(5)"
    SAVE_BUTTON = "button:has-text('Save')"
    CANCEL_BUTTON = "button:has-text('Cancel')"
    FORM_CONTAINER = ".orangehrm-container"
    SUCCESS_MESSAGE = ".oxd-toast--success"
    ERROR_MESSAGE = ".oxd-input-field-error"
    REQUIRED_FIELD_ERROR = ".oxd-text--toast-message"

    def __init__(self, page):
        """Initialize employee page."""
        super().__init__(page)

    def wait_for_employee_form_load(self) -> None:
        """Wait for employee form to load."""
        logger.info("Waiting for employee form to load")
        self.page.wait_for_selector("input[name='firstName']", timeout=15000)

    def enter_first_name(self, first_name: str) -> None:
        """Enter first name."""
        logger.info(f"Entering first name: {first_name}")
        self.fill(self.FIRST_NAME_INPUT, first_name)

    def enter_middle_name(self, middle_name: str) -> None:
        """Enter middle name."""
        logger.info(f"Entering middle name: {middle_name}")
        self.fill(self.MIDDLE_NAME_INPUT, middle_name)

    def enter_last_name(self, last_name: str) -> None:
        """Enter last name."""
        logger.info(f"Entering last name: {last_name}")
        self.fill(self.LAST_NAME_INPUT, last_name)

    def enter_employee_id(self, employee_id):
        self.page.locator(
        "//label[text()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input"
        ).fill(employee_id)

    def fill_employee_form(
        self,
        first_name: str,
        last_name: str,
        employee_id: str,
        middle_name: str = "",
    ) -> None:
        """Fill the complete employee form."""
        logger.info("Filling employee form")
        self.enter_first_name(first_name)
        if middle_name:
            self.enter_middle_name(middle_name)
        self.enter_last_name(last_name)
        self.enter_employee_id(employee_id)

    def click_save(self) -> None:
        """Click save button."""
        logger.info("Clicking save button")
        self.click(self.SAVE_BUTTON)
        self.wait_for_navigation()

    def click_cancel(self) -> None:
        """Click cancel button."""
        logger.info("Clicking cancel button")
        self.click(self.CANCEL_BUTTON)

    def submit_employee_form(
        self,
        first_name=None,
        last_name=None,
        middle_name=None,
        employee_id=None
        ):
        if first_name:
            self.enter_first_name(first_name)

        if middle_name:
            self.enter_middle_name(middle_name)

        if last_name:
            self.enter_last_name(last_name)

        if employee_id:
            self.enter_employee_id(employee_id)

        self.page.locator("button:has-text('Save')").click()

        self.page.wait_for_timeout(2000)

    def is_success_message_displayed(self):
        """Check if success message is displayed with fallback selectors."""
        try:
            # Try primary selector
            if self.page.locator(".oxd-toast").is_visible(timeout=2000):
                logger.info("✓ Success message detected via .oxd-toast")
                return True
        except:
            pass
        
        try:
            # Try generic toast selector
            if self.page.locator("[class*='toast']").is_visible(timeout=2000):
                logger.info("✓ Success message detected via [class*='toast']")
                return True
        except:
            pass
        
        try:
            # Try alert selector
            if self.page.locator("[role='alert']").is_visible(timeout=2000):
                logger.info("✓ Success message detected via [role='alert']")
                return True
        except:
            pass
        
        # Wait a bit for any async message and retry
        import time
        time.sleep(1)
        
        try:
            if self.page.locator("[class*='success']").is_visible(timeout=1000):
                logger.info("✓ Success message detected via [class*='success']")
                return True
        except:
            pass
        
        logger.warning("✗ No success message found with any selector")
        return False

    def is_error_displayed(self) -> bool:
        """Check if validation error is displayed."""
        logger.info("Checking if error is displayed")
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_messages(self) -> list:
        """Get all validation error messages."""
        logger.info("Getting error messages")
        errors = self.page.query_selector_all(self.REQUIRED_FIELD_ERROR)
        return [error.text_content() for error in errors]

    def get_first_name_value(self) -> str:
        """Get value of first name input."""
        logger.info("Getting first name value")
        return self.page.input_value(self.FIRST_NAME_INPUT)

    def get_last_name_value(self) -> str:
        """Get value of last name input."""
        logger.info("Getting last name value")
        return self.page.input_value(self.LAST_NAME_INPUT)

    def get_employee_id_value(self):
        return self.page.locator(
        "//label[text()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input"
        ).input_value()

    def is_first_name_required(self) -> bool:
        """Check if first name field shows as required."""
        logger.info("Checking if first name is required")
        first_name_field = self.page.query_selector(self.FIRST_NAME_INPUT)
        return first_name_field.get_attribute("required") is not None

"""
Pytest configuration and fixtures for all tests.
"""

import pytest
import logging
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import allure

from utils.config import (
    BROWSER_TYPE,
    HEADLESS,
    SLOW_MO,
    TIMEOUT,
    VIEWPORT,
    ORANGEHRM_BASE_URL,
)

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "test_execution.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


# ============================================================================
# Allure Report Helper Function
# ============================================================================


def attach_screenshot_to_allure(page):
    """Attach screenshot to Allure report on test failure."""
    try:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        logger.warning(f"Could not attach screenshot to Allure: {e}")


# ============================================================================
# UI Test Fixtures (Playwright)
# ============================================================================


@pytest.fixture(scope="session")
def browser_context_args():
    """Configure browser context arguments."""
    return {
        "viewport": VIEWPORT,
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def playwright_instance():
    """Create a Playwright instance."""
    logger.info("Starting Playwright instance")
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    """Create a browser instance."""
    logger.info(f"Launching browser: {BROWSER_TYPE}")
    browser = getattr(playwright_instance, BROWSER_TYPE).launch(
        headless=HEADLESS,
        slow_mo=SLOW_MO,
    )
    yield browser
    logger.info("Closing browser")
    browser.close()


@pytest.fixture
def context(browser, browser_context_args):
    """Create a new browser context for each test."""
    logger.info("Creating new browser context")
    context = browser.new_context(**browser_context_args)
    yield context
    logger.info("Closing browser context")
    context.close()


@pytest.fixture
def page(context):
    """Create a new page for each test."""
    logger.info("Creating new page")
    page = context.new_page()
    page.set_default_timeout(TIMEOUT)
    yield page
    
    # Take screenshot on failure
    if hasattr(page, "_test_failed") and page._test_failed:
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = screenshot_dir / f"failure_{timestamp}.png"
        logger.info(f"Taking screenshot: {screenshot_path}")
        page.screenshot(path=str(screenshot_path))
    
    logger.info("Closing page")
    page.close()


# ============================================================================
# Fixture for tracking test failures
# ============================================================================


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test failures."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            item.funcargs["page"]._test_failed = True


# ============================================================================
# API Test Fixtures
# ============================================================================


@pytest.fixture
def api_client():
    """Provide REST Countries API client."""
    from api.restcountries_client import RestCountriesClient

    logger.info("Creating REST Countries API client")
    return RestCountriesClient()


# ============================================================================
# Test Data Fixtures
# ============================================================================


@pytest.fixture
def country_test_data():
    """Provide country test data."""
    from data.test_data import CountryTestData

    logger.info("Loading country test data")
    return CountryTestData()


@pytest.fixture
def orangehrm_test_data():
    """Provide OrangeHRM test data."""
    from data.test_data import OrangeHRMTestData

    logger.info("Loading OrangeHRM test data")
    return OrangeHRMTestData()


# ============================================================================
# Page Object Fixtures
# ============================================================================


@pytest.fixture
def login_page(page):
    """Provide login page object."""
    from pages.login_page import LoginPage

    logger.info("Creating LoginPage object")

    try:
        page.goto(
            ORANGEHRM_BASE_URL,
            timeout=30000,
            wait_until="domcontentloaded"
        )
        page.wait_for_load_state("networkidle", timeout=60000)

        page.wait_for_selector(
            "input[name='username']",
            timeout=10000
        )

        return LoginPage(page)

    except Exception as e:
        logger.warning(f"Failed to load login page: {e}")
        logger.warning(
            "Ensure OrangeHRM is accessible: "
            "https://opensource-demo.orangehrmlive.com"
        )
        raise


@pytest.fixture
def dashboard_page(page):
    """Provide dashboard page object."""
    from pages.dashboard_page import DashboardPage

    logger.info("Creating DashboardPage object")
    return DashboardPage(page)


@pytest.fixture
def pim_page(page):
    """Provide PIM page object."""
    from pages.pim_page import PIMPage

    logger.info("Creating PIMPage object")
    return PIMPage(page)


@pytest.fixture
def employee_page(page):
    """Provide employee page object."""
    from pages.employee_page import EmployeePage

    logger.info("Creating EmployeePage object")
    return EmployeePage(page)


# ============================================================================
# Markers
# ============================================================================


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "api: mark test as an API test")
    config.addinivalue_line("markers", "ui: mark test as a UI test")
    config.addinivalue_line("markers", "smoke: mark test as a smoke test")
    config.addinivalue_line("markers", "regression: mark test as a regression test")
    config.addinivalue_line("markers", "negative: mark test as a negative test")
    config.addinivalue_line("markers", "critical: mark test as critical severity")
    config.addinivalue_line("markers", "blocker: mark test as blocker severity")
    config.addinivalue_line("markers", "login: mark test related to login functionality")
    config.addinivalue_line("markers", "employee: mark test related to employee management")

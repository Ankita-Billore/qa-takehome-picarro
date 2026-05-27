"""
Base page class for common page operations.
"""

from typing import Optional
from playwright.sync_api import Page, expect
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""

    def __init__(self, page: Page):
        """Initialize with Playwright page object."""
        self.page = page

    def goto(self, url: str) -> None:
        """Navigate to URL."""
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def click(self, selector: str, force: bool = False) -> None:
        """Click on element."""
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector, force=force)

    def fill(self, selector: str, text: str) -> None:
        """Fill text in input field."""
        logger.info(f"Filling text in {selector}: {text}")
        self.page.fill(selector, text)

    def type_text(self, selector: str, text: str) -> None:
        """Type text character by character."""
        logger.info(f"Typing text in {selector}: {text}")
        self.page.locator(selector).type(text)

    def get_text(self, selector: str) -> str:
        """Get text content from element."""
        text = self.page.text_content(selector)
        logger.info(f"Retrieved text from {selector}: {text}")
        return text or ""

    def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        is_vis = self.page.is_visible(selector)
        logger.info(f"Element {selector} visible: {is_vis}")
        return is_vis

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        is_en = self.page.is_enabled(selector)
        logger.info(f"Element {selector} enabled: {is_en}")
        return is_en

    def wait_for_element(self, selector: str, timeout: int = 30000) -> None:
        """Wait for element to be visible."""
        logger.info(f"Waiting for element: {selector}")
        self.page.wait_for_selector(selector, timeout=timeout)

    def get_url(self) -> str:
        """Get current URL."""
        url = self.page.url
        logger.info(f"Current URL: {url}")
        return url

    def refresh(self) -> None:
        """Refresh the page."""
        logger.info("Refreshing page")
        self.page.reload()

    def wait_for_navigation(self, timeout: int = 30000) -> None:
        """Wait for page navigation."""
        logger.info("Waiting for navigation")
        self.page.wait_for_load_state("networkidle", timeout=timeout)

    def get_page_title(self) -> str:
        """Get page title."""
        title = self.page.title()
        logger.info(f"Page title: {title}")
        return title

    def take_screenshot(self, path: str) -> None:
        """Take screenshot and save."""
        logger.info(f"Taking screenshot: {path}")
        self.page.screenshot(path=path)

    def is_element_present(self, selector: str) -> bool:
        """Check if element is present in DOM."""
        try:
            self.page.query_selector(selector)
            return True
        except Exception:
            return False

    def get_element_count(self, selector: str) -> int:
        """Get count of elements matching selector."""
        count = len(self.page.query_selector_all(selector))
        logger.info(f"Element count for {selector}: {count}")
        return count

    def scroll_to_element(self, selector: str) -> None:
        """Scroll element into view."""
        logger.info(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def press_key(self, key: str) -> None:
        """Press keyboard key."""
        logger.info(f"Pressing key: {key}")
        self.page.press("body", key)

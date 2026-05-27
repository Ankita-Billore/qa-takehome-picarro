"""
Configuration settings for the QA automation project.
"""

import os
from typing import Optional

# API Configuration
API_BASE_URL = "https://restcountries.com"
API_VERSION = "v3.1"
API_TIMEOUT = 10

# OrangeHRM Configuration
ORANGEHRM_BASE_URL = "https://opensource-demo.orangehrmlive.com"
ORANGEHRM_USERNAME = "Admin"
ORANGEHRM_PASSWORD = "admin123"

# Browser Configuration
BROWSER_TYPE = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", 0))  # milliseconds
TIMEOUT = int(os.getenv("TIMEOUT", 60000))  # milliseconds (increased for slow networks)
VIEWPORT = {"width": 1920, "height": 1080}

# Test Data Configuration
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/test_execution.log"

# Retry Configuration
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 1))


def get_api_url(endpoint: str) -> str:
    """Build full API URL from endpoint."""
    return f"{API_BASE_URL}/{API_VERSION}{endpoint}"


def get_orangehrm_url(path: str = "") -> str:
    """Build full OrangeHRM URL from path."""
    base = ORANGEHRM_BASE_URL.rstrip("/")
    path = path.lstrip("/")
    return f"{base}/{path}" if path else base

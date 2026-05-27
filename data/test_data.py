"""
Test data for API and UI tests.
"""

from typing import Dict, List, Any


class CountryTestData:
    """Test data for REST Countries API."""

    # Valid country names
    VALID_COUNTRY_NAMES = [
        "France",
        "United States",
        "Germany",
        "Japan",
        "India",
    ]

    # Valid country codes
    VALID_COUNTRY_CODES = {
        "US": "cca2",  # alpha2
        "FR": "cca2",
        "USA": "cca3",  # alpha3
        "FRA": "cca3",
        "GB": "cca2",
    }

    # Valid regions
    VALID_REGIONS = [
        "Europe",
        "Americas",
        "Africa",
        "Asia",
        "Oceania",
    ]

    # Valid currencies
    VALID_CURRENCIES = {
        "usd": "United States",
        "eur": "Multiple",
        "gbp": "United Kingdom",
        "jpy": "Japan",
        "inr": "India",
    }

    # Valid languages
    VALID_LANGUAGES = {
        "spanish": "Spain",
        "english": "United Kingdom",
        "french": "France",
        "german": "Germany",
        "japanese": "Japan",
    }

    # Valid capitals
    VALID_CAPITALS = {
        "Paris": "France",
        "Washington": "United States",
        "Berlin": "Germany",
        "Tokyo": "Japan",
        "New Delhi": "India",
    }

    # Invalid test data
    INVALID_COUNTRY_NAME = "XyZaAbBcCdDeEfF"
    INVALID_COUNTRY_CODE = "XX"
    INVALID_REGION = "InvalidRegion"
    INVALID_CURRENCY = "xyz"
    INVALID_LANGUAGE = "klingon"
    INVALID_CAPITAL = "InvalidCapital"

    # Expected response fields for countries
    EXPECTED_COUNTRY_FIELDS = [
        "name",
        "capital",
        "region",
        "subregion",
        "population",
        "area",
        "timezones",
        "continents",
        "currencies",
        "languages",
    ]

    # Fields for /all endpoint request
    ALL_ENDPOINT_FIELDS = ["name", "capital", "currencies", "region"]


class OrangeHRMTestData:
    """Test data for OrangeHRM UI tests."""

    # Valid credentials
    VALID_ADMIN_USERNAME = "Admin"
    VALID_ADMIN_PASSWORD = "admin123"

    # Invalid credentials
    INVALID_USERNAME = "InvalidUser"
    INVALID_PASSWORD = "WrongPassword"

    # Employee data for add employee flow
    NEW_EMPLOYEE_DATA = {
        "firstName": "John",
        "middleName": "Michael",
        "lastName": "Doe",
        "employeeId": "EMP12345",
    }

    EMPLOYEE_DATA_VARIATIONS = [
        {
            "firstName": "Jane",
            "middleName": "Anne",
            "lastName": "Smith",
            "employeeId": "EMP12346",
        },
        {
            "firstName": "Robert",
            "lastName": "Johnson",
            "employeeId": "EMP12347",
        },
    ]

    # UI Selectors/Locators
    LOGIN_PAGE_SELECTORS = {
        "username_input": "input[name='username']",
        "password_input": "input[name='password']",
        "login_button": "button[type='submit']",
        "error_message": ".oxd-alert-content-text",
    }

    DASHBOARD_SELECTORS = {
        "dashboard_header": "h1:has-text('Dashboard')",
        "user_profile": ".oxd-topbar-header-userarea",
        "main_nav": ".oxd-sidepanel-body",
    }

    PIM_SELECTORS = {
        "add_employee_button": "button:has-text('Add')",
        "employee_form": ".orangehrm-container",
        "first_name_input": "input[placeholder='First Name']",
        "middle_name_input": "input[placeholder='Middle Name']",
        "last_name_input": "input[placeholder='Last Name']",
        "employee_id_input": "input[name='employeeId']",
        "save_button": "button:has-text('Save')",
        "success_toast": ".oxd-toast-close-button",
    }


class APIResponseStructure:
    """Expected API response structures."""

    COUNTRY_OBJECT_SCHEMA = {
        "name": {"common": str, "official": str},
        "capital": list,
        "region": str,
        "subregion": str,
        "population": int,
        "area": (int, float),
        "timezones": list,
        "continents": list,
    }

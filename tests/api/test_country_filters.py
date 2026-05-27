"""
API tests for REST Countries - Filter endpoints.
Tests for FR-API-3 through FR-API-9
"""

import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.smoke
class TestCountryByCode:
    """Test cases for GET /v3.1/alpha/{code} endpoint."""

    def test_get_country_by_valid_alpha2_code(self, api_client):
        """
        Test: Get country by valid alpha2 code
        FR-API-3, AC-API-3: Valid code returns 200 and country object
        """
        code = "US"
        
        response = api_client.get_country_by_code(code)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        # Response can be array or object depending on API version
        if isinstance(data, list):
            assert len(data) > 0, "Response array should not be empty"
            country = data[0]
        else:
            country = data
        
        assert "name" in country
        assert "cca2" in country
        
        logger.info(f"✓ Successfully retrieved country with code '{code}'")

    def test_get_country_by_valid_alpha3_code(self, api_client):
        """
        Test: Get country by valid alpha3 code
        FR-API-3: Valid alpha3 code works
        """
        code = "USA"
        
        response = api_client.get_country_by_code(code)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        if isinstance(data, list):
            assert len(data) > 0
            country = data[0]
        else:
            country = data
        
        assert "name" in country
        
        logger.info(f"✓ Successfully retrieved country with code '{code}'")

    def test_get_multiple_countries_by_codes(self, api_client):
        """
        Test: Get multiple countries by codes parameter
        FR-API-3: Multiple codes work
        """
        codes = ["US", "FR", "DE"]
        
        response = api_client.get_countries_by_codes(codes)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3, f"Expected 3 countries, got {len(data)}"
        
        logger.info(f"✓ Successfully retrieved {len(data)} countries by codes")

    def test_invalid_country_code_returns_404(self, api_client, country_test_data):
        """
        Test: Invalid country code returns 404
        FR-API-5, AC-API-5: Invalid code returns 404
        """
        invalid_code = country_test_data.INVALID_COUNTRY_CODE
        
        response = api_client.get_country_by_code(invalid_code)
        
        assert response.status_code == 404, \
            f"Expected 404 for invalid code, got {response.status_code}"
        
        logger.info(f"✓ Invalid country code correctly returns 404")


@pytest.mark.api
class TestAllCountries:
    """Test cases for GET /v3.1/all endpoint."""

    def test_get_all_countries_with_fields(self, api_client):
        """
        Test: Get all countries with fields parameter
        FR-API-4, AC-API-4: All endpoint with fields returns 200
        """
        fields = ["name", "capital", "currencies"]
        
        response = api_client.get_all_countries(fields)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 100, "Should return multiple countries"
        
        # Verify requested fields are present
        for country in data[:5]:  # Check first 5
            assert "name" in country, "name field missing"
        
        logger.info(f"✓ Retrieved {len(data)} countries with specified fields")

    def test_all_countries_without_fields_returns_400(self, api_client):
        """
        Test: Get all countries without fields parameter returns 400
        FR-API-6, AC-API-6: Missing fields parameter returns 400
        """
        import requests
        # Direct call without fields parameter
        response = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        
        assert response.status_code == 400, \
            f"Expected 400 for missing fields, got {response.status_code}"
        
        logger.info("✓ Missing fields parameter correctly returns 400")


@pytest.mark.api
class TestCountryFilters:
    """Test cases for region, currency, and language filters."""

    def test_get_countries_by_region(self, api_client):
        """
        Test: Get countries by region
        FR-API-7, AC-API-7: Region filter returns array of countries
        """
        region = "Europe"
        
        response = api_client.get_countries_by_region(region)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, f"Should find countries in {region}"
        
        # Verify all results are in the specified region
        for country in data:
            assert country.get("region", "").lower() == region.lower(), \
                f"Country region mismatch: {country.get('region')}"
        
        logger.info(f"✓ Found {len(data)} countries in {region}")

    def test_get_countries_by_currency(self, api_client):
        """
        Test: Get countries by currency
        FR-API-8, AC-API-8: Currency filter returns array
        """
        currency = "usd"
        
        response = api_client.get_countries_by_currency(currency)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, f"Should find countries with {currency}"
        
        logger.info(f"✓ Found {len(data)} countries with currency {currency}")

    def test_get_countries_by_language(self, api_client):
        """
        Test: Get countries by language
        FR-API-9, AC-API-9: Language filter returns array
        """
        language = "english"
        
        response = api_client.get_countries_by_language(language)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, f"Should find countries with {language}"
        
        logger.info(f"✓ Found {len(data)} countries with language {language}")

    def test_invalid_region_returns_404(self, api_client, country_test_data):
        """
        Test: Invalid region returns 404
        FR-API-5: Invalid region returns 404
        """
        invalid_region = country_test_data.INVALID_REGION
        
        response = api_client.get_countries_by_region(invalid_region)
        
        assert response.status_code == 404, \
            f"Expected 404 for invalid region, got {response.status_code}"
        
        logger.info("✓ Invalid region correctly returns 404")

    def test_multiple_filters_consistency(self, api_client):
        """
        Test: Data consistency across different endpoints
        Validates that the same country appears in multiple filter results
        """
        # Get United States by name
        response_by_name = api_client.get_country_by_name("United States")
        assert response_by_name.status_code == 200
        country_by_name = response_by_name.json()[0]
        
        # Get by code
        response_by_code = api_client.get_country_by_code("US")
        assert response_by_code.status_code == 200
        country_by_code = response_by_code.json()[0] if isinstance(
            response_by_code.json(), list
        ) else response_by_code.json()
        
        # Both should have same common name
        assert country_by_name["name"]["common"] == country_by_code["name"]["common"], \
            "Country data inconsistency between endpoints"
        
        logger.info("✓ Data consistency verified across endpoints")

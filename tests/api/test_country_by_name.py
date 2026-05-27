"""
API tests for REST Countries - Country by Name endpoint.
Tests for FR-API-1, FR-API-2, AC-API-1, AC-API-2
"""

import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.smoke
class TestCountryByName:
    """Test cases for GET /v3.1/name/{name} endpoint."""

    def test_get_country_by_valid_name(self, api_client, country_test_data):
        """
        Test: Get country by valid name (partial match)
        FR-API-1, AC-API-1: Valid country name returns 200 and JSON array
        """
        country_name = "France"
        
        response = api_client.get_country_by_name(country_name)
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Assert response is JSON array
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, "Response array should not be empty"
        
        # Assert expected fields in response
        country = data[0]
        expected_fields = ["name", "capital", "region", "currencies", "languages"]
        for field in expected_fields:
            assert field in country, f"Field '{field}' not found in response"
        
        # Assert name contains search term
        assert "france" in str(country["name"]).lower(), "Country name should contain search term"
        
        logger.info(f"✓ Successfully retrieved {len(data)} country(ies) for '{country_name}'")

    def test_get_country_by_valid_full_name(self, api_client):
        """
        Test: Get country by exact full name
        FR-API-2, AC-API-2: Full name match returns 200 with exact match
        """
        country_name = "Germany"
        
        response = api_client.get_country_by_name(country_name, full_text=True)
        
        # Assert status code
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Assert response
        data = response.json()
        assert isinstance(data, list), "Response should be an array"
        assert len(data) > 0, "Response should not be empty"
        
        # Verify exact match
        country = data[0]
        assert country["name"]["common"].lower() == country_name.lower(), \
            f"Expected exact match for '{country_name}'"
        
        logger.info(f"✓ Successfully retrieved exact match for '{country_name}'")

    def test_get_country_by_multiple_names(self, api_client, country_test_data):
        """
        Test: Retrieve multiple different countries by name
        FR-API-1: Multiple valid names work correctly
        """
        for country_name in country_test_data.VALID_COUNTRY_NAMES[:3]:
            response = api_client.get_country_by_name(country_name)
            
            assert response.status_code == 200, \
                f"Failed for country '{country_name}': {response.status_code}"
            
            data = response.json()
            assert len(data) > 0, f"No results for '{country_name}'"
            
            logger.info(f"✓ Retrieved data for {country_name}")

    def test_get_country_by_partial_name(self, api_client):
        """
        Test: Partial name matching works
        AC-API-1: Partial match returns results
        """
        partial_name = "United"
        
        response = api_client.get_country_by_name(partial_name)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        assert len(data) >= 1, "Should find at least one country with 'United' in name"
        
        # Verify results contain search term
        for country in data:
            assert "united" in str(country["name"]).lower(), \
                "Results should contain search term"
        
        logger.info(f"✓ Found {len(data)} countries with '{partial_name}' in name")

    def test_response_structure_for_country_by_name(self, api_client, country_test_data):
        """
        Test: Response structure contains all expected fields
        AC-API-1: Response contains name, capital, region fields
        """
        response = api_client.get_country_by_name("Japan")
        data = response.json()
        country = data[0]
        
        # Check key fields exist
        assert "name" in country
        assert isinstance(country["name"], dict)
        assert "common" in country["name"]
        
        assert "capital" in country
        assert isinstance(country["capital"], list)
        
        assert "region" in country
        assert isinstance(country["region"], str)
        
        assert "currencies" in country
        assert isinstance(country["currencies"], dict)
        
        assert "languages" in country
        assert isinstance(country["languages"], dict)
        
        logger.info("✓ Response structure is valid")

    def test_invalid_country_name_returns_404(self, api_client, country_test_data):
        """
        Test: Invalid country name returns 404
        FR-API-5, AC-API-5: Non-existent name returns 404
        """
        invalid_name = country_test_data.INVALID_COUNTRY_NAME
        
        response = api_client.get_country_by_name(invalid_name)
        
        assert response.status_code == 404, \
            f"Expected 404 for invalid country, got {response.status_code}"
        
        logger.info(f"✓ Invalid country name correctly returns 404")

    def test_empty_name_parameter(self, api_client):
        """
        Test: Empty name parameter handling
        Negative test case
        """
        response = api_client.get_country_by_name("")
        
        # API likely returns 404 for empty name
        assert response.status_code in [400, 404, 500], \
            f"Unexpected status code: {response.status_code}"
        
        logger.info("✓ Empty name handled appropriately")

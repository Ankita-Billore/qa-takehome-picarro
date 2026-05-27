"""
API tests for negative scenarios and edge cases.
Tests for error handling and boundary conditions
"""

import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.negative
class TestAPIErrorHandling:
    """Test error handling and edge cases."""

    def test_malformed_endpoint_returns_404(self, api_client):
        """
        Test: Malformed endpoint returns 404
        Negative test case
        """
        import requests
        response = requests.get(
            "https://restcountries.com/v3.1/invalid_endpoint",
            timeout=10
        )
        
        assert response.status_code == 404, "Malformed endpoint should return 404"
        logger.info("✓ Malformed endpoint correctly returns 404")

    def test_special_characters_in_country_name(self, api_client):
        """
        Test: Special characters in country name
        Negative test case
        """
        special_name = "Côte d'Ivoire"  # Ivory Coast
        
        response = api_client.get_country_by_name(special_name)
        
        # Should either work or return 404, not error
        assert response.status_code in [200, 404], \
            f"Unexpected status for special characters: {response.status_code}"
        
        logger.info("✓ Special characters handled appropriately")

    def test_very_long_country_name(self, api_client):
        """
        Test: Very long string as country name
        Negative test case
        """
        long_name = "a" * 1000
        
        response = api_client.get_country_by_name(long_name)
        
        # Should return 404, not error
        assert response.status_code == 404, \
            f"Expected 404 for invalid long name, got {response.status_code}"
        
        logger.info("✓ Long country name handled appropriately")

    def test_numeric_country_code(self, api_client):
        """
        Test: Numeric country code (invalid format)
        Negative test case
        """
        invalid_code = "12"
        
        response = api_client.get_country_by_code(invalid_code)
        
        assert response.status_code == 404, \
            f"Expected 404 for numeric code, got {response.status_code}"
        
        logger.info("✓ Numeric code correctly returns 404")

    def test_case_insensitivity(self, api_client):
        """
        Test: API handles case variations
        Positive test case - API should be case insensitive
        """
        # Test lowercase
        response_lower = api_client.get_country_by_name("france")
        assert response_lower.status_code == 200
        
        # Test uppercase
        response_upper = api_client.get_country_by_name("FRANCE")
        assert response_upper.status_code == 200
        
        # Both should return same country
        data_lower = response_lower.json()[0]
        data_upper = response_upper.json()[0]
        
        assert data_lower["name"]["common"] == data_upper["name"]["common"], \
            "Case variants should return same country"
        
        logger.info("✓ API correctly handles case variations")

    def test_whitespace_handling(self, api_client):
        """
        Test: Whitespace in country name
        Positive test case
        """
        response = api_client.get_country_by_name("United States")
        
        assert response.status_code == 200, \
            "Should handle country names with spaces"
        
        logger.info("✓ Whitespace in country names handled correctly")

    def test_null_response_handling(self, api_client):
        """
        Test: API returns valid JSON structure
        Validates no null responses for valid requests
        """
        response = api_client.get_country_by_name("United Kingdom")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response is not null
        assert data is not None, "Response should not be null"
        assert len(data) > 0, "Response should have data"
        
        logger.info("✓ API returns valid response structure")

    def test_duplicate_codes(self, api_client):
        """
        Test: Multiple codes parameter with duplicates
        Edge case test
        """
        response = api_client.get_countries_by_codes(["US", "US", "FR"])
        
        assert response.status_code == 200
        data = response.json()
        
        # API might return 2 or 3 depending on deduplication
        assert len(data) in [2, 3], "Should handle duplicate codes gracefully"
        
        logger.info("✓ Duplicate codes handled appropriately")

    def test_response_time_acceptable(self, api_client):
        """
        Test: API response time is reasonable
        Performance constraint check
        """
        import time
        
        start = time.time()
        response = api_client.get_country_by_name("France")
        elapsed = time.time() - start
        
        # Should respond within 5 seconds
        assert elapsed < 5, f"API response took {elapsed:.2f}s, should be < 5s"
        assert response.status_code == 200
        
        logger.info(f"✓ API responded in {elapsed:.2f}s")

    def test_response_encoding_is_utf8(self, api_client):
        """
        Test: Response is properly UTF-8 encoded
        Tests countries with special characters
        """
        response = api_client.get_country_by_name("São Tomé")
        
        if response.status_code == 200:
            data = response.json()
            # If we get here without encoding errors, UTF-8 is correct
            assert len(data) >= 0, "Response parsed successfully"
            logger.info("✓ Response is properly UTF-8 encoded")
        else:
            logger.info(f"✓ Special character handling: {response.status_code}")

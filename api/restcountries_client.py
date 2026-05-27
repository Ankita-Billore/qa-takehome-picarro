"""
REST Countries API client.
"""

import requests
import logging
from typing import Optional, List, Dict, Any
from utils.config import get_api_url, API_TIMEOUT

logger = logging.getLogger(__name__)


class RestCountriesClient:
    """Client for REST Countries API v3.1."""

    def __init__(self, base_url: str = "https://restcountries.com/v3.1"):
        """Initialize API client."""
        self.base_url = base_url
        self.timeout = API_TIMEOUT

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Make HTTP request to API."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"{method} {url}")
        if params:
            logger.info(f"Query params: {params}")

        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            timeout=self.timeout,
        )

        logger.info(f"Response status: {response.status_code}")
        return response

    def get_country_by_name(self, name: str, full_text: bool = False) -> requests.Response:
        """
        Get country by name.
        
        Args:
            name: Country name (partial or full)
            full_text: If True, match full name exactly
        
        Returns:
            Response object
        """
        params = None
        if full_text:
            params = {"fullText": "true"}
        
        endpoint = f"/name/{name}"
        return self._make_request("GET", endpoint, params=params)

    def get_country_by_code(self, code: str) -> requests.Response:
        """
        Get country by alpha code (cca2 or cca3).
        
        Args:
            code: Country code
        
        Returns:
            Response object
        """
        endpoint = f"/alpha/{code}"
        return self._make_request("GET", endpoint)

    def get_countries_by_codes(self, codes: List[str]) -> requests.Response:
        """
        Get countries by multiple codes.
        
        Args:
            codes: List of country codes
        
        Returns:
            Response object
        """
        codes_str = ",".join(codes)
        endpoint = "/alpha"
        params = {"codes": codes_str}
        return self._make_request("GET", endpoint, params=params)

    def get_all_countries(self, fields: Optional[List[str]] = None) -> requests.Response:
        """
        Get all countries.
        
        Args:
            fields: Specific fields to return (required by API)
        
        Returns:
            Response object
        """
        params = None
        if fields:
            params = {"fields": ",".join(fields)}
        else:
            # API requires fields parameter for /all endpoint
            params = {"fields": "name,capital,currencies,region"}
        
        endpoint = "/all"
        return self._make_request("GET", endpoint, params=params)

    def get_countries_by_region(self, region: str) -> requests.Response:
        """
        Get countries by region.
        
        Args:
            region: Region name (e.g., 'europe', 'americas')
        
        Returns:
            Response object
        """
        endpoint = f"/region/{region}"
        return self._make_request("GET", endpoint)

    def get_countries_by_currency(self, currency: str) -> requests.Response:
        """
        Get countries by currency code.
        
        Args:
            currency: Currency code (e.g., 'usd', 'eur')
        
        Returns:
            Response object
        """
        endpoint = f"/currency/{currency}"
        return self._make_request("GET", endpoint)

    def get_countries_by_language(self, language: str) -> requests.Response:
        """
        Get countries by language.
        
        Args:
            language: Language code or name
        
        Returns:
            Response object
        """
        endpoint = f"/lang/{language}"
        return self._make_request("GET", endpoint)

    def get_country_by_capital(self, capital: str) -> requests.Response:
        """
        Get country by capital city.
        
        Args:
            capital: Capital city name
        
        Returns:
            Response object
        """
        endpoint = f"/capital/{capital}"
        return self._make_request("GET", endpoint)

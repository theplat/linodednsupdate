import requests
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class LinodeAPIService:
    BASE_URL = "https://api.linode.com/v4"
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    def test_api_key(self, api_key: str) -> bool:
        """Test if the provided API key is valid."""
        test_session = requests.Session()
        test_session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        })
        try:
            response = test_session.get(f"{self.BASE_URL}/domains")
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False

    def get_domains(self) -> List[Dict[str, Any]]:
        """Get all domains from Linode."""
        if not self.api_key:
            raise ValueError("API key is required")
        response = self.session.get(f"{self.BASE_URL}/domains")
        response.raise_for_status()
        return response.json().get('data', [])

    def get_domain_records(self, domain_id: int) -> List[Dict[str, Any]]:
        """Get all records for a domain."""
        if not self.api_key:
            raise ValueError("API key is required")
        response = self.session.get(f"{self.BASE_URL}/domains/{domain_id}/records")
        response.raise_for_status()
        return response.json().get('data', [])

    def update_domain_record(self, domain_id: int, record_id: int, new_ip: str) -> Dict[str, Any]:
        """Update a domain record with a new IP address."""
        if not self.api_key:
            raise ValueError("API key is required")
        data = {'target': new_ip}
        response = self.session.put(f"{self.BASE_URL}/domains/{domain_id}/records/{record_id}", json=data)
        response.raise_for_status()
        return response.json()

    def get_current_ip(self) -> str:
        """Get the current public IP address."""
        try:
            response = requests.get('https://icanhazip.com')
            response.raise_for_status()
            return response.text.strip()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting current IP: {e}")
            raise 
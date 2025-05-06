import requests
from django.conf import settings
from typing import Optional, Dict, Any, List
import logging
from .models import APIKey

logger = logging.getLogger(__name__)


class LinodeAPIService:
    BASE_URL = "https://api.linode.com/v4"
    
    def __init__(self, user=None):
        self.user = user
        self.api_key = None
        self.session = requests.Session()
        if user:
            try:
                api_key = APIKey.objects.get(user=user)
                self.api_key = api_key.get_key()
                self.session.headers.update({
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                })
            except APIKey.DoesNotExist:
                raise ValueError("No API key configured for this user")

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

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make a request to the Linode API."""
        if not self.api_key:
            raise ValueError("API key is not configured")
            
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.request(method, url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request to Linode API: {e}")
            raise

    def get_domains(self) -> List[Dict[str, Any]]:
        """Get all domains in the account."""
        return self._make_request("GET", "domains")["data"]

    def get_domain_records(self, domain_id: int) -> List[Dict[str, Any]]:
        """Get all DNS records for a domain."""
        return self._make_request("GET", f"domains/{domain_id}/records")["data"]

    def update_domain_record(self, domain_id: int, record_id: int, target: str) -> Dict[str, Any]:
        """Update a DNS record's target (IP address)."""
        data = {"target": target}
        return self._make_request(
            "PUT",
            f"domains/{domain_id}/records/{record_id}",
            data=data
        )

    def get_current_ip(self) -> str:
        """Get the current public IP address."""
        try:
            response = requests.get("https://icanhazip.com")
            response.raise_for_status()
            return response.text.strip()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting current IP address: {e}")
            raise 
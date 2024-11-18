import msal
import requests
from dataclasses import dataclass
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@dataclass
class SPNConfig:
    client_id: str
    client_secret: str
    tenant_id: str
    authority: str = "https://login.microsoftonline.com"
    
    @property
    def authority_url(self) -> str:
        return f"{self.authority}/{self.tenant_id}"

class FabricClient:
    def __init__(self, config: SPNConfig):
        self.config = config
        self.base_url = "https://api.fabric.microsoft.com/v1/"
        self._token: Optional[str] = None
        
        # Initialize MSAL confidential client
        self.app = msal.ConfidentialClientApplication(
            client_id=config.client_id,
            client_credential=config.client_secret,
            authority=config.authority_url
        )
        
    def get_token(self) -> str:
        """Get token using client credentials flow"""
        if not self._token:
            # Define scope for Fabric API with .default suffix
            scope = ["https://api.fabric.microsoft.com/.default"]

            logger.debug(f"Requesting token with scope: {scope}")

            result = self.app.acquire_token_for_client(
                scopes=scope
            )
            
            if "access_token" not in result:
                error_msg = f"Failed to get token: {result.get('error_description', 'Unknown error')}"
                logger.error(error_msg)
                raise ValueError(error_msg)
            
            self._token = result["access_token"]
            logger.debug(f"Token acquired successfully: {self._token[:10]}...")
            
        return self._token

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.get_token()}",
            "Content-Type": "application/json"
        }
        logger.debug(f"Request headers: {headers}")
        return headers
        
    def list_workspaces(self) -> Dict[str, Any]:
        """List all workspaces"""
        response = requests.get(
            f"{self.base_url}workspaces",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

def main():
    # Replace with your SPN credentials
    config = SPNConfig(
        client_id="xxx",
        client_secret="xxx",
        tenant_id="xxx"
    )
    
    try:
        client = FabricClient(config)
        workspaces = client.list_workspaces()
        print("Workspaces:")
        for workspace in workspaces.get('value', []):
            print(f"  • {workspace['displayName']} (ID: {workspace['id']})")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
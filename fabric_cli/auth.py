import os
import json
import msal
import logging
from pathlib import Path
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta

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


@dataclass
class AuthState:
    fabric_token: Optional[str] = None
    fabric_token_expiry: Optional[datetime] = None
    management_token: Optional[str] = None
    management_token_expiry: Optional[datetime] = None
    spn_config: Optional[Dict] = None


class FabricClient:
    def __init__(self, config: SPNConfig, scope: str):
        self.config = config
        self.scope = scope
        self.base_url = "https://api.fabric.microsoft.com/v1/"
        self._token: Optional[str] = None

        # Initialize MSAL confidential client
        self.app = msal.ConfidentialClientApplication(
            client_id=config.client_id,
            client_credential=config.client_secret,
            authority=config.authority_url,
        )
        logger.debug("MSAL ConfidentialClientApplication initialized")

    def get_token(self) -> str:
        """Get token using client credentials flow"""
        if not self._token:
            logger.debug(f"Requesting token with scope: {self.scope}")
            result = self.app.acquire_token_for_client(scopes=[self.scope])
            if "access_token" not in result:
                error_msg = (
                    f"Failed to get token: {result.get('error_description', 'Unknown error')}"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            self._token = result["access_token"]
            logger.debug(f"Token acquired successfully: {self._token[:10]}...")
            logger.info(f"Access token: {self._token}")
        return self._token


class Auth:
    _instance = None
    _state = AuthState()
    _state_file = Path(os.path.expanduser("~/.fabric/auth_state.json"))

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load_state()
        return cls._instance

    @classmethod
    def _load_state(cls):
        """Load authentication state from file"""
        try:
            if cls._state_file.exists():
                with open(cls._state_file) as f:
                    data = json.load(f)
                    cls._state = AuthState(
                        fabric_token=data.get("fabric_token"),
                        fabric_token_expiry=(
                            datetime.fromisoformat(data["fabric_token_expiry"])
                            if data.get("fabric_token_expiry")
                            else None
                        ),
                        management_token=data.get("management_token"),
                        management_token_expiry=(
                            datetime.fromisoformat(data["management_token_expiry"])
                            if data.get("management_token_expiry")
                            else None
                        ),
                        spn_config=data.get("spn_config"),
                    )
                logger.debug(f"Loaded auth state: {cls._state}")
        except Exception as e:
            logger.warning(f"Failed to load auth state: {e}")

    @classmethod
    def _save_state(cls):
        """Save authentication state to file"""
        try:
            cls._state_file.parent.mkdir(parents=True, exist_ok=True)
            state_dict = {
                "fabric_token": cls._state.fabric_token,
                "fabric_token_expiry": (
                    cls._state.fabric_token_expiry.isoformat()
                    if cls._state.fabric_token_expiry
                    else None
                ),
                "management_token": cls._state.management_token,
                "management_token_expiry": (
                    cls._state.management_token_expiry.isoformat()
                    if cls._state.management_token_expiry
                    else None
                ),
                "spn_config": cls._state.spn_config,
            }
            with open(cls._state_file, "w") as f:
                json.dump(state_dict, f)
            logger.debug("Saved auth state")
        except Exception as e:
            logger.warning(f"Failed to save auth state: {e}")

    @classmethod
    def set_token(cls, token: str, provider: str):
        """Set a token manually with a default expiry of 1 hour"""
        logger.debug(f"Setting token manually for {provider}...")
        if provider == "fabric":
            cls._state.fabric_token = token.strip()
            cls._state.fabric_token_expiry = datetime.now() + timedelta(hours=1)
        elif provider == "management":
            cls._state.management_token = token.strip()
            cls._state.management_token_expiry = datetime.now() + timedelta(hours=1)
        cls._save_state()

    @classmethod
    def set_spn_config(cls, config: SPNConfig):
        """Configure service principal authentication"""
        logger.debug("Setting SPN config...")
        cls._state.spn_config = {
            "client_id": config.client_id,
            "tenant_id": config.tenant_id,
            "authority": config.authority,
        }
        cls._save_state()

        # Create new client and fetch initial tokens
        fabric_client = FabricClient(config, "https://api.fabric.microsoft.com/.default")
        fabric_token = fabric_client.get_token()
        cls._state.fabric_token = fabric_token
        cls._state.fabric_token_expiry = datetime.now() + timedelta(hours=1)

        management_client = FabricClient(config, "https://management.azure.com/.default")
        management_token = management_client.get_token()
        cls._state.management_token = management_token
        cls._state.management_token_expiry = datetime.now() + timedelta(hours=1)

        cls._save_state()
        logger.debug(f"SPN client configured with client_id: {config.client_id}")

    def _refresh_token(self, provider: str):
        """Internal method to refresh the token using SPN config"""
        if not self._state.spn_config:
            raise ValueError("No SPN configuration available")

        config = SPNConfig(
            client_id=self._state.spn_config["client_id"],
            client_secret=os.getenv("AZURE_CLIENT_SECRET"),
            tenant_id=self._state.spn_config["tenant_id"],
            authority=self._state.spn_config["authority"],
        )
        if provider == "fabric":
            client = FabricClient(config, "https://api.fabric.microsoft.com/.default")
            self._state.fabric_token = client.get_token()
            self._state.fabric_token_expiry = datetime.now() + timedelta(hours=1)
        elif provider == "management":
            client = FabricClient(config, "https://management.azure.com/.default")
            self._state.management_token = client.get_token()
            self._state.management_token_expiry = datetime.now() + timedelta(hours=1)
        self._save_state()

    def _is_token_valid(self, provider: str) -> bool:
        """Check if the current token is valid"""
        if provider == "fabric":
            token = self._state.fabric_token
            expiry = self._state.fabric_token_expiry
        elif provider == "management":
            token = self._state.management_token
            expiry = self._state.management_token_expiry
        else:
            return False

        if not token or not expiry:
            return False
        return datetime.now() < expiry

    def get_access_token(self, provider: str) -> str:
        """Get a valid access token, refreshing if necessary"""
        logger.debug(f"Getting access token for {provider}...")

        # Check if we need to refresh the token
        if not self._is_token_valid(provider):
            logger.debug(f"Token expired or missing for {provider}, refreshing...")
            self._refresh_token(provider)

        token = self._state.fabric_token if provider == "fabric" else self._state.management_token
        logger.debug(f"Using token for {provider}: {token[:10]}...")
        return token

    def get_headers(self, provider: str) -> Dict[str, str]:
        """Get headers with a valid access token"""
        token = self.get_access_token(provider)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        logger.debug(f"Generated headers with valid token for {provider}")
        logger.debug(headers)
        return headers

    def __str__(self):
        return f"Auth state: {self._state}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_state(cls):
        """Get the current state of the Auth class"""
        return cls._state

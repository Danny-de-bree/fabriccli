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
    token: Optional[str] = None
    token_expiry: Optional[datetime] = None
    spn_config: Optional[Dict] = None


class FabricClient:
    def __init__(self, config: SPNConfig):
        self.config = config
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
            # Define scope for Fabric API with .default suffix
            scope = ["https://api.fabric.microsoft.com/.default"]

            logger.debug(f"Requesting token with scope: {scope}")

            result = self.app.acquire_token_for_client(scopes=scope)

            if "access_token" not in result:
                error_msg = (
                    f"Failed to get token: {result.get('error_description', 'Unknown error')}"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            self._token = result["access_token"]
            logger.debug(f"Token acquired successfully: {self._token[:10]}...")

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
                        token=data.get("token"),
                        token_expiry=(
                            datetime.fromisoformat(data["token_expiry"])
                            if data.get("token_expiry")
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
                "token": cls._state.token,
                "token_expiry": (
                    cls._state.token_expiry.isoformat() if cls._state.token_expiry else None
                ),
                "spn_config": cls._state.spn_config,
            }
            with open(cls._state_file, "w") as f:
                json.dump(state_dict, f)
            logger.debug("Saved auth state")
        except Exception as e:
            logger.warning(f"Failed to save auth state: {e}")

    @classmethod
    def set_token(cls, token: str):
        """Set a token manually with a default expiry of 1 hour"""
        logger.debug("Setting token manually...")
        cls._state.token = token.strip()
        cls._state.token_expiry = datetime.now() + timedelta(hours=1)
        cls._save_state()
        logger.debug(f"Token set: {cls._state.token[:10]}... expires at {cls._state.token_expiry}")

    @classmethod
    def set_spn_config(cls, config: SPNConfig):
        """Configure service principal authentication"""
        logger.debug("Setting SPN config...")
        cls._state.spn_config = {
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "tenant_id": config.tenant_id,
            "authority": config.authority,
        }
        cls._save_state()

        # Create new client and fetch initial token
        spn_client = FabricClient(config)
        result = spn_client.get_token()

        if isinstance(result, dict):
            cls._state.token = result["access_token"]
            expires_in = result.get("expires_in", 3600)
            cls._state.token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
        else:
            cls._state.token = result
            cls._state.token_expiry = datetime.now() + timedelta(hours=1)

        cls._save_state()
        logger.debug(f"SPN client configured with client_id: {config.client_id}")

    def _refresh_token(self):
        """Internal method to refresh the token using SPN config"""
        if not self._state.spn_config:
            raise ValueError("No SPN configuration available")

        config = SPNConfig(**self._state.spn_config)
        spn_client = FabricClient(config)
        result = spn_client.get_token()

        if isinstance(result, dict):
            self._state.token = result["access_token"]
            expires_in = result.get("expires_in", 3600)
            self._state.token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
        else:
            self._state.token = result
            self._state.token_expiry = datetime.now() + timedelta(hours=1)

        self._save_state()
        logger.debug(
            f"Token refreshed: {self._state.token[:10]}... expires at {self._state.token_expiry}"
        )

    def _is_token_valid(self) -> bool:
        """Check if the current token is valid"""
        if not self._state.token or not self._state.token_expiry:
            return False
        return datetime.now() < self._state.token_expiry

    def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        logger.debug("Getting access token...")

        # First try environment variable
        env_token = os.getenv("POWER_BI_ACCESS_TOKEN")
        if env_token:
            logger.debug("Using token from environment variable")
            self.set_token(env_token)
            return self._state.token

        # Check if we need to refresh the token
        if not self._is_token_valid():
            logger.debug("Token expired or missing, refreshing...")
            if self._state.spn_config:
                self._refresh_token()
            else:
                logger.error("No valid token source available")
                raise ValueError("No valid token source available")

        logger.debug(f"Using token: {self._state.token[:10]}...")
        return self._state.token

    def get_headers(self) -> Dict[str, str]:
        """Get headers with a valid access token"""
        token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        logger.debug("Generated headers with valid token")
        return headers

    @classmethod
    def get_state(cls):
        """Get the current state of the Auth class"""
        return cls._state

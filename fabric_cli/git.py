import requests
from typing import Dict
from .auth import Auth
import logging

logger = logging.getLogger(__name__)


def connect_git_repository(
    workspace_id: str, git_provider_details: Dict[str, str], auth: Auth
) -> None:
    """
    Connects a workspace to a Git repository.

    Args:
        workspace_id: The ID of the workspace to connect.
        git_provider_details: A dictionary containing the Git provider details.
        auth: Authentication instance for getting headers.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/git/connect"
    json_payload = {"gitProviderDetails": git_provider_details}

    try:
        logger.debug(
            f"Connecting workspace {workspace_id} to Git repository with payload: {json_payload}"
        )
        response = requests.post(url, json=json_payload, headers=auth.get_headers())
        response.raise_for_status()
        logger.debug(f"Workspace {workspace_id} successfully connected to Git repository")

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error connecting workspace to Git repository: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)

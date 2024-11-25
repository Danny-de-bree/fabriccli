import requests
from typing import List, Tuple
from .auth import Auth
import logging

logger = logging.getLogger(__name__)


def create_lakehouse(workspace_id: str, display_name: str, auth: Auth) -> str:
    """
    Creates a new lakehouse in the specified workspace.

    Args:
        workspace_id: The ID of the workspace where the lakehouse will be created.
        display_name: The display name for the new lakehouse.
        auth: Authentication instance for getting headers.

    Returns:
        str: The ID of the created lakehouse.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"
    json_payload = {"displayName": display_name}

    try:
        logger.debug(f"Creating lakehouse with payload: {json_payload}")
        response = requests.post(url, json=json_payload, headers=auth.get_headers())
        response.raise_for_status()
        lakehouse_id = response.json()["id"]
        logger.debug(f"Lakehouse created with ID: {lakehouse_id}")
        return lakehouse_id

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error creating lakehouse: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)


def get_lakehouses(workspace_id: str, auth: "Auth") -> List[Tuple[str, str]]:
    """
    Get all lakehouses in a workspace.

    Args:
        workspace_id: The ID of the workspace to list lakehouses from.
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing lakehouse IDs and display names.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"
    logger.debug(f"Fetching lakehouses for workspace ID: {workspace_id}")
    response = requests.get(url, headers=auth.get_headers())
    response.raise_for_status()

    response_data = response.json()
    lakehouse_list = []

    for lakehouse in response_data.get("value", []):
        lakehouse_id = lakehouse.get("id")
        display_name = lakehouse.get("displayName")
        if lakehouse_id and display_name:
            lakehouse_list.append((lakehouse_id, display_name))

    logger.debug(f"Fetched lakehouses: {lakehouse_list}")
    return lakehouse_list

import requests
from urllib.parse import urlparse
from typing import List, Tuple, Optional
from .auth import Auth
import logging

logger = logging.getLogger(__name__)


def create_workspace(display_name: str, auth: Auth, capacity_id: Optional[str] = None) -> str:
    """
    Creates a new workspace in the Microsoft Fabric API.

    Args:
        display_name: The display name for the new workspace.
        auth: Authentication instance for getting headers.
        capacity_id: Optional capacity ID to associate with the workspace.

    Returns:
        str: The ID of the created workspace.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = "https://api.fabric.microsoft.com/v1/workspaces/"
    json_payload = {"displayName": display_name}

    if capacity_id:
        json_payload["capacityId"] = capacity_id

    try:
        logger.debug(f"Creating workspace with payload: {json_payload}")
        response = requests.post(url, json=json_payload, headers=auth.get_headers())
        response.raise_for_status()
        location_header = response.headers.get("Location")
        if not location_header:
            raise ValueError("No Location header in response")

        workspace_id = urlparse(location_header).path.split("/")[-1]
        logger.debug(f"Workspace created with ID: {workspace_id}")
        return workspace_id

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error creating workspace: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)


def get_workspaces(auth: Auth) -> List[Tuple[str, str, str]]:
    """
    Fetches the list of workspace IDs and display names.

    Args:
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing workspace IDs, display names, and capacity IDs.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = "https://api.fabric.microsoft.com/v1/workspaces"

    try:
        response = requests.get(url, headers=auth.get_headers())
        response.raise_for_status()
        workspaces = response.json().get("value", [])
        return [(ws["id"], ws["displayName"], ws.get("capacityId")) for ws in workspaces]

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error fetching workspaces: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)


def provision_workspace_identity(workspace_id: str, auth: "Auth") -> bool:
    """
    Provisions an identity for the specified workspace.

    Args:
        workspace_id: The ID of the workspace.
        auth: Authentication instance for getting headers.

    Returns:
        bool: True if the identity was provisioned successfully.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/provisionIdentity"
    logger.debug(f"Provisioning identity for workspace ID: {workspace_id}")
    response = requests.post(url, headers=auth.get_headers())
    response.raise_for_status()
    logger.debug(f"Identity provisioned for workspace ID: {workspace_id}")
    return True


def assign_workspace_to_capacity(workspace_id: str, capacity_id: str, auth: "Auth") -> bool:
    """
    Assigns the specified workspace to a capacity.

    Args:
        workspace_id: The ID of the workspace.
        capacity_id: The ID of the capacity.
        auth: Authentication instance for getting headers.

    Returns:
        bool: True if the workspace was assigned to the capacity successfully.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/assignToCapacity"
    json_payload = {"capacityId": capacity_id}
    logger.debug(f"Assigning workspace ID {workspace_id} to capacity ID {capacity_id}")
    response = requests.post(url, json=json_payload, headers=auth.get_headers())
    response.raise_for_status()
    logger.debug(f"Workspace ID {workspace_id} assigned to capacity ID {capacity_id}")
    return True

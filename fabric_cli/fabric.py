import requests
from urllib.parse import urlparse
from typing import List, Tuple, Optional
from .auth import Auth
import logging

logger = logging.getLogger(__name__)


def create_workspace(display_name: str, auth: "Auth", capacity_id: Optional[str] = None) -> str:
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


def get_workspaces(auth: "Auth") -> List[Tuple[str, str, str]]:
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

        response_data = response.json()
        workspace_list = []

        for workspace in response_data.get("value", []):
            workspace_id = workspace.get("id")
            display_name = workspace.get("displayName")
            capacity_id = workspace.get("capacityId")
            if workspace_id and display_name:
                workspace_list.append((workspace_id, display_name, capacity_id))

        logger.debug(f"Fetched workspaces: {workspace_list}")
        return workspace_list

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


def create_lakehouse(workspace_id: str, display_name: str, auth: "Auth") -> str:
    """
    Creates a new lakehouse in the specified workspace.

    Args:
        workspace_id: The ID of the workspace.
        display_name: The display name for the new lakehouse.
        auth: Authentication instance for getting headers.

    Returns:
        str: The ID of the created lakehouse.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"
    json_payload = {"displayName": display_name}
    logger.debug(f"Creating lakehouse with payload: {json_payload}")
    response = requests.post(url, json=json_payload, headers=auth.get_headers())
    response.raise_for_status()
    response_data = response.json()
    lakehouse_id = response_data["id"]
    logger.debug(f"Lakehouse created with ID: {lakehouse_id}")
    return lakehouse_id


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


def create_warehouse(workspace_id: str, display_name: str, auth: "Auth") -> str:
    """
    Creates a new warehouse in the specified workspace.

    Args:
        workspace_id: The ID of the workspace.
        display_name: The display name for the new warehouse.
        auth: Authentication instance for getting headers.

    Returns:
        str: The ID of the created warehouse.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"
    json_payload = {"displayName": display_name}
    logger.debug(f"Creating warehouse with payload: {json_payload}")
    response = requests.post(url, json=json_payload, headers=auth.get_headers())
    response.raise_for_status()
    response_data = response.json()
    warehouse_id = response_data["id"]
    logger.debug(f"Warehouse created with ID: {warehouse_id}")
    return warehouse_id


def get_warehouses(workspace_id: str, auth: "Auth") -> List[Tuple[str, str]]:
    """
    Get all warehouses in a workspace.

    Args:
        workspace_id: The ID of the workspace to list warehouses from.
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing warehouse IDs and display names.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"
    logger.debug(f"Fetching warehouses for workspace ID: {workspace_id}")
    headers = auth.get_headers()
    logger.debug(f"Request headers: {headers}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    response_data = response.json()
    warehouse_list = []

    for warehouse in response_data.get("value", []):
        warehouse_id = warehouse.get("id")
        display_name = warehouse.get("displayName")
        if warehouse_id and display_name:
            warehouse_list.append((warehouse_id, display_name))

    logger.debug(f"Fetched warehouses: {warehouse_list}")
    return warehouse_list

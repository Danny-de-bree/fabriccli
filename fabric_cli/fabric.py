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


def get_workspaces(auth: "Auth") -> List[Tuple[str, str]]:
    """
    Fetches the list of workspace IDs and display names.

    Args:
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing workspace IDs and display names.

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
        raise requests.exceptions.HTTPError(error_msg)


def provision_workspace_identity(workspace_id, auth: "Auth"):
    """
    Provision an identity for a specified workspace.

    Args:
        workspace_id (str): The ID of the workspace for which to provision an identity.
        auth (Auth): Authentication instance for getting headers.

    Returns:
        bool: True if the identity was successfully provisioned; raises an error otherwise.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/provisionIdentity"

    # Send the POST request to provision the identity
    response = requests.post(url, headers=auth.get_headers())

    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as err:
        error_msg = f"Error provisioning identity for workspace {workspace_id}: {err}"
        if response.content:
            error_msg += f"\nResponse: {response.content.decode()}"
        raise requests.exceptions.HTTPError(error_msg)


def assign_workspace_to_capacity(workspace_id: str, capacity_id: str, auth: "Auth") -> bool:
    """
    Assign a workspace to a capacity.

    Args:
        workspace_id (str): The ID of the workspace to assign
        capacity_id (str): The ID of the capacity to assign the workspace to
        auth (Auth): Authentication instance for getting headers

    Returns:
        bool: True if successfully assigned, raises an error otherwise

    Raises:
        requests.exceptions.HTTPError: If the API request fails
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/assignToCapacity"

    payload = {"capacityId": capacity_id}

    response = requests.post(url, json=payload, headers=auth.get_headers())

    try:
        response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as err:
        error_msg = f"Error assigning workspace {workspace_id} to capacity {capacity_id}: {err}"
        if response.content:
            error_msg += f"\nResponse: {response.content.decode()}"
        raise requests.exceptions.HTTPError(error_msg)


def create_lakehouse(
    workspace_id: str, display_name: str, auth: "Auth", description: str = None
) -> str:
    """Creates a new lakehouse in the specified workspace.

    Args:
        workspace_id: The ID of the workspace to create the lakehouse in.
        display_name: The display name for the new lakehouse.
        auth: Authentication instance for getting headers.
        description: Optional description for the lakehouse.

    Returns:
        str: The ID of the created lakehouse.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"

    json_payload = {"displayName": display_name}

    if description:
        json_payload["description"] = description

    response = requests.post(url, json=json_payload, headers=auth.get_headers())

    try:
        response.raise_for_status()
        response_data = response.json()
        return response_data["id"]
    except requests.exceptions.HTTPError as e:
        error_msg = f"Error creating lakehouse: {str(e)}"
        if e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        raise requests.exceptions.HTTPError(error_msg)


def get_lakehouses(workspace_id: str, auth: "Auth") -> List[Tuple[str, str]]:
    """
    Get all lakehouses in a workspace.

    Args:
        workspace_id: The ID of the workspace to list lakehouses from.
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing lakehouse IDs and display names.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses"

    try:
        response = requests.get(url, headers=auth.get_headers())
        response.raise_for_status()

        response_data = response.json()
        lakehouse_list = []

        for lakehouse in response_data.get("value", []):
            lakehouse_id = lakehouse.get("id")
            display_name = lakehouse.get("displayName")
            if lakehouse_id and display_name:
                lakehouse_list.append((lakehouse_id, display_name))

        return lakehouse_list

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error fetching lakehouses: {str(e)}"
        if e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        raise requests.exceptions.HTTPError(error_msg)


def create_warehouse(workspace_id: str, display_name: str, auth: "Auth") -> str:
    """Creates a new warehouse in the specified workspace.

    Args:
        workspace_id: The ID of the workspace to create the warehouse in.
        display_name: The display name for the new warehouse.
        auth: Authentication instance for getting headers.

    Returns:
        str: The ID of the created warehouse.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"

    json_payload = {"displayName": display_name}

    headers = auth.get_headers()

    response = requests.post(url, json=json_payload, headers=headers)

    try:
        response.raise_for_status()
        response_data = response.json()
        if not response_data:
            raise ValueError("Empty response received")
        return response_data["id"]
    except requests.exceptions.HTTPError as e:
        error_msg = f"Error creating warehouse: {str(e)}"
        if e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        raise requests.exceptions.HTTPError(error_msg)


def get_warehouses(workspace_id: str, auth: "Auth") -> List[Tuple[str, str]]:
    """
    Get all warehouses in a workspace.

    Args:
        workspace_id: The ID of the workspace to list warehouses from.
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing warehouse IDs and display names.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"

    try:
        response = requests.get(url, headers=auth.get_headers())
        response.raise_for_status()

        response_data = response.json()
        warehouse_list = []

        for warehouse in response_data.get("value", []):
            warehouse_id = warehouse.get("id")
            display_name = warehouse.get("displayName")
            if warehouse_id and display_name:
                warehouse_list.append((warehouse_id, display_name))

        return warehouse_list

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error fetching warehouses: {str(e)}"
        if e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        raise requests.exceptions.HTTPError(error_msg)

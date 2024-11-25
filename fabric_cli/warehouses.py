import requests
from typing import List, Tuple
from .auth import Auth
import logging

logger = logging.getLogger(__name__)


def create_warehouse(workspace_id: str, display_name: str, auth: Auth) -> str:
    """
    Creates a new warehouse in the specified workspace.

    Args:
        workspace_id: The ID of the workspace where the warehouse will be created.
        display_name: The display name for the new warehouse.
        auth: Authentication instance for getting headers.

    Returns:
        str: The ID of the created warehouse.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"
    json_payload = {"displayName": display_name}

    try:
        logger.debug(f"Creating warehouse with payload: {json_payload}")
        response = requests.post(url, json=json_payload, headers=auth.get_headers())
        response.raise_for_status()
        warehouse_id = response.json()["id"]
        logger.debug(f"Warehouse created with ID: {warehouse_id}")
        return warehouse_id

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error creating warehouse: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)


def get_warehouses(workspace_id: str, auth: Auth) -> List[Tuple[str, str]]:
    """
    Fetches the list of warehouse IDs and display names in the specified workspace.

    Args:
        workspace_id: The ID of the workspace.
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing warehouse IDs and display names.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/warehouses"

    try:
        response = requests.get(url, headers=auth.get_headers())
        response.raise_for_status()
        warehouses = response.json().get("value", [])
        return [(wh["id"], wh["displayName"]) for wh in warehouses]

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error fetching warehouses: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)

"""
fabric.py

This script helps to interact with the Microsoft Fabric API.

Author: Danny de Bree
Date: 05/11/2024
"""

import requests
from urllib.parse import urlparse
from typing import List, Tuple, Optional
from fabric_cli.auth import Auth

"""
TODO: Implement the following functions to interact with the Microsoft Fabric API:
- Pass capacity_id from api to the create_workspace function.
    - What do we do if there are multiple capacity_ids?

- Add AAD group to workspace
     - Very hard need to investigate more.

- Add authentication with SPN
    - Investigate how to authenticate with SPN.

- Add shortcut with OneLake from storage account.

- Clean some print statements and add logging.

- Add tests for the functions.

"""

def create_workspace(display_name: str, auth: 'Auth', capacity_id: Optional[str] = None) -> str:
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

    response = requests.post(url, json=json_payload, headers=auth.get_headers())
    response.raise_for_status()
    
    location_header = response.headers.get("Location")
    if not location_header:
        raise ValueError("No Location header in response")
        
    workspace_id = urlparse(location_header).path.split('/')[-1]
    return workspace_id

def get_workspaces(auth: 'Auth') -> List[Tuple[str, str]]:
    """
    Fetches the list of workspace IDs and display names.

    Args:
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing workspace IDs and display names.
        
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = "https://api.fabric.microsoft.com/v1/workspaces/"
    response = requests.get(url, headers=auth.get_headers())
    response.raise_for_status()
    
    response_data = response.json()
    workspace_list = []

    for workspace in response_data.get('value', []):
        workspace_id = workspace.get('id')
        display_name = workspace.get('displayName')
        if workspace_id and display_name:
            workspace_list.append((workspace_id, display_name))
            
    return workspace_list

def provision_identity(workspace_id, auth):
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

"""
fabric.py

This script helps to interact with the Microsoft Fabric API.

Author: Danny de Bree
Date: 05/11/2024
"""

import os
import requests
from urllib.parse import urlparse

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

def get_access_token():
    """Retrieve the Power BI access token from environment variables."""
    access_token = os.getenv("POWER_BI_ACCESS_TOKEN")
    if access_token is None:
        raise ValueError("No access token found in environment variables.")
    return access_token.strip()

def create_workspace(display_name, capacity_id=None):
    """
    Creates a new workspace in the Microsoft Fabric API.

    Args:
        display_name (str): The display name for the new workspace.
        capacity_id (str, optional): The capacity ID to associate with the workspace.

    Returns:
        str: The ID of the created workspace if successful; raises an error otherwise.
    """
    url = "https://api.fabric.microsoft.com/v1/workspaces/"
    json_payload = {
        "displayName": display_name,
    }
    
    # Set the headers using the access token
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    # Send the POST request to create the workspace
    response = requests.post(url, json=json_payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code in (200, 201):
        print(f"Workspace '{display_name}' creation request accepted. Processing in progress.")
        location_header = response.headers.get("Location")
        parsed_url = urlparse(location_header)
        path_parts = parsed_url.path.split('/')
        workspace_id = path_parts[-1]
        
        print(location_header)
        print(f"Workspace ID: {workspace_id}")
        
        return workspace_id
    else:
        print("Failed to create workspace.")
        return None

def get_workspaces():
    """
    Fetches the list of workspace IDs and display names from the Microsoft Fabric API.

    Returns:
        list: A list of tuples containing workspace IDs and display names if the request is successful; 
        raises an error otherwise.
    """
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    
    url = "https://api.fabric.microsoft.com/v1/workspaces/"
    response = requests.get(url, headers=headers)

    # Check the response
    response.raise_for_status()
    
    if response.status_code == 200:
        print("Request successful. Here are the workspaces:")
        response_data = response.json()

        workspace_list = []  # List to store workspace IDs and display names
        if 'value' in response_data:
            for workspace in response_data['value']:
                workspace_id = workspace.get('id')  # Get the workspace ID
                display_name = workspace.get('displayName')  # Get the display name
                if workspace_id and display_name:  # Ensure neither is None or empty
                    workspace_list.append((workspace_id, display_name))  # Append as a tuple
        else:
            print("No workspaces found in the response.")
        
        return workspace_list  # Return the list of workspace IDs and names
    else:
        print("Failed to retrieve workspaces.")
        return []  # Return an empty list in case of failure

def provision_identity(workspace_id):
    """
    Provision an identity for a specified workspace.

    Args:
        workspace_id (str): The ID of the workspace for which to provision an identity.

    Returns:
        bool: True if the identity was successfully provisioned; False otherwise.
    """
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/provisionIdentity"
    
    # Send the POST request to provision the identity
    response = requests.post(url, headers=headers)

    # Check the response
    try:
        response.raise_for_status()
        print(f"Successfully provisioned identity for workspace ID: {workspace_id}")
        return True
    except requests.exceptions.HTTPError as err:
        print(f"Error provisioning identity for workspace ID {workspace_id}: {err}")
        print(f"Response content: {response.content}")
        return False

import requests
from typing import Dict
import logging

logger = logging.getLogger(__name__)

API_VERSION = "2022-07-01-preview"


def suspend_capacity(
    subscription_id: str, resource_group_name: str, dedicated_capacity_name: str, access_token: str
) -> Dict:
    """
    Suspend a dedicated capacity in Azure.

    Args:
        subscription_id: The subscription ID.
        resource_group_name: The resource group name.
        dedicated_capacity_name: The dedicated capacity name.
        access_token: The access token.

    Returns:
        Dict: The response from the API.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/"
        f"{resource_group_name}/providers/Microsoft.Fabric/capacities/{dedicated_capacity_name}/"
        f"suspend?api-version={API_VERSION}"
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        logger.debug(f"Suspended capacity: {dedicated_capacity_name}")
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error suspending capacity: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)


def resume_capacity(
    subscription_id: str, resource_group_name: str, dedicated_capacity_name: str, access_token: str
) -> Dict:
    """
    Resume a dedicated capacity in Azure.

    Args:
        subscription_id: The subscription ID.
        resource_group_name: The resource group name.
        dedicated_capacity_name: The dedicated capacity name.
        access_token: The access token.

    Returns:
        Dict: The response from the API.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/"
        f"{resource_group_name}/providers/Microsoft.Fabric/capacities/{dedicated_capacity_name}/"
        f"suspend?api-version={API_VERSION}"
    )
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        logger.debug(f"Resumed capacity: {dedicated_capacity_name}")
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error resuming capacity: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)

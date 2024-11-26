import requests
from typing import Dict
import logging
from .auth import Auth

logger = logging.getLogger(__name__)

API_VERSION = "2022-07-01-preview"


def suspend_capacity(
    subscription_id: str, resource_group_name: str, dedicated_capacity_name: str
) -> Dict:
    """
    Suspend a dedicated capacity.

    Args:
        subscription_id (str): The subscription ID.
        resource_group_name (str): The resource group name.
        dedicated_capacity_name (str): The dedicated capacity name.

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

    try:
        # Log the request details
        logger.info(f"Attempting to suspend capacity from URL: {url}")

        # Get and log headers (without exposing full token)
        auth = Auth()
        headers = auth.get_headers("management")
        masked_headers = {
            k: (v[:10] + "..." if k == "Authorization" else v) for k, v in headers.items()
        }
        logger.debug(f"Request headers: {masked_headers}")

        # Make the API request
        response = requests.post(url, headers=headers)

        # Log response status and basic details
        logger.debug(f"Response received. Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Content: {response.content}")

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Handle empty response for 202 Accepted
        if response.status_code == 202:
            return logger.debug("Request accepted and is being processed asynchronously.")

        # Return the response JSON if not empty
        if response.content:
            return response.json()
        else:
            return logger.debug("No content in response")

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error suspending capacity: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)


def resume_capacity(
    subscription_id: str, resource_group_name: str, dedicated_capacity_name: str
) -> Dict:
    """
    Resume a dedicated capacity.

    Args:
        subscription_id (str): The subscription ID.
        resource_group_name (str): The resource group name.
        dedicated_capacity_name (str): The dedicated capacity name.

    Returns:
        Dict: The response from the API.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = (
        f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/"
        f"{resource_group_name}/providers/Microsoft.Fabric/capacities/{dedicated_capacity_name}/"
        f"resume?api-version={API_VERSION}"
    )

    try:
        # Log the request details
        logger.info(f"Attempting to resume capacity from URL: {url}")

        # Get and log headers (without exposing full token)
        auth = Auth()
        headers = auth.get_headers("management")
        masked_headers = {
            k: (v[:10] + "..." if k == "Authorization" else v) for k, v in headers.items()
        }
        logger.debug(f"Request headers: {masked_headers}")

        # Make the API request
        response = requests.post(url, headers=headers)

        # Log response status and basic details
        logger.debug(f"Response received. Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Content: {response.content}")

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Handle empty response for 202 Accepted
        if response.status_code == 202:
            return logger.debug("Request accepted and is being processed asynchronously.")

        # Return the response JSON if not empty
        if response.content:
            return response.json()
        else:
            return logger.debug("No content in response")

    except requests.exceptions.HTTPError as e:
        error_msg = f"Error resuming capacity: {str(e)}"
        if e.response and e.response.content:
            error_msg += f"\nResponse: {e.response.content.decode()}"
        logger.error(error_msg)
        raise requests.exceptions.HTTPError(error_msg)

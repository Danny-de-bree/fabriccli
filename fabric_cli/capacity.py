import requests
from typing import List, Tuple
from .auth import Auth
import logging

logger = logging.getLogger(__name__)


def get_capacities(auth: Auth) -> List[Tuple[str, str]]:
    """
    Get all capacities.

    Args:
        auth: Authentication instance for getting headers.

    Returns:
        List of tuples containing capacity IDs and display names.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = "https://api.fabric.microsoft.com/v1/capacities"
    logger.debug("Fetching capacities")
    response = requests.get(url, headers=auth.get_headers("fabric"))
    response.raise_for_status()

    response_data = response.json()
    capacity_list = []

    for capacity in response_data.get("value", []):
        capacity_id = capacity.get("id")
        display_name = capacity.get("displayName")
        if capacity_id and display_name:
            capacity_list.append((capacity_id, display_name))

    logger.debug(f"Fetched capacities: {capacity_list}")
    return capacity_list

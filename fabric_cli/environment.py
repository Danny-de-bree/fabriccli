import re
import requests
from .auth import Auth
import logging
import os
from requests_toolbelt import MultipartEncoder

logger = logging.getLogger(__name__)


def list_environments(workspace_id: str, auth: Auth) -> dict:
    """
    List all Spark environments in a workspace.

    Args:
        workspace_id: The ID of the workspace.
        auth: Authentication instance for getting headers.
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments"

    response = requests.get(url, headers=auth.get_headers("fabric"))
    response.raise_for_status()

    environments = response.json()["value"]
    logger.debug(f"Found environments: {environments}")

    return environments


def publish_environment(workspace_id: str, environment_id: str, auth: Auth) -> None:
    """
    Publish a Spark environment in a workspace.

    Args:
        workspace_id: The ID of the workspace.
        environment_id: The ID of the environment
        auth: Authentication instance for getting headers.
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/publish"  # noqa: E501

    response = requests.post(url, headers=auth.get_headers("fabric"))
    response.raise_for_status()


def upload_staging_library(
    workspace_id: str, environment_name: str, library_path: str, auth: Auth
) -> None:
    """
    Uploads a library to the selected Spark environment.

    Args:
        workspace_id: The ID of the workspace where the lakehouse will be created.
        environment_name: The Spark environment name
        library_path: Absolute path to the library
        auth: Authentication instance for getting headers.
    Raises:
        KeyError: If the environment is not known
        FileNotFoundError: If the library path is invalid
        requests.exceptions.HTTPError: If the API request fails.
    """
    # Get environment
    environments = list_environments(workspace_id, auth)
    try:
        environment_id = next(
            environment["id"]
            for environment in environments
            if environment["displayName"] == environment_name
        )
    except StopIteration:
        raise KeyError(f"Environment with name '{environment_name}' is not known.")

    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"  # noqa: E501

    # Read file contents
    with open(library_path, "rb") as fb:
        file_content = fb.read()

    # Encode file
    library_name = os.path.basename(library_path)

    library_name_normalized = re.sub(
        r"\d+\.\d+\.\d+", "", library_name
    )  # remove semantic versioning
    library_name_normalized = re.sub(
        r"--", "-", library_name_normalized
    )  # remove remaining double hyphens

    data = MultipartEncoder(
        fields={
            "file": (
                library_name_normalized,
                file_content,
                "application/octet-stream",
            )
        }
    )

    # Upload library
    logger.debug(f"Uploading library: {library_name}")
    response = requests.post(
        url,
        data=data,
        headers={
            **auth.get_headers("fabric"),
            **{
                "Content-Type": data.content_type,
            },
        },
    )
    response.raise_for_status()

    # Publish environment
    publish_environment(workspace_id, environment_id, auth)

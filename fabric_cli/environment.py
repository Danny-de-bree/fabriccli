import requests
from .auth import Auth
import logging
import os

logger = logging.getLogger(__name__)


def list_environments(workspace_id: str, auth: Auth) -> list:
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


def list_staging_libraries(workspace_id: str, environment_id: str, auth: Auth) -> dict:
    """
    List staging libraries in the selected Spark environment.

    Args:
        workspace_id: The ID of the workspace
        environment_id: The Spark environment ID
        auth: Authentication instance for getting headers.
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"  # noqa: E501

    response = requests.get(url, headers=auth.get_headers("fabric"))
    response.raise_for_status()

    staging_libraries = response.json()
    logger.debug(f"Found staging libaries: {staging_libraries}")

    return staging_libraries


def delete_staging_library(
    workspace_id: str, environment_id: str, library_name: str, auth: Auth
) -> None:
    """
    Delete staging library in the selected Spark environment.

    Args:
        workspace_id: The ID of the workspace
        environment_id: The Spark environment ID
        library_name: The library file to be deleted (including extension)
        auth: Authentication instance for getting headers.
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"  # noqa: E501

    response = requests.delete(
        url,
        params={"libraryToDelete": library_name},
        headers=auth.get_headers("fabric"),
    )
    response.raise_for_status()


def delete_python_package_wheels(
    workspace_id: str, environment_id: str, package_name: str, auth: Auth
) -> None:
    """
    Delete all package wheels that exist of a Python package.

    Args:
        workspace_id: The ID of the workspace
        environment_id: The Spark environment ID
        package_name: Name of the Python package
        auth: Authentication instance for getting headers.
    Raises:
        requests.exceptions.HTTPError: If the API request fails.
    """
    staging_libraries = list_staging_libraries(workspace_id, environment_id, auth)

    wheels: list[str] = staging_libraries["customLibraries"]["wheelFiles"]
    package_wheels = [
        wheel for wheel in wheels if "".join(wheel.split(".")[0].split("-")[:-1]) == package_name
    ]

    for wheel in package_wheels:
        logger.debug(f"Deleting wheel: {wheel}.")
        delete_staging_library(workspace_id, environment_id, wheel, auth)


def upload_staging_library(
    workspace_id: str, environment_id: str, library_path: str, auth: Auth
) -> None:
    """
    Uploads a library to the selected Spark environment.

    Args:
        workspace_id: The ID of the workspace
        environment_id: The Spark environment ID
        library_path: Absolute path to the library
        auth: Authentication instance for getting headers.
    Raises:
        FileNotFoundError: If the library path is invalid
        requests.exceptions.HTTPError: If the API request fails.
    """
    url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/environments/{environment_id}/staging/libraries"  # noqa: E501
    library_name = os.path.basename(library_path)

    logger.debug(f"Uploading library: {library_name}")
    response = requests.post(
        url,
        files={"file": (library_name, open(library_path, "rb"))},
        headers={"Authorization": auth.get_headers("fabric")["Authorization"]},
    )
    response.raise_for_status()

from fabric_cli.environment import (
    delete_python_package_wheels,
    delete_staging_library,
    list_environments,
    list_staging_libraries,
    publish_environment,
    upload_staging_library,
)
from unittest.mock import MagicMock
from tests.conftest import AUTH_HEADER, mocked_request, mocked_response
from pytest import MonkeyPatch
import pytest
import requests
import builtins


def test_list_environments_success(monkeypatch: MonkeyPatch, auth: MagicMock) -> None:
    # Arrange
    mock_response = mocked_response(
        return_value={
            "value": [
                {
                    "id": "932fb819-90c0-4d03-918d-bc6fc20cd545",
                    "type": "Environment",
                    "displayName": "ev_main",
                }
            ]
        }
    )
    mock_request = mocked_request(mock_response)
    monkeypatch.setattr(requests, "get", mock_request)

    # Act
    environments = list_environments(workspace_id="workspace-id", auth=auth)

    # Assert
    mock_request.assert_called_once_with(
        "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/environments",
        headers=AUTH_HEADER,
    )
    assert environments[0]["id"] == "932fb819-90c0-4d03-918d-bc6fc20cd545"


def test_publish_environment_success(monkeypatch: MonkeyPatch, auth: MagicMock) -> None:
    # Arrange
    mock_response = mocked_response()
    mock_request = mocked_request(mock_response)
    monkeypatch.setattr(requests, "post", mock_request)

    # Act
    publish_environment(workspace_id="workspace-id", environment_id="environment-id", auth=auth)

    # Assert
    mock_request.assert_called_once_with(
        "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/environments/environment-id/staging/publish",  # noqa: E501
        headers=AUTH_HEADER,
    )


def test_list_staging_libraries_success(monkeypatch: MonkeyPatch, auth: MagicMock) -> None:
    # Arrange
    mock_response = mocked_response(
        return_value={
            "customLibraries": {
                "wheelFiles": ["fabriccli-0.0.1-py3-none-any.whl"],
                "pyFiles": [],
                "jarFiles": [],
                "rTarFiles": [],
            },
            "environmentYml": "",
        }
    )
    mock_request = mocked_request(mock_response)
    monkeypatch.setattr(requests, "get", mock_request)

    # Act
    staging_libraries = list_staging_libraries(
        workspace_id="workspace-id", environment_id="environment-id", auth=auth
    )

    # Assert
    mock_request.assert_called_once_with(
        "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/environments/environment-id/staging/libraries",  # noqa: E501
        headers=AUTH_HEADER,
    )
    assert staging_libraries["customLibraries"]["wheelFiles"] == [
        "fabriccli-0.0.1-py3-none-any.whl"
    ]


def test_delete_staging_library_success(monkeypatch: MonkeyPatch, auth: MagicMock) -> None:
    # Arrange
    mock_response = mocked_response()
    mock_request = mocked_request(mock_response)
    monkeypatch.setattr(requests, "delete", mock_request)

    # Act
    delete_staging_library(
        workspace_id="workspace-id",
        environment_id="environment-id",
        library_name="fabriccli-0.0.1-py3-none-any.whl",
        auth=auth,
    )

    # Assert
    mock_request.assert_called_once_with(
        "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/environments/environment-id/staging/libraries",  # noqa: E501
        params={"libraryToDelete": "fabriccli-0.0.1-py3-none-any.whl"},
        headers=AUTH_HEADER,
    )


def test_delete_python_package_wheels_success(monkeypatch: MonkeyPatch, auth: MagicMock) -> None:
    # Arrange
    mock_staging_library_list = MagicMock()
    mock_staging_library_list.return_value = {
        "customLibraries": {
            "wheelFiles": ["fabriccli-0.0.1-py3-none-any.whl"],
            "pyFiles": [],
            "jarFiles": [],
            "rTarFiles": [],
        },
        "environmentYml": "",
    }
    monkeypatch.setattr("fabric_cli.environment.list_staging_libraries", mock_staging_library_list)

    mock_staging_library_delete = MagicMock()
    monkeypatch.setattr(
        "fabric_cli.environment.delete_staging_library", mock_staging_library_delete
    )

    # Act
    delete_python_package_wheels(
        workspace_id="workspace-id",
        environment_id="environment-id",
        package_name="fabriccli",
        auth=auth,
    )

    # Assert
    mock_staging_library_delete.assert_called_once_with(
        "workspace-id",
        "environment-id",
        "fabriccli-0.0.1-py3-none-any.whl",
        auth,
    )


def test_upload_staging_library_success(monkeypatch: MonkeyPatch, auth: MagicMock) -> None:
    # Arrange
    mock_read = MagicMock()
    monkeypatch.setattr(builtins, "open", mock_read)

    mock_response = mocked_response()
    mock_request = mocked_request(mock_response)
    monkeypatch.setattr(requests, "post", mock_request)

    # Act
    upload_staging_library(
        workspace_id="workspace-id",
        environment_id="environment-id",
        library_path="path/to/library-0.0.1-py3-none-any.whl",
        auth=auth,
    )

    # Assert
    mock_read.assert_called_once_with(
        "path/to/library-0.0.1-py3-none-any.whl",
        "rb",
    )

    assert len(mock_request.call_args_list) == 1
    request_args, request_kwargs = mock_request.call_args_list[0]
    assert request_args == (
        "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/environments/environment-id/staging/libraries",  # noqa: E501
    )
    assert request_kwargs["files"]["file"][0] == "library-0.0.1-py3-none-any.whl"
    assert request_kwargs["headers"] == AUTH_HEADER

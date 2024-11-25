import unittest
import requests
from unittest.mock import patch, MagicMock
from fabric_cli.workspaces import create_workspace, get_workspaces
from fabric_cli.auth import Auth


class TestWorkspaces(unittest.TestCase):
    """
    Test cases for the workspace functions in workspaces.py.
    """

    @patch("fabric_cli.workspaces.requests.post")
    def test_create_workspace_success(self, mock_post):
        """
        Test the successful creation of a workspace without a capacity ID.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"Location": "https://api.fabric.microsoft.com/v1/workspaces/12345"}
        mock_post.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function
        workspace_id = create_workspace("Test Workspace", mock_auth)

        # Assertions
        self.assertEqual(workspace_id, "12345")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/",
            json={"displayName": "Test Workspace"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.workspaces.requests.post")
    def test_create_workspace_with_capacity_success(self, mock_post):
        """
        Test the successful creation of a workspace with a capacity ID.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"Location": "https://api.fabric.microsoft.com/v1/workspaces/12345"}
        mock_post.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function
        workspace_id = create_workspace("Test Workspace", mock_auth, "capacity-id")

        # Assertions
        self.assertEqual(workspace_id, "12345")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/",
            json={"displayName": "Test Workspace", "capacityId": "capacity-id"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.workspaces.requests.post")
    def test_create_workspace_failure(self, mock_post):
        """
        Test the failure case where the API request raises an HTTPError.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error")
        mock_post.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function and assert exception
        with self.assertRaises(requests.exceptions.HTTPError):
            create_workspace("Test Workspace", mock_auth)

        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/",
            json={"displayName": "Test Workspace"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.workspaces.requests.get")
    def test_get_workspaces_success(self, mock_get):
        """
        Test the successful retrieval of workspaces.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "value": [
                {"id": "12345", "displayName": "Workspace 1", "capacityId": "capacity-1"},
                {"id": "67890", "displayName": "Workspace 2", "capacityId": "capacity-2"},
            ]
        }
        mock_get.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function
        workspaces = get_workspaces(mock_auth)

        # Assertions
        self.assertEqual(
            workspaces,
            [("12345", "Workspace 1", "capacity-1"), ("67890", "Workspace 2", "capacity-2")],
        )
        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces",
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.workspaces.requests.get")
    def test_get_workspaces_failure(self, mock_get):
        """
        Test the failure case where the API request raises an HTTPError.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Error")
        mock_get.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function and assert exception
        with self.assertRaises(requests.exceptions.HTTPError):
            get_workspaces(mock_auth)

        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces",
            headers={"Authorization": "Bearer token"},
        )


if __name__ == "__main__":
    unittest.main()

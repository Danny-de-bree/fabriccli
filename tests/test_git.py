import unittest
import requests
from unittest.mock import patch, MagicMock
from fabric_cli.git import connect_git_repository
from fabric_cli.auth import Auth


class TestGit(unittest.TestCase):
    """
    Test cases for the connect_git_repository function in git.py.
    """

    @patch("fabric_cli.git.requests.post")
    def test_connect_git_repository_success(self, mock_post):
        """
        Test the successful connection of a workspace to a Git repository.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Define the git provider details
        git_provider_details = {
            "organizationName": "Test Organization",
            "projectName": "Test Project",
            "gitProviderType": "AzureDevOps",
            "repositoryName": "Test Repo",
            "branchName": "Test Branch",
            "directoryName": "Test Directory",
        }

        # Call the function
        connect_git_repository("workspace-id", git_provider_details, mock_auth)

        # Assertions
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/git/connect",
            json={"gitProviderDetails": git_provider_details},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.git.requests.post")
    def test_connect_git_repository_failure(self, mock_post):
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

        # Define the git provider details
        git_provider_details = {
            "organizationName": "Test Organization",
            "projectName": "Test Project",
            "gitProviderType": "AzureDevOps",
            "repositoryName": "Test Repo",
            "branchName": "Test Branch",
            "directoryName": "Test Directory",
        }

        # Call the function and assert exception
        with self.assertRaises(requests.exceptions.HTTPError):
            connect_git_repository("workspace-id", git_provider_details, mock_auth)

        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/git/connect",
            json={"gitProviderDetails": git_provider_details},
            headers={"Authorization": "Bearer token"},
        )


if __name__ == "__main__":
    unittest.main()

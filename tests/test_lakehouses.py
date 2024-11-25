import unittest
import requests
from unittest.mock import patch, MagicMock
from fabric_cli.lakehouses import create_lakehouse, get_lakehouses
from fabric_cli.auth import Auth


class TestLakehouses(unittest.TestCase):
    """
    Test cases for the lakehouse functions in lakehouses.py.
    """

    @patch("fabric_cli.lakehouses.requests.post")
    def test_create_lakehouse_success(self, mock_post):
        """
        Test the successful creation of a lakehouse.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "12345"}
        mock_post.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function
        lakehouse_id = create_lakehouse("workspace-id", "Test Lakehouse", mock_auth)

        # Assertions
        self.assertEqual(lakehouse_id, "12345")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/lakehouses",
            json={"displayName": "Test Lakehouse"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.lakehouses.requests.post")
    def test_create_lakehouse_failure(self, mock_post):
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
            create_lakehouse("workspace-id", "Test Lakehouse", mock_auth)

        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/lakehouses",
            json={"displayName": "Test Lakehouse"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.lakehouses.requests.get")
    def test_get_lakehouses_success(self, mock_get):
        """
        Test the successful retrieval of lakehouses.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "value": [
                {"id": "12345", "displayName": "Lakehouse 1"},
                {"id": "67890", "displayName": "Lakehouse 2"},
            ]
        }
        mock_get.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function
        lakehouses = get_lakehouses("workspace-id", mock_auth)

        # Assertions
        self.assertEqual(lakehouses, [("12345", "Lakehouse 1"), ("67890", "Lakehouse 2")])
        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/lakehouses",
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.lakehouses.requests.get")
    def test_get_lakehouses_failure(self, mock_get):
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
            get_lakehouses("workspace-id", mock_auth)

        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/lakehouses",
            headers={"Authorization": "Bearer token"},
        )


if __name__ == "__main__":
    unittest.main()

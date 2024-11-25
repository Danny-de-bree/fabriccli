import unittest
import requests
from unittest.mock import patch, MagicMock
from fabric_cli.warehouses import create_warehouse, get_warehouses
from fabric_cli.auth import Auth


class TestWarehouses(unittest.TestCase):
    """
    Test cases for the warehouse functions in warehouses.py.
    """

    @patch("fabric_cli.warehouses.requests.post")
    def test_create_warehouse_success(self, mock_post):
        """
        Test the successful creation of a warehouse.
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
        warehouse_id = create_warehouse("workspace-id", "Test Warehouse", mock_auth)

        # Assertions
        self.assertEqual(warehouse_id, "12345")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/warehouses",
            json={"displayName": "Test Warehouse"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.warehouses.requests.post")
    def test_create_warehouse_failure(self, mock_post):
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
            create_warehouse("workspace-id", "Test Warehouse", mock_auth)

        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/warehouses",
            json={"displayName": "Test Warehouse"},
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.warehouses.requests.get")
    def test_get_warehouses_success(self, mock_get):
        """
        Test the successful retrieval of warehouses.
        """
        # Mock the response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "value": [
                {"id": "12345", "displayName": "Warehouse 1"},
                {"id": "67890", "displayName": "Warehouse 2"},
            ]
        }
        mock_get.return_value = mock_response

        # Mock the Auth instance
        mock_auth = MagicMock(spec=Auth)
        mock_auth.get_headers.return_value = {"Authorization": "Bearer token"}

        # Call the function
        warehouses = get_warehouses("workspace-id", mock_auth)

        # Assertions
        self.assertEqual(warehouses, [("12345", "Warehouse 1"), ("67890", "Warehouse 2")])
        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/warehouses",
            headers={"Authorization": "Bearer token"},
        )

    @patch("fabric_cli.warehouses.requests.get")
    def test_get_warehouses_failure(self, mock_get):
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
            get_warehouses("workspace-id", mock_auth)

        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/workspace-id/warehouses",
            headers={"Authorization": "Bearer token"},
        )


if __name__ == "__main__":
    unittest.main()

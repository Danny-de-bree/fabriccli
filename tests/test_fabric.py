import unittest
from unittest.mock import patch, MagicMock
from fabric_cli.auth import Auth
from fabric_cli.fabric import (
    create_workspace,
    get_workspaces,
    provision_workspace_identity,
    assign_workspace_to_capacity,
    create_lakehouse,
    get_lakehouses,
    create_warehouse,
    get_warehouses,
)

class TestFabric(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()
        self.auth.set_token("test_token")

    @patch("fabric_cli.fabric.requests.post")
    def test_create_workspace(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.headers = {"Location": "https://api.fabric.microsoft.com/v1/workspaces/12345"}
        mock_post.return_value = mock_response

        workspace_id = create_workspace("Test Workspace", self.auth)
        self.assertEqual(workspace_id, "12345")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/",
            json={"displayName": "Test Workspace"},
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.get")
    def test_get_workspaces(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "value": [
                {"id": "12345", "displayName": "Test Workspace", "capacityId": "67890"}
            ]
        }
        mock_get.return_value = mock_response

        workspaces = get_workspaces(self.auth)
        self.assertEqual(workspaces, [("12345", "Test Workspace", "67890")])
        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces",
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.post")
    def test_provision_workspace_identity(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = provision_workspace_identity("12345", self.auth)
        self.assertTrue(result)
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/12345/provisionIdentity",
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.post")
    def test_assign_workspace_to_capacity(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = assign_workspace_to_capacity("12345", "67890", self.auth)
        self.assertTrue(result)
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/12345/assignToCapacity",
            json={"capacityId": "67890"},
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.post")
    def test_create_lakehouse(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "lakehouse123"}
        mock_post.return_value = mock_response

        lakehouse_id = create_lakehouse("12345", "Test Lakehouse", self.auth)
        self.assertEqual(lakehouse_id, "lakehouse123")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/12345/lakehouses",
            json={"displayName": "Test Lakehouse"},
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.get")
    def test_get_lakehouses(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "value": [
                {"id": "lakehouse123", "displayName": "Test Lakehouse"}
            ]
        }
        mock_get.return_value = mock_response

        lakehouses = get_lakehouses("12345", self.auth)
        self.assertEqual(lakehouses, [("lakehouse123", "Test Lakehouse")])
        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/12345/lakehouses",
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.post")
    def test_create_warehouse(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"id": "warehouse123"}
        mock_post.return_value = mock_response

        warehouse_id = create_warehouse("12345", "Test Warehouse", self.auth)
        self.assertEqual(warehouse_id, "warehouse123")
        mock_post.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/12345/warehouses",
            json={"displayName": "Test Warehouse"},
            headers=self.auth.get_headers()
        )

    @patch("fabric_cli.fabric.requests.get")
    def test_get_warehouses(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "value": [
                {"id": "warehouse123", "displayName": "Test Warehouse"}
            ]
        }
        mock_get.return_value = mock_response

        warehouses = get_warehouses("12345", self.auth)
        self.assertEqual(warehouses, [("warehouse123", "Test Warehouse")])
        mock_get.assert_called_once_with(
            "https://api.fabric.microsoft.com/v1/workspaces/12345/warehouses",
            headers=self.auth.get_headers()
        )

if __name__ == "__main__":
    unittest.main()
import unittest
import os
from fabric_cli.auth import Auth

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.auth = Auth()
        self.test_token = "test_token"
        # Clear any existing token
        Auth._token = None
        if "POWER_BI_ACCESS_TOKEN" in os.environ:
            del os.environ["POWER_BI_ACCESS_TOKEN"]

    def tearDown(self):
        # Clean up environment variable after each test
        if "POWER_BI_ACCESS_TOKEN" in os.environ:
            del os.environ["POWER_BI_ACCESS_TOKEN"]

    def test_set_token(self):
        self.auth.set_token(self.test_token)
        self.assertEqual(self.auth.get_access_token(), self.test_token)

    def test_get_access_token_from_env(self):
        os.environ["POWER_BI_ACCESS_TOKEN"] = self.test_token
        self.assertEqual(self.auth.get_access_token(), self.test_token)

    def test_get_headers(self):
        self.auth.set_token(self.test_token)
        headers = self.auth.get_headers()
        self.assertEqual(headers["Authorization"], f"Bearer {self.test_token}")
        self.assertEqual(headers["Content-Type"], "application/json")

if __name__ == "__main__":
    unittest.main()
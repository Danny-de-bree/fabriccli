from typing import Any
import pytest
from unittest.mock import MagicMock

AUTH_HEADER = {"Authorization": "Bearer token"}


@pytest.fixture
def auth() -> MagicMock:
    mock_auth = MagicMock()
    mock_auth.get_headers.return_value = AUTH_HEADER
    return mock_auth


def mocked_request(mock_response: MagicMock) -> MagicMock:
    mock_request = MagicMock()
    mock_request.return_value = mock_response
    return mock_request


def mocked_response(return_value: Any = {}) -> MagicMock:
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = return_value
    return mock_response

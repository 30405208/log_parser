import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_questionary_select():
    # Patch questionary.select().ask() to always return "Everything"
    with patch('questionary.select') as mock_select:
        mock_select.return_value.ask.return_value = "Everything"
        yield mock_select
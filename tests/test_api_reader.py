import pytest
from unittest.mock import patch, MagicMock
from task.connectors.ratefetchers.api_reader import ApiRatesReader
from task.utils.exceptions import NotFoundInApiError

API_BASE_URL = "https://api.nbp.pl/api/exchangerates/rates/"


@pytest.fixture
def api_rates_reader():
    return ApiRatesReader(table="A")


def test_get_rate_by_currency_success(api_rates_reader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "rates": [
            {"effectiveDate": "2023-06-30", "mid": 4.20},
            {"effectiveDate": "2023-07-01", "mid": 4.22},
        ]
    }

    with patch("requests.get", return_value=mock_response) as mock_get:
        rate = api_rates_reader.get_rate_by_currency("USD")
        mock_get.assert_called_once_with(
            "https://api.nbp.pl/api/exchangerates/rates/A/USD"
        )
        assert rate == 4.22


def test_get_rate_by_currency_not_found(api_rates_reader):
    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(NotFoundInApiError) as exc:
            api_rates_reader.get_rate_by_currency("USD")
        mock_get.assert_called_once_with(
            "https://api.nbp.pl/api/exchangerates/rates/A/USD"
        )
        assert str(exc.value) == "Could not find rate for USD"


def test_get_rate_by_currency_invalid_response(api_rates_reader):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"invalid": "data"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        with pytest.raises(KeyError):
            api_rates_reader.get_rate_by_currency("USD")
        mock_get.assert_called_once_with(
            "https://api.nbp.pl/api/exchangerates/rates/A/USD"
        )

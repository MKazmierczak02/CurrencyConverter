import json
import pytest
from unittest.mock import patch, mock_open
from task.connectors.ratefetchers.file_reader import LocalCurrencyRatesReader
from task.utils.exceptions import RateNotFoundError

LOCAL_CURRENCY_RATES_FNAME = "test_rates.json"


@pytest.fixture
def mock_rates_data():
    return {
        "USD": [
            {"date": "2023-06-30", "rate": 4.20},
            {"date": "2023-07-01", "rate": 4.22},
        ],
        "EUR": [
            {"date": "2023-06-30", "rate": 4.50},
            {"date": "2023-07-01", "rate": 4.55},
        ],
    }


@pytest.fixture
def mock_open_file(mock_rates_data):
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_rates_data))):   # noqa E501
        with patch("task.connectors.ratefetchers.file_reader.LOCAL_CURRENCY_RATES_FNAME",  # noqa E501
                   new_callable=lambda: "test_rates.json"):
            yield


def test_get_rate_by_currency_success(mock_open_file):
    reader = LocalCurrencyRatesReader()
    rate = reader.get_rate_by_currency("USD")
    assert rate == 4.22


def test_get_rate_by_currency_not_found(mock_open_file):
    reader = LocalCurrencyRatesReader()
    with pytest.raises(RateNotFoundError) as excinfo:
        reader.get_rate_by_currency("GBP")
    assert str(excinfo.value) == (
        "Error: Rate for GBP not found. "
        "Try to use different source or update the currency rates file."
    )


def test_refresh(mock_open_file, mock_rates_data):
    reader = LocalCurrencyRatesReader()
    assert reader._data == mock_rates_data
    new_data = {
        "USD": [
            {"date": "2023-06-30", "rate": 4.20},
            {"date": "2023-07-01", "rate": 4.25},
        ]
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(new_data))):
        reader.refresh()
        assert reader._data == new_data
        rate = reader.get_rate_by_currency("USD")
        assert rate == 4.25

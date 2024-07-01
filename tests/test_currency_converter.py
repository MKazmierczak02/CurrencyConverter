import pytest
from unittest.mock import patch
from datetime import datetime
from task.currency_converter import PriceCurrencyConverterToPLN
from task.entity.converted_price_pln import ConvertedPricePLN

MOCK_DATETIME = datetime(2024, 7, 1)


@pytest.fixture
def mock_datetime_now(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return MOCK_DATETIME

    monkeypatch.setattr("datetime.datetime", MockDateTime)


@pytest.fixture
def converted_price_instance():
    return ConvertedPricePLN(
        currency="USD",
        rate=4.0,
        date=MOCK_DATETIME.strftime("%Y-%m-%d"),
        price_in_pln=40.0,
    )


def test_convert_to_pln_api_source(mock_datetime_now):
    with patch(
        "task.connectors.ratefetchers.api_reader.ApiRatesReader"
    ) as MockApiReader, patch(
        "task.connectors.ratefetchers.file_reader.LocalCurrencyRatesReader"
    ):
        mock_api_reader = MockApiReader.return_value
        mock_api_reader.get_rate_by_currency.return_value = 4.0

        converter = PriceCurrencyConverterToPLN(data_source="api")
        result = converter.convert_to_pln(currency="USD", price=10.0)

        assert result.currency == "USD"
        assert result.rate == 4.0
        assert result.price_in_pln == 40.0
        assert result.date == MOCK_DATETIME.strftime("%Y-%m-%d")


def test_convert_to_pln_local_source(mock_datetime_now):
    with patch("task.connectors.ratefetchers.api_reader.ApiRatesReader"), patch(  # noqa E501
        "task.connectors.ratefetchers.file_reader.LocalCurrencyRatesReader"
    ) as MockLocalReader:
        mock_local_reader = MockLocalReader.return_value
        mock_local_reader.get_rate_by_currency.return_value = 3.5

        converter = PriceCurrencyConverterToPLN(data_source="local")
        result = converter.convert_to_pln(currency="EUR", price=20.0)

        assert result.currency == "EUR"
        assert result.rate == 3.5
        assert result.price_in_pln == 70.0
        assert result.date == MOCK_DATETIME.strftime("%Y-%m-%d")


def test_check_exchange_rate_api(mock_datetime_now):
    with patch(
        "task.connectors.ratefetchers.api_reader.ApiRatesReader"
    ) as MockApiReader:
        mock_api_reader = MockApiReader.return_value
        mock_api_reader.get_rate_by_currency.return_value = 4.0

        converter = PriceCurrencyConverterToPLN(data_source="api")
        rate = converter._check_exchange_rate("USD")

        assert rate == 4.0


def test_check_exchange_rate_local(mock_datetime_now):
    with patch(
        "task.connectors.ratefetchers.file_reader.LocalCurrencyRatesReader"
    ) as MockLocalReader:
        mock_local_reader = MockLocalReader.return_value
        mock_local_reader.get_rate_by_currency.return_value = 3.5

        converter = PriceCurrencyConverterToPLN(data_source="local")
        rate = converter._check_exchange_rate("EUR")

        assert rate == 3.5

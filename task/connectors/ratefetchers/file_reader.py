import json

from ...config import LOCAL_CURRENCY_RATES_FNAME
from .base_reader import BaseRatesReader
from ...utils.exceptions import RateNotFoundError


class LocalCurrencyRatesReader(BaseRatesReader):
    def __init__(self):
        self._data = self._read()

    def _read(self) -> dict:
        with open(LOCAL_CURRENCY_RATES_FNAME) as file:
            return json.load(file)

    def get_rate_by_currency(self, currency: str) -> float:
        """
        :param currency: currency code
        :param currency:
        :return:
        """
        self.refresh()
        rates = self._data.get(currency.upper(), None)
        if not rates:
            raise RateNotFoundError(
                f"Error: Rate for {currency} not found. Try to use different "
                f"source or update the currency rates file."
            )
        rate = self._get_latest(rates, date_field="date", rate_field="rate")
        return rate

    def refresh(self) -> None:
        self._data = self._read()

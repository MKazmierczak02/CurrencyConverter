from abc import ABC, abstractmethod
from datetime import datetime


class BaseRatesReader(ABC):
    @abstractmethod
    def get_rate_by_currency(self, currency: str) -> float:
        """
        Get rate by currency.
        :param currency: currency code
        :return:
        """
        pass

    def _get_latest(self, rates, date_field: str, rate_field: str) -> float:
        """
        Gets the latest rate for the specified currency.
        :param rates:
        :param date_field:
        :param rate_field:
        :return:
        """
        rates_sorted = sorted(
            rates,
            key=lambda x: datetime.strptime(x[date_field], "%Y-%m-%d"),
            reverse=True,
        )
        return rates_sorted[0][rate_field]

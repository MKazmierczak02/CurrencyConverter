import requests

from ...config import API_BASE_URL
from .base_reader import BaseRatesReader
from ...utils.exceptions import NotFoundInApiError


class ApiRatesReader(BaseRatesReader):

    def __init__(self, table="A"):
        self.table = table

    def get_rate_by_currency(self, currency: str) -> float:
        """
        Get rate from api by currency.
        :param currency:
        :return:
        """
        api_url = f"{API_BASE_URL}{self.table}/{currency}"
        response = requests.get(api_url)
        if response.status_code == 200:
            rates = response.json()["rates"]
        else:
            raise NotFoundInApiError(f"Could not find rate for {currency}")
        rate = self._get_latest(rates, date_field="effectiveDate", rate_field="mid")
        return rate

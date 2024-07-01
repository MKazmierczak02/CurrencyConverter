from datetime import datetime
from .entity.converted_price_pln import ConvertedPricePLN


class PriceCurrencyConverterToPLN:

    def __init__(self, data_source):
        self.data_source = data_source

    def _check_exchange_rate(self, currency) -> float:
        if self.data_source == "api":
            from .connectors.ratefetchers.api_reader import ApiRatesReader

            currency_rates_reader = ApiRatesReader()
        elif self.data_source == "local":
            from .connectors.ratefetchers.file_reader import LocalCurrencyRatesReader

            currency_rates_reader = LocalCurrencyRatesReader()
        rate = currency_rates_reader.get_rate_by_currency(currency)
        return rate

    def convert_to_pln(self, *, currency: str, price: float) -> ConvertedPricePLN:
        exchange_rate = self._check_exchange_rate(currency)
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")
        converted_price = ConvertedPricePLN(
            currency=currency,
            rate=exchange_rate,
            price_in_pln=price * exchange_rate,
            date=formatted_date,
        )
        return converted_price

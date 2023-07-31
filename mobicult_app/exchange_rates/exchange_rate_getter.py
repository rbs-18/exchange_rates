import json
from collections.abc import Sequence

import requests
from django.core.cache import cache

from .days import Days


class ExchangeRateGetter:
    """Класс для получения курса валют.

    Attributes:
        _base: базовая валюта
        _target_currency: валюты перевода
        _data: данные по стоимости
    Notes:
        документация на сервис:
            https://apilayer.com/marketplace/fixer-api#documentation-tab
    """

    URL = 'https://api.apilayer.com/fixer/timeseries'
    APIKEY = 'T8cvUe57l9M6JbXgC15AwQqyvoqC25g3'  # TODO надо будет спрятать

    def __init__(self, target_currency: Sequence, base_currency: str = 'RUB'):
        self._base = base_currency
        self._symbols = target_currency
        self._data = {
            Days.DAY_BEFORE_YESTERDAY: {},
            Days.YESTERDAY: {},
            Days.TODAY: {},
        }
        self.days = Days()

    def load_currency_data(self):
        result = cache.get('data')

        try:
            self._data = json.loads(result)
        except TypeError:
            headers = {'apikey': self.APIKEY}
            payload = {
                'base': self._base,
                'symbols': self._get_symbols(),
                'start_date': self.days.day_before_yesterday,
                'end_date': self.days.today,
            }
            response = requests.get(self.URL, params=payload, headers=headers)
            self._write_data(data=response.json())

    def _write_data(self, data):
        if data['success']:
            for day, rates in zip(self._data, data['rates'].values()):
                for currency, value in rates.items():
                    rates[currency] = round(1 / value, 2)
                self._data[day] = rates
            cache.set('data', value=json.dumps(self._data), timeout=60*60*24)
            return

        raise ValueError(data['error']['info'])

    def _get_symbols(self):
        if isinstance(self._symbols, str):
            return self._symbols
        return ','.join(self._symbols)

    def get_today_rate(self) -> dict[str, float]:
        return self._data[Days.TODAY]

    def get_yesterday_rate(self) -> dict[str, float]:
        return self._data[Days.YESTERDAY]

    def get_day_before_yesterday_rate(self) -> dict[str, float]:
        return self._data[Days.DAY_BEFORE_YESTERDAY]

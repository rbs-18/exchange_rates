from collections.abc import Sequence
from datetime import datetime, timedelta

import requests


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

    URL ='https://api.apilayer.com/fixer/timeseries'
    APIKEY = 'T8cvUe57l9M6JbXgC15AwQqyvoqC25g3'

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
                    rates[currency] =  round(1 / value, 2)
                self._data[day] = rates
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


class Days:
    DAY_BEFORE_YESTERDAY = 'day_before_yesterday'
    YESTERDAY = 'yesterday'
    TODAY = 'today'

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self):
        self._today = datetime.now()
        self._yesterday = self._today - timedelta(days=1)
        self._day_before_yesterday = self._today - timedelta(days=2)

    @property
    def today(self) -> str:
        return self._today.strftime(self.DATE_FORMAT)

    @property
    def yesterday(self) -> str:
        return self._yesterday.strftime(self.DATE_FORMAT)

    @property
    def day_before_yesterday(self) -> str:
        return self._day_before_yesterday.strftime(self.DATE_FORMAT)

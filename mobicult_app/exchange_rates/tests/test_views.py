from http import HTTPStatus
import requests
from django.test import Client, TestCase
from django.urls import reverse

from ..days import Days
from ..exchange_rate_getter import ExchangeRateGetter


class ExchangeRatesPagesTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        headers = {'apikey': ExchangeRateGetter.APIKEY}
        payload = {
            'base': 'RUB',
            'symbols': 'EUR,USD',
            'start_date': Days.day_before_yesterday,
            'end_date': Days.today,
        }
        cls.response = requests.get(
            'https://api.apilayer.com/fixer/timeseries',
            params=payload,
            headers=headers,
        )
        cls.response.status_code
        cls.data = cls.response.json()

    def setUp(self):
        self.client = Client()

    def test_service(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)

    def test_content(self):
        for url in (
            reverse('exchange_rates:index'),
            reverse('exchange_rates:yesterday'),
            reverse('exchange_rates:day_before_yesterday'),
        ):
            response = self.client.get(url)
            self.assertTrue(response.context.get('active_page'))
            self.assertTrue(response.context.get('today'))
            self.assertTrue(response.context.get('yesterday'))
            self.assertTrue(response.context.get('day_before_yesterday'))
            self.assertTrue(response.context.get('USD'))
            self.assertTrue(response.context.get('EUR'))

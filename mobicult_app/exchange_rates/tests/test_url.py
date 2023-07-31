from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_urls_get_correct_status(self):
        urls_status_code = {
            reverse('exchange_rates:index'): HTTPStatus.OK,
            reverse('exchange_rates:yesterday'): HTTPStatus.OK,
            reverse('exchange_rates:day_before_yesterday'): HTTPStatus.OK,
        }

        for url, status_code in urls_status_code.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status_code)

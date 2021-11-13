import unittest
from CurrencyClient import CurrencyClient
from unittest import IsolatedAsyncioTestCase
import asyncio


class TestCurrencyClientPositive(IsolatedAsyncioTestCase):
    correct_access_key = 'a899a63095452f4c92d59970b7ff4884'
    correct_base_currency = 'EUR'
    currency_client = None
    second_currency_client = None

    def setUp(self) -> None:
        TestCurrencyClientPositive.currency_client = CurrencyClient(seconds=60)
        TestCurrencyClientPositive.second_currency_client = CurrencyClient(seconds=60)
        print('Test Case Setup Completed')

    def testCaching(self):
        TestCurrencyClientPositive.currency_client.set_access_key(TestCurrencyClientPositive.correct_access_key) \
            .set_base_currency(TestCurrencyClientPositive.correct_base_currency).set_interval(seconds=10)
        TestCurrencyClientPositive.currency_client.get_currency('USD')
        TestCurrencyClientPositive.currency_client.get_currency('USD')
        event = TestCurrencyClientPositive.currency_client.get_last_event()
        cache_event = TestCurrencyClientPositive.currency_client.get_last_cache_event()
        self.assertEqual('http://api.exchangeratesapi.io/v1/latest - GET - 200', event)
        self.assertEqual('Get cached data of USD', cache_event)

    async def testInterval(self):
        TestCurrencyClientPositive.currency_client.set_access_key(TestCurrencyClientPositive.correct_access_key) \
            .set_base_currency(TestCurrencyClientPositive.correct_base_currency).set_interval(seconds=5)
        asyncio.create_task(TestCurrencyClientPositive.currency_client.get_currency_periodically('USD'))
        await asyncio.sleep(11)
        self.assertEqual(3, TestCurrencyClientPositive.currency_client.get_amount_of_events())
        await asyncio.sleep(11)
        self.assertEqual(5, TestCurrencyClientPositive.currency_client.get_amount_of_events())

    async def testIntervalTwoCurrencies(self):
        TestCurrencyClientPositive.currency_client.set_access_key(TestCurrencyClientPositive.correct_access_key) \
            .set_base_currency(TestCurrencyClientPositive.correct_base_currency).set_interval(seconds=4)
        asyncio.create_task(TestCurrencyClientPositive.currency_client.get_currency_periodically('USD'))
        asyncio.create_task(TestCurrencyClientPositive.currency_client.get_currency_periodically('PLN'))
        await asyncio.sleep(11)
        self.assertEqual(6, TestCurrencyClientPositive.currency_client.get_amount_of_events())
        await asyncio.sleep(12)
        self.assertEqual(12, TestCurrencyClientPositive.currency_client.get_amount_of_events())

    async def testIntervalTwoCurrenciesTwoClients(self):
        TestCurrencyClientPositive.currency_client.set_access_key(TestCurrencyClientPositive.correct_access_key) \
            .set_base_currency(TestCurrencyClientPositive.correct_base_currency).set_interval(seconds=2)
        TestCurrencyClientPositive.second_currency_client.set_access_key(TestCurrencyClientPositive.correct_access_key) \
            .set_base_currency(TestCurrencyClientPositive.correct_base_currency).set_interval(seconds=3)
        asyncio.create_task(TestCurrencyClientPositive.currency_client.get_currency_periodically('USD'))
        asyncio.create_task(TestCurrencyClientPositive.second_currency_client.get_currency_periodically('PLN'))
        await asyncio.sleep(9)
        self.assertEqual(4, TestCurrencyClientPositive.currency_client.get_amount_of_events())
        self.assertEqual(3, TestCurrencyClientPositive.second_currency_client.get_amount_of_events())
        await asyncio.sleep(3)
        self.assertEqual(6, TestCurrencyClientPositive.currency_client.get_amount_of_events())
        self.assertEqual(4, TestCurrencyClientPositive.second_currency_client.get_amount_of_events())

    async def testCachingAndInterval(self):
        TestCurrencyClientPositive.currency_client.set_access_key(TestCurrencyClientPositive.correct_access_key) \
            .set_base_currency(TestCurrencyClientPositive.correct_base_currency).set_interval(seconds=4)
        TestCurrencyClientPositive.currency_client.get_currency('CAD')
        TestCurrencyClientPositive.currency_client.get_currency('CAD')
        event = TestCurrencyClientPositive.currency_client.get_last_event()
        cache_event = TestCurrencyClientPositive.currency_client.get_last_cache_event()
        self.assertEqual('http://api.exchangeratesapi.io/v1/latest - GET - 200', event)
        self.assertEqual('Get cached data of CAD', cache_event)
        asyncio.create_task(TestCurrencyClientPositive.currency_client.get_currency_periodically('CAD'))
        await asyncio.sleep(5)
        TestCurrencyClientPositive.currency_client.get_currency('CAD')
        self.assertEqual(3, TestCurrencyClientPositive.currency_client.get_amount_of_events())
        self.assertEqual(2, TestCurrencyClientPositive.currency_client.get_amount_of_cache_events())

    def tearDown(self) -> None:
        print('Tear Down Completed')

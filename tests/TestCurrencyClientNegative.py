import unittest
from CurrencyClient import CurrencyClient


class TestCurrencyClientNegative(unittest.TestCase):
    correct_access_key = 'b84d1e8f27aa924158e9372e5b9dafc0'
    incorrect_access_key = 'incorrect'
    correct_base_currency = 'EUR'
    incorrect_base_currency = 'AUD'
    currency_client = None

    def setUp(self) -> None:
        TestCurrencyClientNegative.currency_client = CurrencyClient(seconds=60)
        print('Test Case Setup Completed')

    def testIncorrectAssessKey(self):
        TestCurrencyClientNegative.currency_client.set_access_key(TestCurrencyClientNegative.incorrect_access_key) \
            .set_base_currency(TestCurrencyClientNegative.correct_base_currency).set_interval(seconds=10)
        TestCurrencyClientNegative.currency_client.get_currency('USD')
        error = TestCurrencyClientNegative.currency_client.get_last_connection_error()
        assert error == 'Invalid Access Key'

    def testIncorrectBaseCurrency(self):
        TestCurrencyClientNegative.currency_client.set_access_key(TestCurrencyClientNegative.correct_access_key) \
            .set_base_currency(TestCurrencyClientNegative.incorrect_base_currency).set_interval(seconds=10)
        TestCurrencyClientNegative.currency_client.get_currency('USD')
        error = TestCurrencyClientNegative.currency_client.get_last_connection_error()
        assert error == 'Base Currency Access Restricted'

    def testCurrencyNotInCache(self):
        TestCurrencyClientNegative.currency_client.set_access_key(TestCurrencyClientNegative.correct_access_key) \
            .set_base_currency(TestCurrencyClientNegative.correct_base_currency).set_interval(seconds=10)
        TestCurrencyClientNegative.currency_client.get_cached_currency('USD')
        error = TestCurrencyClientNegative.currency_client.get_last_cache_error()
        assert error == 'Cache does not contain currency USD'

    def tearDown(self) -> None:
        print('Tear Down Completed')

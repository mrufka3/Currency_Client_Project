import datetime
from datetime import timedelta
from CurrencyCache import CurrencyCache

import asyncio
import requests
import json


class CurrencyClient:
    __url = 'http://api.exchangeratesapi.io/v1/latest'
    __global_time_period = timedelta()

    @classmethod
    def get_global_time_period_seconds(cls):
        return CurrencyClient.__global_time_period.total_seconds()

    def __init__(self, **kwargs):
        self.__currency_cache = CurrencyCache()
        self.__cache_items = [f for f in dir(CurrencyCache) if not f.startswith('_')]
        self.__time_period = timedelta(**kwargs)
        if self.__time_period.total_seconds() > CurrencyClient.__global_time_period.total_seconds():
            CurrencyClient.__global_time_period = self.__time_period
        self.__interval = timedelta()
        self.__base_currency = ''
        self.__access_key = ''
        self.__last_connection_error = ''
        self.__event_history = []

    def __getattr__(self, item):
        def method(*args):
            if item in self.__cache_items:
                return getattr(self.__currency_cache, item)(*args)
            else:
                raise AttributeError

        return method

    def get_event(self, index):
        return self.__event_history[index]

    def get_amount_of_events(self):
        return len(self.__event_history)

    def get_last_event(self):
        return self.__event_history[-1]

    def set_access_key(self, _access_key):
        self.__access_key = _access_key
        return self

    def set_base_currency(self, _base_currency):
        self.__base_currency = _base_currency
        return self

    def get_currency(self, _currency):
        self.print_response_from_cache(_currency) if self.cached(_currency) else self.get_from_server_and_cache(_currency)
        return self.get_cached_currency(_currency)

    def get_last_connection_error(self):
        return self.__last_connection_error

    def get_from_server_and_cache(self, _currency):
        try:
            response = self.get_currency_from_server(_currency)
            self.cache_currency(response)
            self.print_response_from_server(response)
        except requests.exceptions.ConnectionError as cerr:
            self.__last_connection_error = cerr.args[0]
            print(cerr.args[0])
        except requests.exceptions.RequestException as reqerr:
            self.__last_connection_error = reqerr.args[0]
            print(reqerr.args[0])

    async def get_currency_periodically(self, _currency):
        end_time = datetime.datetime.now() + self.__time_period
        while True:
            if datetime.datetime.now() >= end_time:
                break

            self.get_from_server_and_cache(_currency)
            await asyncio.sleep(self.__interval.total_seconds())

    def print_response_from_server(self, response):
        message = response.url.split('?')[0] + ' - GET - ' + str(response.status_code)
        self.__event_history.append(message)
        print(message)
        print(json.loads(response.text)["rates"])

    def set_interval(self, **kwargs):
        self.__interval = timedelta(**kwargs)
        return self

    def get_currency_from_server(self, _currency):
        req_params = {'access_key': self.__access_key, 'base': self.__base_currency, 'symbols': _currency}
        response = requests.get(CurrencyClient.__url, params=req_params)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            raise requests.exceptions.ConnectionError('Usage Limit Reached')
        elif response.status_code == 400:
            raise requests.exceptions.RequestException('Base Currency Access Restricted')
        elif response.status_code == 401:
            raise requests.exceptions.RequestException('Invalid Access Key')
        else:
            raise requests.exceptions.ConnectionError('Other connection error occurred')

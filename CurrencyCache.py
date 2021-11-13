import json


class CurrencyCache:

    def __init__(self):
        self.__cache = dict()
        self.__last_cache_error = ''

    def cached(self, _currency):
        return _currency in self.__cache

    def get_last_cache_error(self):
        return self.__last_cache_error

    def cache_currency(self, response):
        current_currency = self.get_current_currency(response)
        self.__cache[current_currency] = response

    def get_cached_currency(self, _currency):
        if self.cached(_currency):
            return self.__cache[_currency]
        else:
            self.__last_cache_error = 'Cache does not contain currency ' + _currency
            print(self.__last_cache_error)
            return None

    def set_cached_currency(self, _currency, _value):
        self.__cache[_currency] = _value

    def print_response_from_cache(self, _currency):
        print('Get cached data of ' + _currency)
        print(json.loads(self.__cache[_currency].text)["rates"])

    @staticmethod
    def print_response_from_server(response):
        print(response.url.split('?')[0] + ' - GET - ' + str(response.status_code))
        print(json.loads(response.text)["rates"])

    @staticmethod
    def get_current_currency(response):
        keys = list(json.loads(response.text)["rates"].keys())
        return keys[0]

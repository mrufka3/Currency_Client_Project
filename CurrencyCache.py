import json


class CurrencyCache:

    def __init__(self):
        self.__cache = dict()
        self.__last_cache_error = ''
        self.__cache_event_history = []

    def get_cache_event(self, index):
        return self.__cache_event_history[index]

    def get_last_cache_event(self):
        return self.__cache_event_history[-1]

    def get_amount_of_cache_events(self):
        return len(self.__cache_event_history)

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
        message = 'Get cached data of ' + _currency
        self.__cache_event_history.append(message)
        print(message)
        print(str(json.loads(self.__cache[_currency].text)["rates"]))

    @staticmethod
    def get_current_currency(response):
        keys = list(json.loads(response.text)["rates"].keys())
        return keys[0]

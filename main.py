import asyncio

from CurrencyClient import CurrencyClient

access_key = 'b84d1e8f27aa924158e9372e5b9dafc0'
currencies = ["USD", "AUD", "CAD", "PLN", "MXN"]
base_currency = 'EUR'
time_periods = [{"seconds": 20}, {"seconds": 30}, {"seconds": 40}, {"seconds": 50}, {"seconds": 60}]
intervals = [{"seconds": 10}, {"seconds": 15}, {"seconds": 20}, {"seconds": 25}, {"seconds": 30}]
currency_clients = []


async def chain():
    for i in range(0, 5):
        currency_clients.append(CurrencyClient(**time_periods[i]))
        currency_clients[i].set_interval(**intervals[i]).set_base_currency(base_currency).set_access_key(access_key)
    for j in range(0, 5):
        asyncio.create_task(currency_clients[j].get_currency_periodically(currencies[j]))
    currency_clients[3].get_currency("USD")
    currency_clients[3].get_currency("USD")
    await asyncio.sleep(CurrencyClient.get_global_time_period_seconds())


if __name__ == '__main__':
    asyncio.run(chain())

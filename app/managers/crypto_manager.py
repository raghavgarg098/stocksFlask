from app import db
from app.models import CryptoCurrency
from app.utils import (
    cached_property,
    extract_dollar_value,
    extract_percentage_value,
    extract_market_cap,
    extract_numeric_volume,
)


class CryptoManager:
    def __init__(self, refreshed_data=[]):
        self.refreshed_data = self.refurbish_scrapper_data(refreshed_data)

    @cached_property
    def all_crypto_names(self):
        return [data.get('name') for data in self.refreshed_data if data.get('name')]

    @cached_property
    def refreshed_cryptos(self):
        return CryptoCurrency.get_by_names(self.all_crypto_names)

    @cached_property
    def crypto_name_refreshed_cryptos_map(self):
        return {crypto.name: crypto for crypto in self.refreshed_cryptos}

    @cached_property
    def refreshed_crypto_names(self):
        return [crypto.name for crypto in self.refreshed_cryptos]

    @cached_property
    def new_crypto_names(self):
        return list(set(self.all_crypto_names) - set(self.refreshed_crypto_names))

    @cached_property
    def crypto_name_crypto_data_map(self):
        return {data.get('name'): data for data in self.refreshed_data if data.get('name')}

    def refurbish_scrapper_data(self, refreshed_data):
        refurbished_data = []
        for data in refreshed_data:
            refurbished_data.append(
                {
                    'name':  data.get('name'),
                    'price': extract_dollar_value(data.get('price')),
                    'last_hour_difference':  extract_percentage_value(data.get('1h')),
                    'last_24_hour_difference': extract_percentage_value(data.get('24h')),
                    'last_7_day_difference': extract_percentage_value(data.get('7d')),
                    'market_cap': extract_market_cap(data.get('market_cap')),
                    'volume_last_24_hour': extract_numeric_volume(data.get('volume(24h)')),
                    'circulating_supply': extract_numeric_volume(data.get('circulating supply')),
                }
            )
        return refurbished_data

    def data_sync(self):
        for crypto_name in self.new_crypto_names:
            CryptoCurrency.create(**self.crypto_name_crypto_data_map.get(crypto_name))
        for crypto_name in self.refreshed_crypto_names:
            CryptoCurrency.update(self.crypto_name_refreshed_cryptos_map.get(crypto_name),
                                  **self.crypto_name_crypto_data_map.get(crypto_name))
        db.session.commit()

    @classmethod
    def get_all_cryptocurrencies(cls):
        crypto_currencies = CryptoCurrency.get_all()
        data = []
        for crypto in crypto_currencies:
            data.append(crypto.serialize())
        return data










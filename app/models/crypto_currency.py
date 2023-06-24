from sqlalchemy import desc

from .base import BaseModelMixin
from app import db


class CryptoCurrency(BaseModelMixin):
    __tablename__ = 'crypto_currency'

    name = db.Column(db.String(250), index=True, unique=True)
    price = db.Column(db.Float(precision=10, decimal_return_scale=2))
    last_hour_difference = db.Column(db.Float(precision=10, decimal_return_scale=2))
    last_24_hour_difference = db.Column(db.Float(precision=10, decimal_return_scale=2))
    last_7_day_difference = db.Column(db.Float(precision=10, decimal_return_scale=2))
    market_cap = db.Column(db.String(250))
    volume_last_24_hour = db.Column(db.String(250))
    circulating_supply = db.Column(db.String(250))

    @classmethod
    def create(cls, commit=False, **kwargs):
        crypto = CryptoCurrency()
        crypto.name = kwargs.get('name')
        crypto.price = kwargs.get('price')
        crypto.last_hour_difference = kwargs.get('last_hour_difference')
        crypto.last_24_hour_difference = kwargs.get('last_24_hour_difference')
        crypto.last_7_day_difference = kwargs.get('last_7_day_difference')
        crypto.market_cap = kwargs.get('market_cap')
        crypto.volume_last_24_hour = kwargs.get('volume_last_24_hour')
        crypto.circulating_supply = kwargs.get('circulating_supply')

        db.session.add(crypto)
        if commit:
            db.session.commit()

    @classmethod
    def update(cls, crypto, commit=False, **kwargs):
        crypto.price = kwargs.get('price')
        crypto.last_hour_difference = kwargs.get('last_hour_difference')
        crypto.last_24_hour_difference = kwargs.get('last_24_hour_difference')
        crypto.last_7_day_difference = kwargs.get('last_7_day_difference')
        crypto.market_cap = kwargs.get('market_cap')
        crypto.volume_last_24_hour = kwargs.get('volume_last_24_hour')
        crypto.circulating_supply = kwargs.get('circulating_supply')

        db.session.add(crypto)
        if commit:
            db.session.commit()

    @classmethod
    def get_by_names(cls, names_list):
        return cls.query.filter(cls.name.in_(names_list)).all()

    @classmethod
    def get_all(cls):
        return cls.query.order_by(desc(cls.updated_on)).limit(100).all()

    def serialize(self):
        return {
            'name': self.name,
            'price': self.price,
            'last_hour_difference': self.last_hour_difference,
            'last_24_hour_difference': self.last_24_hour_difference,
            'last_7_day_difference': self.last_7_day_difference,
            'market_cap': self.market_cap,
            'volume_last_24_hour': self.volume_last_24_hour,
            'circulating_supply': self.circulating_supply,
        }







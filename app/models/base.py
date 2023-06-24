import datetime
import uuid

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import UUIDType

from app import db


class BaseModelMixin(db.Model):
    __abstract__ = True

    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_on = db.Column(
        db.DateTime,
        nullable=False,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
    )
    meta = db.Column(JSON, default=dict)



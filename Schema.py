from datetime import datetime, timezone

from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from app import db
from model import Driver


class DriverSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Driver
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    firstName = fields.String(required=True)
    lastName = fields.String(required=True)
    email = fields.String(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    rate = fields.String(required=True)
    created_on = fields.DateTime(required=True, default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'))
    updated_on = fields.DateTime(required=True, default=datetime.utcnow().strftime('%B %d %Y - %H:%M:%S'))

import hashlib

from datetime import datetime
from app import db, app
from Enum import Rate
import enum

class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(80), unique=False, nullable=False)
    lastName = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    rate = db.Column(db.Enum(Rate), nullable=False)
    created_on = db.Column(db.DateTime())
    updated_on = db.Column(db.DateTime())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, firstName, lastName, email, username, password, rate, created_on, updated_on):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.username = username
        self.password = password
        self.rate = rate
        self.created_on = created_on
        self.updated_on = updated_on

    def __repr__(self):
        return '<Driver %r>' % self.id


class DriverRide(db.Model):
    __tablename__ = 'driver_ride'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'))
    driver = db.relationship("Driver", uselist=False, lazy='select')
    is_available = db.Column(db.Boolean, unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    longitude = db.Column(db.Float, unique=False, nullable=False)
    started_at = db.Column(db.DateTime(), unique=False, nullable=True)
    finished_at = db.Column(db.DateTime(), unique=False, nullable=True)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, driver_id, is_available, latitude, longitude, started_at, finished_at):
        self.driver_id = driver_id
        self.is_available = is_available
        self.latitude = latitude
        self.longitude = longitude
        self.started_at = started_at
        self.finished_at = finished_at

    def __repr__(self):
        return '<DriverRide %r>' % self.id
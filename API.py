import json
import os

from datetime import date, datetime
from flask import Flask, render_template, request, jsonify, make_response
from marshmallow import ValidationError
from pymysql import IntegrityError
from sqlalchemy.orm import load_only
from sqlalchemy.orm import defer
from sqlalchemy.orm import undefer

from Schema import DriverSchema, DriverRideSchema
from model import Driver
from app import app, db
from Connection import Connection
import hashlib


@app.route('/')
def index():
    return "Welcome to Taxii app, have a safe trip!!!"


@app.route('/driver', methods=['POST'])
def create_driver():
    data = request.get_json()
    created_on = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    updated_on = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    password = data['password']
    hash_password = hashlib.md5(password.encode())
    data['password'] = hash_password.hexdigest()
    driver_schema = DriverSchema()
    data['created_on'] = created_on
    data['updated_on'] = updated_on
    driver = driver_schema.load(data)
    result = driver_schema.dump(driver.create())
    return make_response(jsonify({"driver": result}), 200)


@app.route('/driver/<string:id>', methods=['DELETE'])
def delete_driver_by_id(id):
    get_driver = Driver.query.get(id)
    if not get_driver:
        return make_response(jsonify({"Message": "Id not found"}))
    db.session.delete(get_driver)
    db.session.commit()
    return make_response("", 204)


@app.route('/driver/<string:id>', methods=['GET'])
def getDriver(id):
    try:
        get_driver = Driver.query.get(id)
        print(get_driver)
        if not get_driver:
            return make_response(jsonify({"Message": "Id not found"}))
        driver_schema = DriverSchema()
        driver = driver_schema.dump(get_driver)
        driver.pop('password')
        return make_response(jsonify({"driver": driver}))
    except ValidationError as err:
        return err.messages, 400

@app.route('/drivers', methods=['GET'])
def alldrivers():
    get_drivers = Driver.query.all()
    driver_schema = DriverSchema(many=True)
    drivers = driver_schema.dump(get_drivers)
    for i, val in enumerate(drivers):
        drivers[i].pop('password')
    return make_response(jsonify({"drivers": drivers}))

@app.route('/driverRide', methods=['POST'])
def create_driverRide():
    data = request.get_json()
    driverRide_schema = DriverRideSchema()
    driverRide = driverRide_schema.load(data)
    result = driverRide_schema.dump(driverRide.create())
    return make_response(jsonify({"ride": result}), 200)

if __name__ == '__main__':
    app.run()

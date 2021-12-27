import json
import os

from datetime import date, datetime
from flask import Flask, render_template, request, jsonify, make_response
from marshmallow import ValidationError

from Schema import DriverSchema, DriverRideSchema
from model import Driver, DriverRide
from app import app, db
from Connection import Connection
import hashlib


@app.route('/')
def index():
    return "Welcome to Taxii app, have a safe trip!!!"


@app.route('/driver', methods=['POST'])
def create_driver():
    data = request.get_json()
    email = data['email']
    username = data['username']
    validateDriver = Driver.query.filter(Driver.email == email).first() or Driver.query.filter(Driver.username ==
                                                                                               username).first()
    if validateDriver:
        return make_response(jsonify({"Message": "Driver already exist!!!"}))
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
    result.pop('password')
    returnedResp = jsonify({"driver": result})
    return make_response(returnedResp, 200)


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


@app.route('/driver/<string:id>/password', methods=['POST'])
def change_driver_password(id):
    get_driver = Driver.query.get(id)
    if not get_driver:
        return make_response(jsonify({"Message": "Id not found"}))
    data = request.get_json()
    email = data['email']
    username = data['username']
    oldPassword = data['password']
    newPassword = data['newPassword']
    hash_oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
    hash_newPassword = hashlib.md5(newPassword.encode()).hexdigest()
    emailExist = Driver.query.filter(Driver.email == email).first() and Driver.query.filter(Driver.username == username).first()
    if not str(Driver.query.get(id).id) == id:
        return make_response(jsonify({"Error": "Id in URL doesn't match Driver Id!!!!!!"}))
    if not emailExist:
        return make_response(jsonify({"Error": "Email doesn't exist !!!!!!"}))
    else:
        isUserAndPassValid = Driver.query.filter(Driver.username == username).first() and Driver.query.filter(
            Driver.password == hash_oldPassword).first()
        if isUserAndPassValid:
            updated_on = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            result = Driver.query.filter(Driver.id == id).update({Driver.password: hash_newPassword, Driver.updated_on: updated_on})
            db.session.commit()
            if result:
                return make_response(jsonify("Password changed successfully"), 200)
            else:
                return make_response(jsonify("Password not changed successfully"), 400)
        else:
            return make_response(jsonify("User and Password doesn't match"), 401)


@app.route('/driverRide', methods=['POST'])
def create_driverRide():
    data = request.get_json()
    driverRide_schema = DriverRideSchema()
    driverRide = driverRide_schema.load(data)
    result = driverRide_schema.dump(driverRide.create())
    return make_response(jsonify({"ride": result}), 200)

@app.route('/driverRide/<string:id>', methods=['GET'])
def getDriverRide(id):
    try:
        get_driver_ride = DriverRide.query.get(id)
        if not get_driver_ride:
            return make_response(jsonify({"Message": "Id not found"}))
        driver_ride_schema = DriverRideSchema()
        driver_ride = driver_ride_schema.dump(get_driver_ride)
        return make_response(jsonify({"driver_ride": driver_ride}))
    except ValidationError as err:
        return err.messages, 400


if __name__ == '__main__':
    app.run()

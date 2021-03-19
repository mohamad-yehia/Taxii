import json
import os

from datetime import date, datetime
from flask import Flask, render_template, request, jsonify, make_response
from Schema import DriverSchema
from model import Driver
from app import app, db
from Connection import Connection
import hashlib


@app.route('/')
def index():
    return "Welcome to Taxii app, have a safe trip!!!"


@app.route('/driver', methods=['POST'])
def newDriver():
    driverInfo = request.get_json()
    today = date.today()
    for i in driverInfo:
        firstName = i[0]
        lastName = i[1]
        email = i[2]
        username = i[3]
        password = i[4]
        rate = i[5]
        hash_password = hashlib.md5(password.encode())
    cur = Connection().connection()
    cur.execute(
        "insert into drivers(firstName, lastName, email, username, password, rate, created_on, updated_on) VALUES (%s, %s, "
        "%s, %s, %s, %s, %s, %s)",
        (firstName, lastName, email, username, hash_password, rate, today, today))
    driverId = {'id': cur.lastrowid}
    driverInfo.update(driverId)
    cur.close()
    return jsonify({'driver': driverInfo})

@app.route('/products', methods = ['POST'])
def create_product():
    data = request.get_json()
    #password = data['password']
    created_on = data['created_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    updated_on = data['updated_on'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    password = data['password']
    hash_password = hashlib.md5(password.encode())
    driver_schema = DriverSchema()
    data['created_on'] = created_on
    data['updated_on'] = updated_on
    driver = driver_schema.load(data)
    #driver = driver_schema.load(created_on)
    #driver = driver_schema.load(updated_on)
    result = driver_schema.dump(driver.create())
    return make_response(jsonify({"product": result}),200)

@app.route('/driver/<string:id>', methods=['DELETE'])
def deleteDriver(id):
    cur = Connection().connection()
    cur.execute("SELECT * FROM drivers WHERE ID=%s", [id])
    if len(cur.fetchall()) > 0:
        cur.execute("DELETE FROM drivers WHERE ID=%s", [id])
    else:
        return jsonify({'Error': 'Driver ' + id + ' doesn\'t exist!!!'})
    cur.close()
    return jsonify({'Message': 'The Driver ' + id + ' is deleted successfully'})

@app.route('/driver/<string:id>', methods=['GET'])
def getDriver(id):
    try:
        cur = Connection().connection()
        cur.execute("SELECT * FROM drivers WHERE ID=%s", [id])
        if len(cur.fetchall()) > 0:
            cur.execute("SELECT ID, EMAIL, FIRSTNAME, LASTNAME, USERNAME FROM drivers WHERE ID=%s", [id])
            driver = cur.fetchone()
            driver = jsonify(driver)
            driver.status_code = 200
        else:
            return jsonify({'Error': 'Driver ' + id + ' doesn\'t exist!!!'})
        cur.close()
        return driver

    except Exception as e:
        print(e)

@app.route('/drivers', methods = ['GET'])
def alldrivers():
    get_drivers = Driver.query.all()
    driver_schema = DriverSchema(many=True)
    drivers = driver_schema.dump(get_drivers)
    return make_response(jsonify({"drivers": drivers}))

if __name__ == '__main__':
    app.run()

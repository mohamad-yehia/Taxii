import json

from flask import Flask, render_template, request, jsonify
from Connection import Connection
from Driver import Driver
import hashlib
app = Flask(__name__)

@app.route('/driver', methods=['POST'])
def newDriver():
    driverInfo = request.get_json()
    for i in driverInfo:
        firstName = i[0]
        lastName = i[1]
        email = i[2]
        username = i[3]
        password = i[4]
        hash_password = hashlib.md5(password.encode())
    cur = Connection().connection()
    cur.execute("INSERT INTO DRIVERS(firstName, lastName, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                (firstName, lastName, email, username, hash_password))
    driverId = {'id': cur.lastrowid}
    driverInfo.update(driverId)
    cur.close()
    return jsonify({'driver': driverInfo})

@app.route('/driver/<string:id>', methods=['DELETE'])
def deleteDriver(id):
    cur = Connection().connection()
    cur.execute("SELECT * FROM DRIVERS WHERE ID=%s", [id])
    if len(cur.fetchall()) > 0:
        cur.execute("DELETE FROM DRIVERS WHERE ID=%s", [id])
    else:
        return jsonify({'Error': 'Driver ' + id + ' doesn\'t exist!!!'})
    cur.close()
    return jsonify({'Message': 'The Driver ' + id + ' is deleted successfully'})


if __name__ == '__main__':
    app.run()
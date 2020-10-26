import json

from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import hashlib
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'TAXII'

mysql = MySQL(app)

@app.route('/createDriver', methods=['POST'])
def newDriver():
    driverInfo = request.get_json()
    for i in driverInfo:
        firstName = i[0]
        lastName = i[1]
        email = i[2]
        username = i[3]
        password = i[4]
        hash_password = hashlib.md5(password.encode())
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO DRIVERS(firstName, lastName, email, username, password) VALUES (%s, %s, %s, %s, %s)",
                (firstName, lastName, email, username, hash_password))
    mysql.connection.commit()
    cur.close()
    return 'success'

@app.route('/deleteDriver/<string:id>', methods=['DELETE'])
def deleteDriver(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM DRIVERS WHERE ID=%s", id)
    if len(cur.fetchall()) > 0:
        cur.execute("DELETE FROM DRIVERS WHERE ID=%s", id)
    else:
        return jsonify({'Error': 'Driver ' + id + ' doesn\'t exist!!!'})
    mysql.connection.commit()
    cur.close()
    return jsonify({'Message': 'The Driver ' + id + ' is deleted successfully'})


if __name__ == '__main__':
    app.run()
from ConfigDB import Config
import pymysql
import os

class Connection:

    def __init__(self):
        db_server = os.environ['DB_SERVER']
        db_user = os.environ['DB_USER']
        db_password = os.environ['DB_PASSWORD']
        db_name = os.environ['DB_NAME']
        self.db=pymysql.connect(host=db_server, user=db_user, passwd=db_password, db=db_name)
        self.db.autocommit(True)

    def connection(self):
        self.cur = self.db.cursor()
        return self.cur
import hashlib

from datetime import datetime
from API import db, app
from model import Driver

with app.app_context():
    db.create_all()

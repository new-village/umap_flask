from flask_pymongo import PyMongo
from flask_login import UserMixin
from werkzeug.security import check_password_hash

mongo = PyMongo()


class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

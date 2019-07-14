from flask_pymongo import PyMongo, ObjectId
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import mongo


class User(UserMixin):
    def __init__(self, email, password):
        self.id = email
        self.email = email
        self.password = password

    def __str__(self):
        return self.email + "/" + self.password

    def save(self):
        hashed_password = generate_password_hash(self.password)
        user = {"_id": self.email.lower(), "password": hashed_password}
        result = mongo.db.users.update({"_id": self.id}, user, upsert=True)
        return result

    @staticmethod
    def search(email):
        rtn = mongo.db.users.find_one({"_id": email})
        if rtn:
            return User(rtn["_id"], rtn["password"])
        else:
            return None

    def valid_password(self, password):
        return check_password_hash(self.password, password)

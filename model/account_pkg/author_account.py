from model.account_pkg.account import Account
import pymongo
from pymongo import MongoClient
import urllib.parse


class AuthorAccount(Account):

    def __init__(self, account_id: int, username: str, password: str, notification: []):
        super(AuthorAccount, self).__init__(account_id, username, password, Account.Role.AUTHOR, notification)
        self.__client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")
        self._username = None
        self._account_id = None
        self._password = None

    def login(self, username, password):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        res = col.find_one({"username": username, "password": password})
        if res is None:
            return 0
        else:
            self._username = username
            self._account_id = res['id']
            self._password = password
            return 1

    def user_exists(self, username):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        res = col.find_one({"username": username})
        return 0 if res is None else 1

    def account_type(self, username):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        res = col.find_one({"username": username})
        return res['role']

    def change_password(self, oldpass: str, newpass: str):
        pass

    def update(self):
        pass

    def notify_account_change(self):
        pass

    def get_account_id(self):
        return self._account_id

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

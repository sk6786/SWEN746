from model.account_pkg.account import Account
import pymongo
from pymongo import MongoClient
import urllib.parse

class AuthorAccount(Account):

    def __init__(self):
        self.__account_id = ""
        self.__username = ""
        self.__password = ""
        self.__client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")


    @property
    def __account_id(self):
        return self.__account_id

    @__account_id.setter
    def __account_id(self, acc_id):
        self.__accountID = acc_id

    # TODO: add other getter and setter

    def login(self, username, password):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        res = col.find_one({"username": username, "password": password})
        if res is None:
            return 0
        else:
            self.__username = username
            self.__account_id = res['_id']
            self.__password = password
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

    def create_account(self, username, password):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        mydict = {"username": username, "password": password, "role": "author"}
        col.insert_one(mydict)

    def change_password(self, oldpass: str, newpass: str):
        pass

    def update(self):
        pass

    def notify_account_change(self):
        pass


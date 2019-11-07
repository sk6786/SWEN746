import pymongo
from pymongo import MongoClient
import urllib.parse
class Auth():

    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")

    def login(self, username, password):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        res = col.find_one({"username": username, "password": password})
        return 0 if res is None else 1

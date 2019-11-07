import pymongo
from pymongo import MongoClient
import urllib.parse
class Register():

    def __init__(self):
        self.__client = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")
    def create_account(self, username, password):
        db = self.__client.get_database("SAM2020")
        col = db.get_collection("Accounts")
        mydict = {"username": username, "password": password, "role": "author"}
        col.insert_one(mydict)



import pymongo
from pymongo import MongoClient
import urllib.parse

cli = pymongo.MongoClient("mongodb+srv://"+urllib.parse.quote_plus("USER2")+":"+urllib.parse.quote_plus("1q2w3e4r")+"@cluster0-tk7v1.mongodb.net/test?retryWrites=true&w=majority")
db = cli.get_database("SAM2020")
col = db.get_collection("Accounts")
mydict = {"name": "John", "address": "Highway 37"}
x = col.insert_one(mydict)
print(cli)


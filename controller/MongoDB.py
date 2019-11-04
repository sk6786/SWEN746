
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient('mongodb://USER2:SAM2020@cluster0-tk7v1.mongodb.net/SAM2020')
db = client.SAM2020

col =db.Accounts

emp_rec1 = {"name": "Mr.Geek"}
emp_rec2 = {"name": "Mr.Shaurya"}

# Insert Data
col.insert_one(emp_rec1)
col.insert_one(emp_rec2)





import pymongo
from pymongo import MongoClient
from settings import *


cluster = MongoClient(DATABASE)
db = cluster[DB_NAME]
collection = db[COLLECTION_NAME]

collection.insert_one({"_id": 0, "name": "test"})

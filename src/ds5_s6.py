import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')
db=client.myDB
results = db.myCol.find()
for r in results:
        print r['Persons']
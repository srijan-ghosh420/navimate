from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["kolkata_navigation"]

collection = db["context"]

with open("context_data.json") as f:
    data = json.load(f)

collection.insert_many(data)

print("Context data inserted!")

from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["kolkata_navigation"]

collection = db["area_context"]

with open("area_context.json") as f:
    data = json.load(f)

collection.insert_many(data)

print("Area context inserted!")
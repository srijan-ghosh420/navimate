from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["kolkata_navigation"]
collection = db["edges"]

with open("edges_bidirectional.json") as f:
    data = json.load(f)

collection.insert_many(data)

print("Data inserted!")
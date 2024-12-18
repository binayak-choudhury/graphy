import os
from pymongo import MongoClient

# Initialize the MongoDB client once
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
mongo_db = os.getenv("MONGODB_DB", "product_catalog")

# Create a MongoClient instance and connect to the database
client = MongoClient(mongo_uri)

# Access the database
db = client[mongo_db]

def get_db():
    """
    Return the database instance
    """
    return db

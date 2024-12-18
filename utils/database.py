import pymongo
from config import Config


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            config = Config

            try:
                # Connect to MongoDB
                cls._instance.client = pymongo.MongoClient(config.MONGODB_URI)
                cls._instance.db = cls._instance.client[config.MONGODB_DB]

                # Create products collection with indexes
                cls._instance.products_collection = cls._instance.db["products"]

                cls._instance.products_collection.create_index(
                    [("category", pymongo.ASCENDING)]
                )
                cls._instance.products_collection.create_index(
                    [("price", pymongo.ASCENDING)]
                )
            except Exception as e:
                print(f"Error connecting to MongoDB: {e}")
                raise
        return cls._instance


db_connection = DatabaseConnection()

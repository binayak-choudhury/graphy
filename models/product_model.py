from dataclasses import dataclass, field
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
import os
from config import Config
import uuid


@dataclass
class Product:
    """Product Model class representing a product in the catalog."""

    _id: Optional[ObjectId] = field(default_factory=ObjectId)
    name: str = ""
    category: str = ""
    price: float = 0.0
    stock: int = 0

    def to_dict(self):
        """Convert the Product object to a dictionary."""
        return {
            "_id": str(self._id),
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
        }

    @staticmethod
    def from_dict(product_data: dict):
        """Create a Product object from a dictionary."""
        return Product(
            _id=product_data.get("_id") or str(ObjectId()),
            name=product_data.get("name"),
            category=product_data.get("category"),
            price=product_data.get("price"),
            stock=product_data.get("stock"),
        )

    @staticmethod
    def get_mongo_client():
        """Get the MongoDB client with the appropriate database."""
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        mongo_db = os.getenv("MONGODB_DB", "product_catalog")
        client = MongoClient(mongo_uri)
        return client[mongo_db]

    @staticmethod
    def get_by_id(product_id: int) -> Optional["Product"]:
        """Fetch a product from MongoDB by its ID."""
        product_collection = Product.get_mongo_client().products
        product_data = product_collection.find_one({"_id": product_id})
        return Product.from_dict(product_data) if product_data else None

    @staticmethod
    def get_by_filters(query: dict) -> list["Product"]:
        """Fetch a product from MongoDB by its ID."""
        product_collection = Product.get_mongo_client().products
        product_data: list[Product] = product_collection.find(query)
        return [Product.from_dict(data) for data in product_data]

    @staticmethod
    def get_all() -> List["Product"]:
        """Fetch all products from MongoDB."""
        product_collection = Product.get_mongo_client().products
        products_data = list(product_collection.find({}))
        return [Product.from_dict(data) for data in products_data]

    @staticmethod
    def create(product_data: dict) -> "Product":
        """Insert a new product into MongoDB."""
        product_collection = Product.get_mongo_client().products
        product = Product.from_dict(product_data)
        product_collection.insert_one(product.to_dict())
        return product

    @staticmethod
    def update(product_id: int, product_data: dict) -> bool:
        """Update an existing product in MongoDB."""
        product_collection = Product.get_mongo_client().products
        result = product_collection.update_one(
            {"_id": ObjectId(product_id)}, {"$set": product_data}
        )
        return result.matched_count > 0

    @staticmethod
    def delete(product_id: int) -> bool:
        """Delete a product from MongoDB."""
        product_collection = Product.get_mongo_client().products
        result = product_collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0

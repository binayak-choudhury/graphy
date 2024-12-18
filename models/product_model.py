from dataclasses import dataclass, field
from bson import ObjectId
from models import get_db


@dataclass
class Product:
    """
    Product Catalog Model
    """

    _id: str = field(default_factory=str(ObjectId()))
    name: str = field(default="")
    category: str = field(default="")
    price: float = field(default=0.0)
    stock: int = field(default=0)

    def to_dict(self):
        """
        Convert the Product object to a dictionary.
        """
        return {
            "_id": str(self._id),
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
        }

    @staticmethod
    def from_dict(product_data: dict):
        """
        Create a Product object from a dictionary.
        """
        return Product(
            _id=product_data.get("_id") or str(ObjectId()),
            name=product_data.get("name"),
            category=product_data.get("category"),
            price=product_data.get("price"),
            stock=product_data.get("stock"),
        )

    @staticmethod
    def get_by_id(product_id: str) -> "Product":
        """
        Fetch a product by 'id'.
        """
        product_collection = get_db().products
        product_data = product_collection.find_one({"_id": product_id})
        return Product.from_dict(product_data) if product_data else None

    @staticmethod
    def get_by_filters(query: dict) -> list["Product"]:
        """
        Fetch products from query.
        """
        product_collection = get_db().products
        product_data: list[Product] = product_collection.find(query)
        return [Product.from_dict(data) for data in product_data]

    @staticmethod
    def get_all() -> list["Product"]:
        """
        Fetch all products.
        """
        product_collection = get_db().products
        products_data = list(product_collection.find({}))
        return [Product.from_dict(data) for data in products_data]

    @staticmethod
    def create(product_data: dict) -> "Product":
        """
        Insert a new product.
        """
        product_collection = get_db().products
        product = Product.from_dict(product_data)
        product_collection.insert_one(product.to_dict())
        return product

    @staticmethod
    def update(product_id: str, product_data: dict) -> bool:
        """
        Upsert an existing product.
        """
        product_collection = get_db().products
        result = product_collection.update_one(
            {"_id": product_id}, {"$set": product_data}
        )
        return result.matched_count > 0

    @staticmethod
    def delete(product_id: str) -> bool:
        """
        Delete a product.
        """
        product_collection = get_db().products
        result = product_collection.delete_one({"_id": product_id})
        return result.deleted_count > 0

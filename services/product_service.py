from models.product_model import Product
import redis
from config import Config
import json

# Initialize Redis Cache
redis_cache = redis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)


def get_all_products():
    """Fetch all products with caching logic."""
    cache_key = "all_products"

    # Check Redis cache
    cached_data = redis_cache.get(cache_key)
    if cached_data:
        return eval(cached_data)  # Return cached data if present

    # Fetch from MongoDB using the Product model
    products = Product.get_all()
    redis_cache.setex(
        cache_key,
        Config.PRODUCT_LIST_CACHE_EXPIRY,
        str([product.to_dict() for product in products]),
    )  # Cache with expiry
    return [product.to_dict() for product in products]


def get_product_by_id(product_id):
    """Fetch a specific product by ID."""
    cache_key = f"product_{product_id}"

    # Check Redis cache
    cached_data = redis_cache.get(cache_key)
    if cached_data:
        return json.loads(cached_data)  # Deserialize data from Redis cache

    # Fetch from MongoDB using the Product model
    product = Product.get_by_id(product_id)
    if product:
        redis_cache.setex(
            cache_key, Config.PRODUCT_CACHE_EXPIRY, json.dumps(product.to_dict())
        )  # Serialize and cache with expiry
    return product.to_dict() if product else None


def create_product(data):
    """Create a new product and invalidate cache."""
    new_product = Product.create(data)

    # Invalidate cache
    redis_cache.delete("all_products")

    return new_product.to_dict()


def update_product(product_id, data):
    """Update an existing product and invalidate cache."""
    if Product.update(product_id, data):
        redis_cache.delete(f"product_{product_id}")  # Invalidate product cache
        redis_cache.delete("all_products")  # Invalidate product list cache
        return Product.get_by_id(product_id).to_dict()  # Return updated product data
    return None


def delete_product(product_id):
    """Delete a product and invalidate cache."""
    if Product.delete(product_id):
        redis_cache.delete(f"product_{product_id}")  # Invalidate product cache
        redis_cache.delete("all_products")  # Invalidate product list cache
        return True
    return False


def filter_products(category=None, price_min=None, price_max=None):
    """Filter products based on category and price range."""

    query = {}

    # Add filters to the query dynamically
    if category:
        query["category"] = category
    if price_min is not None:
        query["price"] = {"$gte": float(price_min)}  # Filter price >= price_min
    if price_max is not None:
        if "price" not in query:
            query["price"] = {}
        query["price"]["$lte"] = float(price_max)  # Filter price <= price_max

    return Product.get_by_filters(query)

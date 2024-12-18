from models.product_model import Product
from utils.cache import RedisCache
from config import Config
import logging

# Initialize RedisCache instance
redis_cache = RedisCache()

# Configure logging
logger = logging.getLogger(__name__)
log_filename = 'app.log'
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

# Cache statistics variables
cache_stats = {"hits": 0, "misses": 0}


def get_all_products():
    """
    Fetch all products with caching logic.
    """
    cache_key = "all_products"

    # Check Redis cache
    cached_data = redis_cache.get(cache_key)
    if cached_data:
        return cached_data

    # Fetch from Product model
    products = Product.get_all()
    redis_cache.cache_product_list(products)
    return [product.to_dict() for product in products]


def get_product_by_id(product_id: str):
    """
    Fetch a specific product by ID.
    """
    cache_key = f"product_{product_id}"

    # Check Redis cache
    cached_data = redis_cache.get(cache_key)
    if cached_data:
        return cached_data  # Return cached data if available

    # Fetch from MongoDB using the Product model
    product = Product.get_by_id(product_id)
    if product:
        redis_cache.cache_product(product_id, product)  # Cache the product
    return product.to_dict() if product else None


def create_product(data: dict):
    """
    Create a new product and invalidate cache.
    """
    new_product: Product = Product.create(data)

    # Invalidate cache
    redis_cache.invalidate_product_list_cache()
    redis_cache.invalidate_product_cache(new_product._id)

    return new_product.to_dict()


def update_product(product_id: str, data: dict):
    """
    Update an existing product and invalidate cache.
    """
    if Product.update(product_id, data):
        redis_cache.invalidate_product_cache(product_id)
        redis_cache.invalidate_product_list_cache()

        # Cache the updated product (optional but ensures freshness)
        updated_product = Product.get_by_id(product_id)
        redis_cache.cache_product(product_id, updated_product)

        return updated_product.to_dict()  # Return updated product data
    return None


def delete_product(product_id):
    """Delete a product and invalidate cache."""
    if Product.delete(product_id):
        redis_cache.invalidate_product_cache(product_id)  # Invalidate cache for deleted product
        redis_cache.invalidate_product_list_cache()  # Invalidate product list cache

        return True
    return False


def filter_products(category=None, price_min=None, price_max=None):
    """Filter products based on category and price range."""

    query = {}

    # Add filters to the query dynamically
    if category:
        query["category"] = category
    if price_min is not None:
        try:
            query["price"] = {"$gte": float(price_min)}  # Filter price >= price_min
        except ValueError:
            return {"error": "Invalid value for price_min"}  # Handle invalid price_min
    if price_max is not None:
        try:
            if "price" not in query:
                query["price"] = {}
            query["price"]["$lte"] = float(price_max)  # Filter price <= price_max
        except ValueError:
            return {"error": "Invalid value for price_max"}  # Handle invalid price_max
        
    
    # Log the received query parameters
    logger.info("Received query parameters - Category: %s, Price Min: %s, Price Max: %s", category, price_min, price_max)

    # Cache the filtered result (optional, depending on your use case)
    cache_key = f"filtered_products_{str(query)}"
    cached_data = redis_cache.get(cache_key)

    if cached_data:
        cache_stats["hits"] += 1
        logger.info("Cache hit. Cache Hits: %d", cache_stats["hits"])
        return cached_data  # Return cached filtered products if available

    # Fetch filtered products from MongoDB
    products = Product.get_by_filters(query)

    # Cache the filtered result
    redis_cache.set(cache_key, [product.to_dict() for product in products], Config.PRODUCT_LIST_CACHE_EXPIRY)
    cache_stats["misses"] += 1
    logger.info("Cache miss. Cache Misses: %d", cache_stats["misses"])

    return [product.to_dict() for product in products]
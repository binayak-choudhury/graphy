import json
import redis
from config import Config
from models.product_model import Product

class RedisCache:
    """
    Handles all Redis cache operations.
    """

    def __init__(self):
        """
        Initialize client.
        """
        self.client = redis.StrictRedis(
            host=Config.REDIS_HOST, 
            port=Config.REDIS_PORT, 
            db=0, 
            decode_responses=True
        )
    
    def get(self, cache_key: str):
        """
        Get data from the cache.
        """
        cached_data = self.client.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        return None
    
    def set(self, cache_key: str, data: dict, expiry_time: int):
        """
        Set data in the cache with an expiration time.
        """
        self.client.setex(
            cache_key, 
            expiry_time, 
            json.dumps(data)
        )
    
    def delete(self, cache_key: str):
        """
        Delete data from the cache.
        """
        self.client.delete(cache_key)
    
    def cache_product_list(self, products: list[Product]):
        """
        Cache the entire product list.
        """
        cache_key = "all_products"
        self.set(cache_key, [product.to_dict() for product in products], Config.PRODUCT_LIST_CACHE_EXPIRY)
    
    def cache_product(self, product_id: str, product: Product):
        """
        Cache an individual product.
        """
        cache_key = f"product_{product_id}"
        self.set(cache_key, product.to_dict(), Config.PRODUCT_CACHE_EXPIRY)

    def invalidate_product_cache(self, product_id: str):
        """
        Invalidate cache for a specific product.
        """
        cache_key = f"product_{product_id}"
        self.delete(cache_key)
    
    def invalidate_product_list_cache(self):
        """
        Invalidate the entire product list cache.
        """
        self.delete("all_products")
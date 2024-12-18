import redis
from config import get_config


class CacheConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            config = get_config()

            try:
                # Connect to Redis
                cls._instance.client = redis.Redis(
                    host=config.REDIS_HOST,
                    port=config.REDIS_PORT,
                    decode_responses=True,
                )
            except Exception as e:
                print(f"Error connecting to Redis: {e}")
                raise
        return cls._instance


cache_connection = CacheConnection()

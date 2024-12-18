import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base Configuration Class
    """

    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    MONGODB_DB = os.getenv("MONGODB_DB", "product_catalog")

    # Redis Configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

    # Caching Configuration
    PRODUCT_CACHE_EXPIRY = 600  # Cache expiry for product details (10 minutes)
    PRODUCT_LIST_CACHE_EXPIRY = 300  # Cache expiry for product list (5 minutes)

    # Flask Application Configuration
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "development_secret_key")


# Development-specific configuration
class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = os.getenv("MONGODB_DB", "product_catalog_dev")


# Production-specific configuration
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "production_secret_key")


# Testing-specific configuration
class TestingConfig(Config):
    TESTING = True
    MONGODB_DB = "test_product_catalog"
    PRODUCT_CACHE_EXPIRY = 60  # Shorter cache for testing (1 minute)
    PRODUCT_LIST_CACHE_EXPIRY = 30

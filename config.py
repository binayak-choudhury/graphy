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
    PRODUCT_CACHE_EXPIRY = 600
    PRODUCT_LIST_CACHE_EXPIRY = 300

    # Flask Application Configuration
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "development_secret_key")


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_DB = os.getenv("MONGODB_DB", "product_catalog_dev")


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "production_secret_key")
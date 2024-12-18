from flask import Flask
from config import DevelopmentConfig, ProductionConfig

# Choose Config based on environment
import os

env = os.getenv("FLASK_ENV", "development")

if env == "production":
    config_class = ProductionConfig
else:
    config_class = DevelopmentConfig

# Initialize Flask App
app = Flask(__name__)
app.config.from_object(config_class)

# Import blueprints
from controllers.product_controller import product_bp

app.register_blueprint(product_bp)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])

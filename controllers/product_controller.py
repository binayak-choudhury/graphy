from flask import Blueprint, request, jsonify
from services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
    filter_products,
)

product_bp = Blueprint("product", __name__)


# GET /products - Fetch all products
@product_bp.route("/products", methods=["GET"])
def get_products():
    products = get_all_products()
    return jsonify({"data": products}), 200


# GET /products/{id} - Fetch specific product by ID
@product_bp.route("/products/<string:id>", methods=["GET"])
def get_product(id):
    product = get_product_by_id(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify({"data": product}), 200


# POST /products - Add new product
@product_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = create_product(data)
    return jsonify({"data": new_product}), 201


# PUT /products/{id} - Update product details
@product_bp.route("/products/<int:id>", methods=["PUT"])
def update_product_info(id):
    data = request.get_json()
    updated_product = update_product(id, data)
    if not updated_product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify({"data": updated_product}), 200


# DELETE /products/{id} - Delete product
@product_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product_info(id):
    result = delete_product(id)
    if not result:
        return jsonify({"message": "Product not found"}), 404
    return jsonify({"message": "Product deleted successfully"}), 200


@product_bp.route("/products/filter", methods=["GET"])
def get_filtered_products():
    """Filter products by category and price range."""
    category = request.args.get("category")  # Get 'category' from query params
    price_min = request.args.get("price_min")  # Get 'price_min' from query params
    price_max = request.args.get("price_max")  # Get 'price_max' from query params

    # Call the filter function
    products = filter_products(
        category=category, price_min=price_min, price_max=price_max
    )
    return jsonify(products), 200

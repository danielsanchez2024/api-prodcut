from flask import Blueprint, request, jsonify
from app.database import mongo_db
from bson import ObjectId

mongo_bp = Blueprint('mongo', __name__)

def is_valid_objectid(id):
    """Valida si un ID es un ObjectId de MongoDB"""
    try:
        return ObjectId(id)
    except Exception:
        return None

def serialize_product(product):
    """Convierte ObjectId a string en un producto"""
    if product and "_id" in product:
        product["_id"] = str(product["_id"])
    return product

@mongo_bp.route("/products/mongo", methods=["POST"])
def add_product_mongo():
    data = request.json

    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid data format"}), 400

    required_fields = ["name", "price", "stock"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data.get("price"), (int, float)) or data["price"] < 0:
        return jsonify({"error": "Invalid price"}), 400

    if not isinstance(data.get("stock"), int) or data["stock"] < 0:
        return jsonify({"error": "Invalid stock"}), 400

    result = mongo_db.products.insert_one(data)
    return jsonify({"message": "Product added", "id": str(result.inserted_id)}), 201

@mongo_bp.route("/products/mongo", methods=["GET"])
def get_all_products_mongo():
    products = list(mongo_db.products.find())
    return jsonify([serialize_product(product) for product in products]), 200

@mongo_bp.route("/products/mongo/<product_id>", methods=["GET"])
def get_product_mongo(product_id):
    object_id = is_valid_objectid(product_id)
    if not object_id:
        return jsonify({"error": "Invalid product ID format"}), 400

    product = mongo_db.products.find_one({"_id": object_id})
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(serialize_product(product)), 200

@mongo_bp.route("/products/mongo/<product_id>", methods=["PUT"])
def update_product_mongo(product_id):
    object_id = is_valid_objectid(product_id)
    if not object_id:
        return jsonify({"error": "Invalid product ID format"}), 400

    data = request.json
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid data format"}), 400

    if "price" in data and (not isinstance(data["price"], (int, float)) or data["price"] < 0):
        return jsonify({"error": "Invalid price"}), 400

    if "stock" in data and (not isinstance(data["stock"], int) or data["stock"] < 0):
        return jsonify({"error": "Invalid stock"}), 400

    result = mongo_db.products.update_one({"_id": object_id}, {"$set": data})

    if result.matched_count == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product updated" if result.modified_count else "No changes made"}), 200

@mongo_bp.route("/products/mongo/<product_id>", methods=["DELETE"])
def delete_product_mongo(product_id):
    object_id = is_valid_objectid(product_id)
    if not object_id:
        return jsonify({"error": "Invalid product ID format"}), 400

    result = mongo_db.products.delete_one({"_id": object_id})

    if result.deleted_count == 0:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product deleted"}), 200

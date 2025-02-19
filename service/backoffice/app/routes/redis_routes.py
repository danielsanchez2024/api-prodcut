from flask import Blueprint, request, jsonify
import json
from app.database import redis_client

redis_routes = Blueprint("redis_routes", __name__)

# Función auxiliar para validar JSON en Redis
def get_json_from_redis(key):
    try:
        value = redis_client.get(key)
        return json.loads(value) if value else None
    except json.JSONDecodeError:
        return None
    except Exception as e:
        return str(e)

# Agregar un producto a Redis
@redis_routes.route("/products/redis", methods=["POST"])
def add_product_redis():
    try:
        data = request.json
        product_id = data.get("id")

        if not product_id or not isinstance(product_id, str):
            return jsonify({"error": "Valid 'id' is required"}), 400

        redis_client.set(f"product:{product_id}", json.dumps(data))
        return jsonify({"message": "Product added to Redis"}), 201

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Obtener todos los productos de Redis
@redis_routes.route("/products/redis", methods=["GET"])
def get_all_products_redis():
    try:
        keys = redis_client.keys("product:*")

        if not keys:
            return jsonify([])

        products = [get_json_from_redis(key) for key in keys if get_json_from_redis(key) is not None]

        return jsonify(products)

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Obtener un producto específico de Redis
@redis_routes.route("/products/redis/<product_id>", methods=["GET"])
def get_product_redis(product_id):
    try:
        if not isinstance(product_id, str):
            return jsonify({"error": "Invalid product ID"}), 400

        product = get_json_from_redis(f"product:{product_id}")

        if product:
            return jsonify(product)

        return jsonify({"error": "Product not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Actualizar un producto en Redis
@redis_routes.route("/products/redis/<product_id>", methods=["PUT"])
def update_product_redis(product_id):
    try:
        if not isinstance(product_id, str):
            return jsonify({"error": "Invalid product ID"}), 400

        data = request.json

        if redis_client.exists(f"product:{product_id}"):
            redis_client.set(f"product:{product_id}", json.dumps(data))
            return jsonify({"message": "Product updated in Redis"}), 200

        return jsonify({"error": "Product not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# Eliminar un producto de Redis
@redis_routes.route("/products/redis/<product_id>", methods=["DELETE"])
def delete_product_redis(product_id):
    try:
        if not isinstance(product_id, str):
            return jsonify({"error": "Invalid product ID"}), 400

        deleted = redis_client.delete(f"product:{product_id}")

        if deleted:
            return jsonify({"message": "Product deleted from Redis"}), 200

        return jsonify({"error": "Product not found"}), 404

    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

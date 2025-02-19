from flask import Blueprint, request, jsonify
from app.database import es_client
from app.config import config

es_routes = Blueprint("es_routes", __name__)

# Validate Elasticsearch index configuration
ES_INDEX = config.get("elasticsearch", {}).get("index")
if not ES_INDEX:
    raise ValueError("Elasticsearch index is not configured. Check your environment variables.")

def validate_request_data(required_fields):
    """Validates if the request contains all required fields."""
    data = request.json
    if not data:
        return None, jsonify({"error": "Invalid JSON payload."}), 400
    
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return None, jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    return data, None, None

# CRUD operations for Elasticsearch
@es_routes.route("/products/elasticsearch", methods=["POST"])
def add_product_es():
    data, error_response, status = validate_request_data(["id", "name", "description"])
    if error_response:
        return error_response, status
    
    product_id = data["id"]
    try:
        es_client.index(index=ES_INDEX, id=product_id, body=data)
        return jsonify({"message": "Product added to Elasticsearch."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@es_routes.route("/products/elasticsearch", methods=["GET"])
def get_all_products_es():
    try:
        result = es_client.search(index=ES_INDEX, body={"query": {"match_all": {}}})
        products = [doc["_source"] for doc in result["hits"]["hits"]]
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@es_routes.route("/products/elasticsearch/<product_id>", methods=["GET"])
def get_product_es(product_id):
    try:
        product = es_client.get(index=ES_INDEX, id=product_id)
        return jsonify(product["_source"])
    except Exception:
        return jsonify({"error": "Product not found."}), 404

@es_routes.route("/products/elasticsearch/<product_id>", methods=["PUT"])
def update_product_es(product_id):
    data, error_response, status = validate_request_data(["name", "description"])
    if error_response:
        return error_response, status
    
    try:
        if not es_client.exists(index=ES_INDEX, id=product_id):
            return jsonify({"error": "Product not found."}), 404
        
        es_client.index(index=ES_INDEX, id=product_id, body=data)
        return jsonify({"message": "Product updated in Elasticsearch."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@es_routes.route("/products/elasticsearch/<product_id>", methods=["DELETE"])
def delete_product_es(product_id):
    try:
        if not es_client.exists(index=ES_INDEX, id=product_id):
            return jsonify({"error": "Product not found."}), 404
        
        es_client.delete(index=ES_INDEX, id=product_id)
        return jsonify({"message": "Product deleted from Elasticsearch."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Flask
from app.routes.mongo_routes import mongo_bp
from app.routes.redis_routes import redis_routes
from app.routes.elasticsearch_routes import es_routes
from app.config import config

app = Flask(__name__)

# Registrar Blueprints
app.register_blueprint(mongo_bp)
app.register_blueprint(redis_routes)
app.register_blueprint(es_routes)

if __name__ == "__main__":
    app.run(host=config["app"]["host"], port=config["app"]["port"], debug=True)

from pymongo import MongoClient
from redis import Redis
from elasticsearch import Elasticsearch
from app.config import config

# Conexión a MongoDB
mongo_client = MongoClient(
    host=config["mongo"]["host"],
    port=int(config["mongo"]["port"]),
    username=config["mongo"]["username"],
    password=config["mongo"]["password"]
)
mongo_db = mongo_client[config["mongo"]["database"]]

# Conexión a Redis
redis_client = Redis(
    host=config["redis"]["host"],
    port=int(config["redis"]["port"]),
    decode_responses=True
)

# Conexión a Elasticsearch
es_client = Elasticsearch([{
    'host': config["elasticsearch"]["host"],
    'port': int(config["elasticsearch"]["port"]),
    'scheme': config["elasticsearch"]["scheme"]
}])

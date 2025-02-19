import os

config = {
    "app": {
        "port": os.getenv('FLASK_PORT', 5000),
        "host": os.getenv('FLASK_HOST', "backoffice")
    },
    "mongo": {
        "host": os.getenv("MONGO_HOST", "mongodb"), 
        "port": os.getenv("MONGO_PORT", "27017"),
        "username": os.getenv("MONGO_USER", "mongo"),
        "password": os.getenv("MONGO_PASSWORD", "password"),
        "database": os.getenv("MONGO_DB", "product")
    },
    "redis": {
        "host": os.getenv('REDIS_HOST', 'redis'),
        "port": os.getenv('REDIS_PORT', 6379)
    },
    "elasticsearch": {
        "host": os.getenv('ES_HOST', 'elasticsearch'),
        "port": os.getenv('ES_PORT', 9200),
        "scheme": os.getenv('ES_SCHEME', "http"),
        "index": os.getenv('ES_INDEX', "product")
    }
}

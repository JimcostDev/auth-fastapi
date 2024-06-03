from pymongo import MongoClient
import os
from contextlib import contextmanager

@contextmanager
def get_database_instance():
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        raise ValueError("La variable de entorno MONGODB_URI no está definida")
    
    client = MongoClient(mongo_uri)
    db = client['football']
    try:
        yield db
    finally:
        client.close()

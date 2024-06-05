# Importar MongoClient desde pymongo para conectar a MongoDB
from pymongo import MongoClient

# Importar os para acceder a las variables de entorno
import os

# Importar contextmanager para manejar el contexto de la conexión a la base de datos
from contextlib import contextmanager

@contextmanager
def get_database_instance():
    """
    Crea un contexto para manejar la conexión a la base de datos MongoDB.

    Yields:
    - db: Instancia de la base de datos 'football'.
    
    Este gestor de contexto asegura que la conexión a la base de datos se cierre
    automáticamente después de usarla.
    """
    # Obtener la URI de MongoDB desde las variables de entorno
    mongo_uri = os.getenv("MONGODB_URI")
    
    # Verificar si la URI está definida
    if not mongo_uri:
        # Lanzar un error si la variable de entorno no está definida
        raise ValueError("La variable de entorno MONGODB_URI no está definida")
    
    # Crear un cliente MongoDB usando la URI
    client = MongoClient(mongo_uri)
    
    # Acceder a la base de datos 'football'
    db = client['football']
    
    try:
        # Ceder el control al bloque de código que usa este contexto
        yield db
    finally:
        # Cerrar la conexión a la base de datos al salir del contexto
        client.close()

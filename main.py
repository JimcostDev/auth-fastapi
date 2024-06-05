# Importaciones necesarias de FastAPI, HTTPException, y Depends
from fastapi import FastAPI, HTTPException, Depends

# Importar la función para obtener la instancia de la base de datos
from conn_db import get_database_instance

# Importar la función para verificar el rol del usuario
from jwt_manager import check_user_role

# Importar el módulo de autenticación
import auth

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Definir una ruta GET para obtener la lista de equipos
@app.get("/teams", 
         tags=['auth'],
         summary="Obtener equipos de una liga o todos los equipos",
         description="Obtiene una lista de equipos de una liga o todos los equipos. Solo los usuarios autenticados pueden acceder a esta información.")
async def get_teams(current_user: dict = Depends(check_user_role)):
    """
    Endpoint para obtener una lista de equipos de la 'Premier League'.
    
    Args:
    - current_user (dict): Información del usuario actual, verificada por la función 'check_user_role'.

    Returns:
    - dict: Un diccionario con la lista de equipos.
    """
    try:
        # Conectar a la base de datos usando un contexto 'with'
        with get_database_instance() as db:
            # Acceder a la colección de equipos
            teams_collection = db.teams

            # Definir un filtro para la liga 'Premier League'
            filter = {"league": "Premier League"}

            # Ejecutar la consulta y ordenar los resultados por nombre (ascendente)
            cursor = teams_collection.find(filter, {"_id": 0}).sort("name", 1)

            # Convertir los documentos del cursor a una lista de diccionarios
            teams = [document for document in cursor]

            # Retornar la lista de equipos en un diccionario
            return {"teams": teams}
    except Exception as e:
        # Lanzar una excepción HTTP con código 500 si ocurre un error
        raise HTTPException(status_code=500, detail="Error al obtener los equipos")

# Incluir las rutas de autenticación definidas en el módulo 'auth'
app.include_router(auth.router)

from fastapi import FastAPI, HTTPException
from conn_db import get_database_instance

app = FastAPI()

@app.get("/teams")
async def get_teams():
    try:
        with get_database_instance() as db:
            teams_collection = db.teams

            # Consulta por liga
            filter = {}

            # Ejecutar la consulta y ordenar por nombre
            cursor = teams_collection.find(filter, {"_id": 0}).sort("name", 1)

            teams = [document for document in cursor]

            return {"teams": teams}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los equipos")

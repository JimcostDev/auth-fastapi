# Importaciones necesarias de FastAPI y otras librerías
from fastapi import APIRouter, HTTPException, status
from jwt_manager import create_token
from datetime import datetime, timedelta
import logging
from conn_db import get_database_instance
from pydantic import BaseModel, EmailStr

# Configuración del logger para registrar errores
logger = logging.getLogger(__name__)

# Crear un enrutador de FastAPI
router = APIRouter()

# Definir la clave secreta para firmar los tokens JWT
secret_key = "hola-esta-es-una-secret-key"  # Se debe cambiar por una clave segura, también se puede leer de una variable de entorno

# Definir el esquema de datos para el login de usuario usando Pydantic
class LoginUser(BaseModel):
    """Esquema para el login de usuario"""
    email: EmailStr
    password: str

# Función para obtener un usuario por su email
def get_user_by_email(email: EmailStr) -> dict:
    """
    Obtiene un usuario de la base de datos por su email.

    Args:
    - email (EmailStr): El email del usuario a buscar.

    Returns:
    - dict: Un diccionario con la información del usuario o None si no se encuentra.
    """
    try:
        with get_database_instance() as db:
            users_collection = db.users
            user = users_collection.find_one({"email": email})

            if user:
                return user
            else:
                return None
    except Exception as e:
        raise e

# Endpoint para iniciar sesión
@router.post(
    "/login",
    tags=['auth'],
    summary="Iniciar sesión de usuario",
    description="Endpoint para permitir a los usuarios iniciar sesión. Proporciona las credenciales de usuario en el cuerpo de la solicitud. "
                "Si las credenciales son válidas, devuelve un mensaje de inicio de sesión exitoso."
)
def login(user_data: LoginUser):
    """
    Iniciar sesión de usuario.

    Args:
    - user_data (LoginUser): El email y la contraseña del usuario.

    Returns:
    - dict: Un diccionario con un mensaje de éxito y el token de acceso.

    Raises:
    - HTTPException: Si el usuario no se encuentra o la contraseña es incorrecta.
    """
    try:
        user = get_user_by_email(user_data.email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No se pudo encontrar la información del usuario, email: '{user_data.email}' no existe.")
                
        # Verificar contraseña
        if not user['password'] == user_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")

        # Crear el payload del token JWT con información del usuario
        token_payload = {
            'sub': user['username'],
            'roles': user['roles'],
            # Tiempo de expiración del token (30 minutos)
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }

        # Generar el token usando create_token
        message = create_token(token_payload, secret_key)
        return message
    except Exception as e:
        logger.error(f"Ocurrió un error durante el login: {e}")
        raise e

# Importaciones necesarias
import os
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from conn_db import get_database_instance

# Función para obtener el usuario por su nombre de usuario
def get_user(username: str) -> dict:
    """
    Obtiene un usuario de la base de datos por su nombre de usuario.

    Args:
    - username (str): El nombre de usuario a buscar.

    Returns:
    - dict: Un diccionario con la información del usuario o None si no se encuentra.
    """
    try:
        with get_database_instance() as db:
            users_collection = db.users
            user = users_collection.find_one({"username": username})

            if user:
                return user
            else:
                return None
    except Exception as e:
        raise e

# Clave secreta para firmar los tokens JWT
secret_key = "hola-esta-es-una-secret-key"  # Se debe cambiar por una clave segura, también se puede leer de una variable de entorno

# Instancia del esquema OAuth2 para obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para generar un token JWT
def create_token(token_payload: dict, secret_key: str):
    """
    Genera un token JWT.

    Args:
    - token_payload (dict): Los datos a incluir en el token.
    - secret_key (str): La clave secreta para firmar el token.

    Returns:
    - dict: Un diccionario con el mensaje de éxito y el token generado.
    """
    try:
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')   
        return {"message": "Inicio de sesión exitoso", "access_token": token, "token_type": "bearer"}  
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al generar el token: {e}")

# Función para obtener y verificar el token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Obtiene el usuario actual a partir del token JWT.

    Args:
    - token (str): El token JWT.

    Returns:
    - dict: Un diccionario con la información del usuario.

    Raises:
    - HTTPException: Si el token no es válido o ha expirado.
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        username: str = payload.get("sub")
        user = get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user  
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"No se pudo validar las credenciales: {e}")

# Función de dependencia para verificar el rol del usuario
def check_user_role(current_user: dict = Depends(get_current_user)):
    """
    Verifica que el usuario tenga uno de los roles permitidos.

    Args:
    - current_user (dict): Información del usuario actual.

    Returns:
    - dict: La información del usuario si tiene un rol permitido.

    Raises:
    - HTTPException: Si el usuario no tiene un rol permitido.
    """
    allowed_roles = ['super-admin', 'admin']
    user_roles = current_user.get("roles", [])
    if not any(role in allowed_roles for role in user_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado. Se requiere rol de 'super-admin' o 'admin'")
    return current_user

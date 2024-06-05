## Auth con FastAPI

Este repositorio proporciona una implementación de autenticación utilizando FastAPI y MongoDB.

### Requisitos previos

### Requisitos previos

Asegúrate de tener instalado Python 3.6 o superior y crea una cuenta en MongoDB Atlas. Puedes registrarte y configurar una base de datos gratuita en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).


### Instrucciones de configuración

1. **Clona este repositorio ejecutando el siguiente comando:**
    ```bash
    git clone https://github.com/JimcostDev/auth-fastapi.git
    ```
    ```bash
    cd auth-fastapi
    ```

2. **Crea y activa tu entorno virtual:**
    - Crea un entorno virtual:
        ```bash
        python -m venv venv
        ```
    - Activa el entorno virtual:
        - En Windows:
            ```bash
            venv\Scripts\activate
            ```
        - En macOS y Linux:
            ```bash
            source venv/bin/activate
            ```

3. **Instala las dependencias requeridas:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configura la conexión a MongoDB:**
   Para conectarte a MongoDB, puedes hacerlo a través de una variable de entorno o directamente en el código. Reemplaza la siguiente parte en tu código:

   - Usando una variable de entorno:
     ```python
     import os

     mongo_uri = os.getenv("MONGODB_URI")
     ```
     Asegúrate de definir `MONGODB_URI` en tu entorno. Puedes hacerlo creando un archivo `.env` en el directorio raíz del proyecto y agregando:
     ```plaintext
     MONGODB_URI=tu_cadena_de_conexion
     ```

   - Usando una cadena directa (no recomendado para producción):
     ```python
     mongo_uri = "tu_cadena_de_conexion"
     ```

5. **Ejecuta la aplicación:**
    - En modo desarrollo:
        ```bash
        fastapi dev main.py 
        ```
        API docs: http://127.0.0.1:8000/docs 
    - En producción:
        ```bash
        fastapi run
        ```
6. **Usa Insomnia o Postman para probar la API:**
   - **Instala Insomnia o Postman:**
     - [Descarga Insomnia](https://insomnia.rest/download) o [descarga Postman](https://www.postman.com/downloads/).
   
   - **Configura una nueva solicitud:**
     - Abre Insomnia o Postman y crea una nueva solicitud.
     - Configura la URL de la solicitud apuntando a `http://127.0.0.1:8000` o al dominio donde esté desplegada tu API.
   
   - **Realiza solicitudes a los endpoints:**
     - Agrega los headers necesarios como `Content-Type: application/json` y cualquier header de autenticación si es requerido.
     - Prueba los distintos endpoints definidos en tu API, como registros, inicios de sesión, y cualquier otro recurso disponible.

   - **Ejemplo de solicitud en Insomnia/Postman:**
     - Método: `POST`
     - URL: `http://127.0.0.1:8000/login`
     - Headers:
       ```json
       {
         "Content-Type": "application/json"
       }
       ```
     - Body:
       ```json
       {
         "username": "tu_usuario",
         "password": "tu_contraseña"
       }
       ```

   - **Autenticación con token Bearer:**
     - Después de iniciar sesión y obtener un token, agrega el token a tus solicitudes para acceder a los endpoints protegidos.
     - Ejemplo de configuración del header de autorización en Insomnia o Postman:
       - Header: `Authorization`
       - Valor: `Bearer tu_token`
   
   - **Ejemplo de solicitud para ver equipos:**
     - Método: `GET`
     - URL: `http://127.0.0.1:8000/teams`
     - Headers:
       ```json
       {
         "Authorization": "Bearer tu_token"
       }
       ```
### Apoya el proyecto

Si te ha sido útil este proyecto, considera apoyarlo dando una estrella en GitHub. ¡Gracias por tu apoyo!

[Repositorio en GitHub](https://github.com/JimcostDev/auth-fastapi)

### Recursos adicionales

### Recursos adicionales

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de MongoDB](https://docs.mongodb.com/)
- [Repositorio personal sobre MongoDB](https://github.com/JimcostDev/mongodb_developer_path)
- **Video tutorial:** En este [video](https://youtu.be/BZZOuM1UpyI) te enseño a crear tu primera API y desplegarla.



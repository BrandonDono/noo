import os
from flask import Flask, Blueprint, jsonify, request
from flask_cors import CORS
from config import init_app, db
from controllers.userController import get_all_users, create_user, update_user, delete_user, login_user
from flask_jwt_extended import JWTManager
from flasgger import Swagger  # Importamos Swagger

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'siii'  # Cambia por una clave segura en producción
jwt = JWTManager(app)

swagger = Swagger(app)  

init_app(app)

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    """
    Obtener la lista de usuarios
    ---
    responses:
        200:
            description: OK. La solicitud se ha procesado correctamente.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
        404:
            description: No encontrado. No se encontraron usuarios.
        500:
            description: Error interno en el servidor.
    """
    return get_all_users()

@user_bp.route('/', methods=['POST'])
def user_store():
    """
    Crear un nuevo usuario
    ---
    parameters:
      - name: body
        in: body
        description: Datos del usuario
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john.doe@example.com
            password:
              type: string
              example: "password123"
    responses:
        201:
            description: Creado. El usuario se ha creado con éxito.
        400:
            description: Solicitud incorrecta. Los datos proporcionados son inválidos.
        409:
            description: Conflicto. Ya existe un usuario con ese correo electrónico.
        500:
            description: Error interno en el servidor.
    """
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    return create_user(name, email, password)

@user_bp.route('/<int:id>', methods=['PUT'])
def user_update(id):
    """
    Actualizar los datos de un usuario
    ---
    parameters:
      - name: id
        in: path
        description: ID del usuario
        required: true
        type: integer
      - name: body
        in: body
        description: Nuevos datos del usuario
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john.doe@example.com
    responses:
        200:
            description: OK. El usuario se ha actualizado correctamente.
        400:
            description: Solicitud incorrecta. Los datos proporcionados son inválidos.
        404:
            description: No encontrado. El usuario con el ID proporcionado no existe.
        409:
            description: Conflicto. El correo electrónico ya está en uso por otro usuario.
        500:
            description: Error interno en el servidor.
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    return update_user(id, name, email)

@user_bp.route('/<int:id>', methods=['DELETE'])
def user_delete(id):
    """
    Eliminar un usuario por su ID
    ---
    parameters:
      - name: id
        in: path
        description: ID del usuario a eliminar
        required: true
        type: integer
    responses:
        200:
            description: OK. El usuario se ha eliminado correctamente.
        404:
            description: No encontrado. El usuario con el ID proporcionado no existe.
        500:
            description: Error interno en el servidor.
    """
    return delete_user(id)

@user_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión para un usuario
    ---
    parameters:
      - name: body
        in: body
        description: Datos de inicio de sesión
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: john.doe@example.com
            password:
              type: string
              example: "password123"
    responses:
        200:
            description: OK. Inicio de sesión exitoso.
            schema:
              type: object
              properties:
                access_token:
                  type: string
        400:
            description: Solicitud incorrecta. Datos inválidos.
        401:
            description: No autorizado. Las credenciales son incorrectas.
        404:
            description: No encontrado. El usuario no existe.
        500:
            description: Error interno en el servidor.
    """
    data = request.get_json()
    return login_user(data['email'], data['password'])

# Registrar blueprint
app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True)

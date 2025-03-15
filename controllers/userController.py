from flask import jsonify
from models.User import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from config import db

# Obtener todos los usuarios
def get_all_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'msg': 'No se encontraron usuarios'}), 404
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener usuarios'}), 500

# Crear un nuevo usuario
def create_user(name, email, password):
    try:
        if User.query.filter_by(email=email).first():
            return jsonify({'msg': 'El correo ya está registrado'}), 400
        
        new_user = User(name, email, password)  # La contraseña se cifra automáticamente
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear usuario'}), 500

# Actualizar un usuario por ID
def update_user(id, name, email):
    try:
        user = User.query.get(id)
        if user:
            if User.query.filter_by(email=email).first() and user.email != email:
                return jsonify({'msg': 'El correo ya está en uso'}), 400
            
            user.name = name
            user.email = email
            db.session.commit()
            return jsonify(user.to_dict()), 200
        return jsonify({'msg': 'Usuario no encontrado'}), 404
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al actualizar usuario'}), 500

# Eliminar un usuario por ID
def delete_user(id):
    try:
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'msg': 'Usuario eliminado exitosamente'}), 200
        return jsonify({'msg': 'Usuario no encontrado'}), 404
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al eliminar usuario'}), 500

# Login de usuario
def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user': {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }), 200

    return jsonify({"msg": "Credenciales inválidas"}), 401

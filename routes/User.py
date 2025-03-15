from flask import Blueprint, jsonify, request
from controllers.userController import get_all_users, create_user, update_user, delete_user, login_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    return get_all_users()

@user_bp.route('/', methods=['POST'])
def user_store():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    return create_user(name, email, password)

@user_bp.route('/<int:id>', methods=['PUT'])
def user_update(id):
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    return update_user(id, name, email)

@user_bp.route('/<int:id>', methods=['DELETE'])
def user_delete(id):
    return delete_user(id)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return login_user(data['email'], data['password'])

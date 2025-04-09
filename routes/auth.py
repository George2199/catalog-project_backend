from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Заполните все поля"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Имя пользователя занято"}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Пользователь зарегистрирован"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print("== ЛОГИН ==")
    print("Полученные данные:", request.get_json())

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    print("Найден пользователь:", user)
    if user:
        print("Проверка пароля:", check_password_hash(user.password_hash, password))

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Неверный логин или пароль"}), 401

    if user.is_banned:
        return jsonify({"error": "Пользователь заблокирован"}), 403

    return jsonify({
        "message": "Успешный вход",
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }), 200

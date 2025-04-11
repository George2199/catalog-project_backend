from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Неверный логин или пароль"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "user_id": user.id,
        "username": user.username
    }), 200


@auth_bp.route("/profile", methods=["GET"])
def profile():
    user_id = request.args.get("user_id")  # или request.json, если POST
    if not user_id:
        return jsonify({"error": "Не передан user_id"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    from models import Resource
    user_resources = Resource.query.filter_by(user_id=user_id).all()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "resources": [
            {
                "id": r.id,
                "title": r.title,
                "date": r.last_updated.strftime('%d.%m.%Y') if r.last_updated else "неизвестно"
            } for r in user_resources
        ]
    })
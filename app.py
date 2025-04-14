from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, migrate
from models import User, Resource, Image
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()


    from routes.auth import auth_bp
    from routes.resources import resource_bp
    from routes.catalog import catalog_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(resource_bp, url_prefix="/api/resources")
    app.register_blueprint(catalog_bp, url_prefix="/api/catalog")

    # CORS(app, resources={r"/api/*": {
    #     "origins": "*",
    #     "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #     "allow_headers": ["Content-Type", "Authorization"]
    #     , "origins":["http://localhost:8081"]
    #     , "supports_credentials":True
    # }})

    CORS(app)

    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(os.path.join(app.root_path, 'static'), filename)
    
    @app.route("/db-check")
    def db_check():
        try:
            # Импорт модели
            from models import User  # или как у тебя там
            count = User.query.count()
            return f"DB подключена. Всего пользователей: {count}"
        except Exception as e:
            return f"Ошибка подключения к БД: {e}", 500

    
    app.config['JWT_SECRET_KEY'] = 'very-secret'
    jwt = JWTManager(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

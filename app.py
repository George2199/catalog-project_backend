from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from routes.auth import auth_bp
    from routes.resources import resource_bp
    from routes.catalog import catalog_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(resource_bp, url_prefix="/api/resources")
    app.register_blueprint(catalog_bp, url_prefix="/api/catalog")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

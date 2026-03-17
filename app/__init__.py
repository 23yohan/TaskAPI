from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models import task
        from .routes.health import health_bp
        from .routes.tasks import crud_bp

        app.register_blueprint(health_bp, url_prefix='/health')
        app.register_blueprint(crud_bp, url_prefix='/api')

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config, configTypes

db = SQLAlchemy()
migrate = Migrate()

def create_app(conf="dev"):
    """
    @Brief: Function creates the app
    @Param: conf - The config we want to use. three types
                    dev - Config for development
                    prod - Config used for production
                    testing - Config used for unit testing
    @Return: app - The flask application
    """
    app = Flask(__name__)
    app.config.from_object(configTypes[conf])

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models import task, users
        from .routes.health import health_bp
        from .routes.tasks import crud_bp
        from .routes.users import users_bp

        app.register_blueprint(health_bp, url_prefix='/health')
        app.register_blueprint(crud_bp, url_prefix='/tasks')
        app.register_blueprint(users_bp, url_prefix='/users')

    return app
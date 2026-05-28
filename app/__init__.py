import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    from app import config
    
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static"
    )

    # Load default config, then override with instance config (secrets & db)
    app.config.from_object(config.LiveConfig)
    app.config.from_pyfile('config.py', silent=True)

    # Initialize extensions
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models and routes after app exists
    with app.app_context():
        from app import models

    return app


app = create_app()

# Import routes
from app import properties

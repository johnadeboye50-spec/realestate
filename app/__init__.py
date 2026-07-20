import os
from flask import Flask, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from dotenv import load_dotenv


load_dotenv()

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    from app import config
    from app.models import User
    
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

    @app.context_processor
    def inject_users():
        admin = None
        agent = None
        client = None
        if session.get('user_id'):
            user = db.session.get(User, session['user_id'])
            if user:
                if user.role == 'admin':
                    admin = user
                elif user.role == 'agent':
                    agent = user
                elif user.role == 'client':
                    client = user   
        return dict(admin=admin, agent=agent, client=client)

    # Import models and routes after app exists
    with app.app_context():
        from app import models

    return app



app = create_app()

# Import routes
from app import properties

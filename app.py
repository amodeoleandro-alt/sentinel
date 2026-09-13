import os
from datetime import timedelta
from flask import Flask
from extensions import db, login_manager
from config import config_by_name
from models import Usuario


def create_app(env=None):
    env = env or os.environ.get("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env])
    app.permanent_session_lifetime = timedelta(
        minutes=app.config["PERMANENT_SESSION_LIFETIME_MINUTES"]
    )

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return "Acceso denegado: no tenés permisos para ver esta página.", 403

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

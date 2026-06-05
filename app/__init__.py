from flask import Flask

from config import config_dict

from app.extensions import *

from app.auth.login_manager import (
    init_login_manager
)


def create_app(config_name="default"):

    app = Flask(__name__)

    app.config.from_object(
        config_dict[config_name]
    )

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    bcrypt.init_app(app)

    init_login_manager(app)

    from app.auth.routes import auth_bp
    from app.core.dashboard import dashboard_bp
    from app.modules.usuarios.routes import usuario_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuario_bp)

    return app
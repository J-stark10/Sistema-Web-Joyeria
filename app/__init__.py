from flask import Flask
from config import config_dict
from app.extensions import *

from app.auth.login_manager import (init_login_manager)


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    init_login_manager(app)

    from app.auth.routes import auth_bp
    from app.core.dashboard import dashboard_bp
    from app.modules.usuarios.routes import usuario_bp
    from app.modules.clientes.routes import cliente_bp
    from app.modules.proveedores.routes import proveedor_bp
    from app.modules.materiales.routes import material_bp
    from app.modules.categorias.routes import categoria_bp
    from app.modules.joyas.routes import joya_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(joya_bp)

    return app
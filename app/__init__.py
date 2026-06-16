from flask import Flask
from config import config_dict
from app.extensions import *

from app.auth.login_manager import (init_login_manager)

from datetime import datetime, timedelta
from flask import session, redirect, url_for, flash
from flask_login import current_user, logout_user

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
    from app.modules.compras.routes import compra_bp
    from app.modules.ventas.routes import venta_bp
    from app.modules.inventario.routes import inventario_bp
    from app.modules.reportes.routes import reporte_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(proveedor_bp)
    app.register_blueprint(material_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(joya_bp)
    app.register_blueprint(compra_bp)
    app.register_blueprint(venta_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(reporte_bp)

    @app.before_request
    def verificar_inactividad():

        if not current_user.is_authenticated:
            return

        ahora = datetime.utcnow()

        ultima_actividad = session.get("ultima_actividad")

        if ultima_actividad:

            ultima_actividad = datetime.fromisoformat(ultima_actividad)

            if ahora - ultima_actividad > timedelta(minutes=30):

                logout_user()
                session.clear()
                flash("La sesión expiró por inactividad.","warning")

                return redirect(url_for("auth.login"))

        session["ultima_actividad"] = ahora.isoformat()

    return app
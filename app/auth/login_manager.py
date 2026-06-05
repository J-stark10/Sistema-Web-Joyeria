from flask_login import LoginManager

login_manager = LoginManager()

def init_login_manager(app):

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    login_manager.login_message = (
        "Debes iniciar sesión para acceder."
    )

    login_manager.login_message_category = (
        "warning"
    )

from app.modules.usuarios.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_by_id(int(user_id))
from app.modules.usuarios.models import Usuario
from werkzeug.security import check_password_hash

class AuthService:

    @staticmethod
    def autenticar(nombre_usuario, password):
        usuario = Usuario.get_by_username(nombre_usuario.strip())

        if not usuario:
            return None

        if not usuario.activo:
            return "INACTIVO"

        if not check_password_hash(usuario.contrasena_hash, password):
            return None

        return usuario
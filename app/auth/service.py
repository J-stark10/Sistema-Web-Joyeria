from app.modules.usuarios.services import UsuarioService

class AuthService:

    @staticmethod
    def autenticar(nombre_usuario, password):

        usuario = UsuarioService.obtener_por_username(
            nombre_usuario.strip()
        )

        if not usuario:
            return None

        if not usuario.activo:
            return "INACTIVO"

        if not usuario.check_password(password):
            return None

        return usuario
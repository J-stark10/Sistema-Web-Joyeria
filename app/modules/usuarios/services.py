from app.modules.usuarios.models import Usuario

class UsuarioService:

    @staticmethod
    def listar_usuarios():
        return Usuario.get_all()

    @staticmethod
    def obtener_usuario(id_usuario):
        return Usuario.get_by_id(id_usuario)

    @staticmethod
    def obtener_por_username(nombre_usuario):
        return Usuario.get_by_username(nombre_usuario)

    @staticmethod
    def crear_usuario( nombre_usuario,password, rol):

        usuario_existente = Usuario.get_by_username(nombre_usuario)

        if usuario_existente:
            raise ValueError("El nombre de usuario ya existe.")

        usuario = Usuario( nombre_usuario=nombre_usuario, rol=rol)
        usuario.set_password(password)
        usuario.save()

        return usuario

    @staticmethod
    def actualizar_usuario(id_usuario,nombre_usuario=None,rol=None,activo=None):

        usuario = Usuario.get_by_id(id_usuario)

        if not usuario:
            raise ValueError( "Usuario no encontrado.")

        if nombre_usuario:
            existente = Usuario.get_by_username(nombre_usuario)
            if ( existente and existente.id_usuario != id_usuario):
                raise ValueError("El nombre de usuario ya está en uso.")
            
        usuario.update( nombre_usuario=nombre_usuario,rol=rol,activo=activo)

        return usuario

    @staticmethod
    def cambiar_password(id_usuario, password):

        usuario = Usuario.get_by_id(id_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.update_password(password)

        return usuario

    @staticmethod
    def desactivar_usuario(id_usuario):

        usuario = Usuario.get_by_id(id_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.update(activo=False)

        return usuario

    @staticmethod
    def activar_usuario( id_usuario):
        usuario = Usuario.get_by_id(id_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado.")
        usuario.update(activo=True)

        return usuario

    @staticmethod
    def autenticar_usuario( nombre_usuario, password):

        usuario = Usuario.get_by_username(nombre_usuario)

        if not usuario:
            return None

        if not usuario.activo:
            return None

        if not usuario.check_password(password):
            return None

        return usuario
from app.modules.usuarios.models import Usuario

class UsuarioService:

    @staticmethod
    def listar_usuarios():
        return Usuario.get_all()

    @staticmethod
    def obtener_usuario(id_usuario):
        usuario = Usuario.get_by_id(id_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return usuario

    @staticmethod
    def obtener_por_username(nombre_usuario):
        return Usuario.get_by_username(nombre_usuario)

    @staticmethod
    def crear_usuario( nombre_usuario,password, rol):

        nombre_usuario = nombre_usuario.strip()

        if not nombre_usuario:
            raise ValueError("El nombre usuario es obligatorio.")
        
        if len(nombre_usuario) > 50:
            raise ValueError("El nombre de usuario no puede superar los 50 caracteres.")

        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        
        if rol not in ['ADMIN', 'VENDEDOR']:
            raise ValueError("El rol seleccionado no es válido.")

        if Usuario.get_by_username(nombre_usuario):
            raise ValueError("Ya existe un usuario con ese nombre.")

        usuario = Usuario( nombre_usuario=nombre_usuario, rol=rol)
        usuario.set_password(password)
        usuario.save()

        return usuario

    @staticmethod
    def actualizar_usuario(id_usuario, nombre_usuario, rol, activo):

        usuario = UsuarioService.obtener_usuario(id_usuario)
        nombre_usuario = nombre_usuario.strip()

        if not nombre_usuario:
            raise ValueError("El nombre de usuario es obligatorio.")

        if len(nombre_usuario) > 50:
            raise ValueError("El nombre de usuario no puede superar los 50 caracteres.")

        if rol not in ["ADMIN", "VENDEDOR"]:
            raise ValueError("El rol seleccionado no es válido.")

        existente = Usuario.get_by_username(nombre_usuario)

        if existente and existente.id_usuario != usuario.id_usuario:
            raise ValueError("Ya existe otro usuario con ese nombre.")

        usuario.update(nombre_usuario=nombre_usuario, rol=rol, activo=activo)

        return usuario

    @staticmethod
    def cambiar_password(id_usuario, password):

        usuario = UsuarioService.obtener_usuario(id_usuario)
        password = password.strip()

        if not password:
            raise ValueError("La contraseña es obligatoria.")
        
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        if not usuario:
            raise ValueError("Usuario no encontrado.")
        
        usuario.update_password(password)
        return usuario

    @staticmethod
    def desactivar_usuario(id_usuario):

        usuario = UsuarioService.obtener_usuario(id_usuario)

        if not usuario.activo:
            raise ValueError("El usuario ya se encuentra desactivado.")

        if not usuario:
            raise ValueError("Usuario no encontrado.")
        
        usuario.deactivate()
        return usuario

    @staticmethod
    def activar_usuario( id_usuario):

        usuario = UsuarioService.obtener_usuario(id_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if usuario.activo:
            raise ValueError("El usuario ya se encuentra activo.")
        
        usuario.restore()
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
    
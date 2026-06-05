from app.modules.proveedores.models import Proveedor

class ProveedorService:

    @staticmethod
    def listar_proveedores():
        return Proveedor.get_all()

    @staticmethod
    def listar_proveedores_activos():
        return Proveedor.get_activos()

    @staticmethod
    def obtener_proveedor(id_proveedor):
        proveedor = Proveedor.get_by_id(id_proveedor)

        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        return proveedor

    # ==========================
    # CREAR
    # ==========================

    @staticmethod
    def crear_proveedor(nombre_razon_social, nit, telefono, correo=None):

        existente = Proveedor.get_by_nit(nit)

        if existente:
            raise ValueError("Ya existe un proveedor con ese NIT.")

        proveedor = Proveedor(
            nombre_razon_social=nombre_razon_social.strip(),
            nit=nit.strip(),
            telefono=telefono.strip(),
            correo=correo.strip() if correo else None
        )

        proveedor.save()

        return proveedor

    # ==========================
    # ACTUALIZAR
    # ==========================

    @staticmethod
    def actualizar_proveedor(id_proveedor, nombre_razon_social, nit, telefono, correo=None, activo=True):

        proveedor = Proveedor.get_by_id(id_proveedor)

        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        otro_proveedor = Proveedor.get_by_nit(nit)

        if otro_proveedor and otro_proveedor.id_proveedor != proveedor.id_proveedor:
            raise ValueError("Ya existe otro proveedor con ese NIT.")

        proveedor.update(
            nombre_razon_social=nombre_razon_social.strip(),
            nit=nit.strip(),
            telefono=telefono.strip(),
            correo=correo.strip() if correo else None,
            activo=activo
        )

        return proveedor

    # ==========================
    # DESACTIVAR
    # ==========================

    @staticmethod
    def desactivar_proveedor(id_proveedor):

        proveedor = Proveedor.get_by_id(id_proveedor)

        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        proveedor.delete()

    # ==========================
    # ACTIVAR
    # ==========================

    @staticmethod
    def activar_proveedor(id_proveedor):

        proveedor = Proveedor.get_by_id(id_proveedor)

        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        proveedor.restore()
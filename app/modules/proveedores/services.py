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

    # CREAR
    @staticmethod
    def crear_proveedor(nombre_razon_social, nit, telefono, correo=None):

        nombre_razon_social = nombre_razon_social.strip()
        if not nombre_razon_social:
            raise ValueError("La razón social es obligatoria.")
        if len(nombre_razon_social) > 150:
            raise ValueError("La razón social no puede superar los 150 caracteres.")

        nit = nit.strip()
        if not nit:
            raise ValueError("El NIT es obligatorio.")
        if len(nit) > 30:
            raise ValueError("El NIT no puede superar los 30 caracteres.")
        
        telefono = telefono.strip()
        if not telefono:
            raise ValueError("El teléfono es obligatorio.")
        if len(telefono) > 20:
            raise ValueError("El teléfono no puede superar los 20 caracteres.")

        if correo and len(correo.strip()) > 30:
            raise ValueError("El correo no puede superar los 30 caracteres.")
        if correo and "@" not in correo:
            raise ValueError("El correo electrónico no es válido.")
        
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

    # ACTUALIZAR
    @staticmethod
    def actualizar_proveedor(id_proveedor, nombre_razon_social, nit, telefono, correo=None, activo=True):

        proveedor = ProveedorService.obtener_proveedor(id_proveedor)

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

    # DESACTIVAR
    @staticmethod
    def desactivar_proveedor(id_proveedor):

        proveedor = ProveedorService.obtener_proveedor(id_proveedor)

        if not proveedor.activo:
            raise ValueError("El proveedor ya se encuentra desactivado.")

        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        proveedor.delete()

    # ACTIVAR
    @staticmethod
    def activar_proveedor(id_proveedor):

        proveedor = ProveedorService.obtener_proveedor(id_proveedor)

        if proveedor.activo:
            raise ValueError("El proveedor ya se encuentra activo.")

        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        proveedor.restore()
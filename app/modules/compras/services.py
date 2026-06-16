from decimal import Decimal, InvalidOperation
from app.extensions import db

from app.modules.compras.models import Compra, DetalleCompra
from app.modules.proveedores.services import ProveedorService
from app.modules.usuarios.services import UsuarioService
from app.modules.joyas.services import JoyaService

class CompraService:

    @staticmethod
    def listar_compras():
        return Compra.get_all()

    @staticmethod
    def obtener_compra(id_compra):

        compra = Compra.get_by_id(id_compra)
        if not compra:
            raise ValueError("Compra no encontrada.")

        return compra

    # CREAR COMPRA
    @staticmethod
    def crear_compra(id_proveedor, id_usuario, detalles):

        proveedor = ProveedorService.obtener_proveedor(id_proveedor)
        if not proveedor.activo:
            raise ValueError("No es posible registrar compras con un proveedor inactivo.")

        usuario = UsuarioService.obtener_usuario(id_usuario)
        if not usuario.activo:
            raise ValueError("No es posible registrar compras con un usuario inactivo.")

        if not detalles:
            raise ValueError("Debe agregar al menos una joya a la compra.")
        total_compra = Decimal("0.00")

        compra = Compra(
            id_proveedor=id_proveedor,
            id_usuario=id_usuario,
            total_compra=0,
            estado="COMPLETADA"
        )

        db.session.add(compra)
        db.session.flush()

        for item in detalles:

            if not item.get("id_joya"):
                raise ValueError("Debe seleccionar una joya.")

            joya = JoyaService.obtener_joya(item["id_joya"])

            if not joya.activo:
                raise ValueError(
                    f"No es posible registrar la joya '{joya.nombre}' porque se encuentra inactiva."
                )

            try:
                cantidad = int(item["cantidad"])

            except (ValueError, TypeError):
                raise ValueError("La cantidad ingresada no es válida.")

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")

            try:
                precio = Decimal(str(item["precio_unit_compra"]))

            except (InvalidOperation, ValueError, TypeError):
                raise ValueError("El precio de compra ingresado no es válido.")

            if precio <= 0:
                raise ValueError("El precio de compra debe ser mayor a cero.")

            subtotal = cantidad * precio

            detalle = DetalleCompra(
                id_compra=compra.id_compra,
                id_joya=joya.id_joya,
                cantidad=cantidad,
                precio_unit_compra=precio,
                subtotal=subtotal
            )

            db.session.add(detalle)

            joya.stock_actual += cantidad
            joya.precio_compra = precio

            total_compra += subtotal

        compra.total_compra = total_compra

        db.session.commit()

        return compra

    # ANULAR COMPRA
    @staticmethod
    def anular_compra(id_compra):

        compra = CompraService.obtener_compra(id_compra)

        if compra.estado == "ANULADA":
            raise ValueError("La compra ya fue anulada.")

        for detalle in compra.detalles:

            joya = JoyaService.obtener_joya(detalle.id_joya)

            if joya.stock_actual < detalle.cantidad:
                raise ValueError(
                    f"No es posible anular la compra porque la joya '{joya.nombre}' ya no cuenta con stock suficiente."
                )

            joya.stock_actual -= detalle.cantidad

        compra.anular()

        return compra
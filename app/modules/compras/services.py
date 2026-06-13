from decimal import Decimal

from app.extensions import db

from app.modules.compras.models import Compra, DetalleCompra
from app.modules.proveedores.models import Proveedor
from app.modules.usuarios.models import Usuario
from app.modules.joyas.models import Joya

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

    # ==========================
    # CREAR COMPRA
    # ==========================

    @staticmethod
    def crear_compra(id_proveedor, id_usuario, detalles):

        proveedor = Proveedor.get_by_id(id_proveedor)
        if not proveedor:
            raise ValueError("Proveedor no encontrado.")

        usuario = Usuario.get_by_id(id_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado.")

        if not detalles:
            raise ValueError("Debe agregar al menos un producto.")

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

            joya = Joya.get_by_id(item["id_joya"])
            if not joya:
                raise ValueError("Joya no encontrada.")
            cantidad = int(item["cantidad"])
            precio = Decimal(str(item["precio_unit_compra"]))

            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a cero.")

            if precio <= 0:
                raise ValueError("El precio debe ser mayor a cero.")

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

    # ==========================
    # ANULAR COMPRA
    # ==========================

    @staticmethod
    def anular_compra(id_compra):

        compra = Compra.get_by_id(id_compra)
        if not compra:
            raise ValueError("Compra no encontrada.")

        if compra.estado == "ANULADA":
            raise ValueError("La compra ya fue anulada.")

        for detalle in compra.detalles:
            joya = Joya.get_by_id(detalle.id_joya)
            joya.stock_actual -= detalle.cantidad
            if joya.stock_actual < 0:
                joya.stock_actual = 0

        compra.anular()
        db.session.commit()

        return compra
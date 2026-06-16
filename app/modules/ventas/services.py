from decimal import Decimal
from app import db

from app.modules.ventas.models import Venta, DetalleVenta
from app.modules.joyas.services import JoyaService
from app.modules.usuarios.services import UsuarioService
from app.modules.clientes.services import ClienteService


class VentaService:
    # LISTAR
    @staticmethod
    def listar_ventas():
        return Venta.get_all()

    # OBTENER
    @staticmethod
    def obtener_venta(id_venta):
        return Venta.get_by_id(id_venta)

    # CREAR
    @staticmethod
    def crear_venta(
        id_usuario,
        id_cliente,
        items
    ):
        try:
            usuario = UsuarioService.obtener_usuario( id_usuario)
            if not usuario.activo:
                raise ValueError("No es posible registrar ventas con un usuario inactivo.")

            cliente = None

            if id_cliente:

                cliente = ClienteService.obtener_cliente(id_cliente)

                if not cliente.activo:
                    raise ValueError("No es posible registrar ventas para un cliente inactivo.")

            if not items:
                raise ValueError("Debe agregar al menos una joya.")

            venta = Venta(
                id_usuario=usuario.id_usuario,
                id_cliente=cliente.id_cliente if cliente else None,
                total_venta=Decimal("0.00"),
                estado="COMPLETADA"
            )

            db.session.add(venta)
            db.session.flush()

            total = Decimal("0.00")

            for item in items:

                joya = JoyaService.obtener_joya(
                    item["id_joya"]
                )

                if not joya.activo:
                    raise ValueError(f"La joya '{joya.nombre}' se encuentra inactiva.")

                try:
                    cantidad = int(item["cantidad"])

                except (ValueError, TypeError):
                    raise ValueError(f"Cantidad inválida para {joya.nombre}.")

                if cantidad <= 0:
                    raise ValueError(f"La cantidad para {joya.nombre} debe ser mayor a cero.")

                try:
                    precio = Decimal(str(item["precio"]))

                except:
                    raise ValueError(f"Precio inválido para {joya.nombre}.")

                if precio <= 0:
                    raise ValueError( f"El precio para {joya.nombre} debe ser mayor a cero.")

                if joya.stock_actual < cantidad:
                    raise ValueError(f"Stock insuficiente para {joya.nombre}.")

                subtotal = (
                    Decimal(cantidad) * precio
                ).quantize(
                    Decimal("0.01")
                )

                detalle = DetalleVenta(
                    id_venta=venta.id_venta,
                    id_joya=joya.id_joya,
                    cantidad=cantidad,
                    precio_unit_venta=precio,
                    subtotal=subtotal
                )

                db.session.add(detalle)
                joya.disminuir_stock(cantidad)
                total += subtotal

            venta.total_venta = total.quantize( Decimal("0.01"))

            db.session.commit()
            return venta
        
        except Exception as e:
            db.session.rollback()
            raise e

    # ANULAR
    @staticmethod
    def anular_venta(id_venta):
        try:
            venta = Venta.query.get(id_venta)
            if not venta:
                raise ValueError("Venta no encontrada.")

            if venta.estado == "ANULADA":
                raise ValueError("La venta ya fue anulada.")

            for detalle in venta.detalles:
                joya = JoyaService.obtener_joya(detalle.id_joya)
                joya.aumentar_stock( detalle.cantidad)

            venta.anular()
            db.session.commit()
            return venta

        except Exception as e:
            db.session.rollback()
            raise e
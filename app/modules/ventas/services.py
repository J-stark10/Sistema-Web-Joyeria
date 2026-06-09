from app.modules.ventas.models import Venta, DetalleVenta
from app.modules.joyas.models import Joya

from decimal import Decimal

from app import db

class VentaService:

    @staticmethod
    def listar_ventas():
        return Venta.query.order_by(Venta.fecha_venta.desc()).all()

    @staticmethod
    def obtener_venta(id_venta):

        venta = Venta.query.get(id_venta)
        if not venta:
            raise ValueError("Venta no encontrada")

        return venta

    @staticmethod
    def crear_venta(id_usuario, id_cliente, items):
        try:            
            venta = Venta(
                id_usuario=int(id_usuario),
                id_cliente=int(id_cliente),
                total_venta=0
            )

            db.session.add(venta)

            total = 0

            for item in items:
                joya = Joya.query.get(int(item["id_joya"]))

                if not joya:
                    raise ValueError("Joya no encontrada")
                
                cantidad = int(item["cantidad"])
                precio = Decimal(str(item["precio"]))

                if joya.stock_actual < cantidad:
                    raise ValueError(f"Stock insuficiente para {joya.nombre}")

                subtotal = (Decimal(cantidad) * precio).quantize(Decimal("0.01"))
                

                detalle = DetalleVenta(
                    venta=venta,
                    joya=joya,
                    cantidad=item["cantidad"],
                    precio_unit_venta=item["precio"],
                    subtotal=subtotal
                )

                db.session.add(detalle)

                joya.disminuir_stock(item["cantidad"])
                total += subtotal

            venta.total_venta = total.quantize(Decimal("0.01")) # Redondeamos

            db.session.commit()
            return venta

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def anular_venta(id_venta):
        try:
            venta = Venta.query.get(id_venta)

            if not venta:
                raise ValueError("Venta no encontrada")

            if venta.estado == "ANULADA":
                raise ValueError("La venta ya está anulada")

            for detalle in venta.detalles:
                detalle.joya.stock_actual += detalle.cantidad

            venta.estado = "ANULADA"

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
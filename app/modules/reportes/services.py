from sqlalchemy import func

from app.modules.ventas.models import Venta, DetalleVenta
from app.modules.joyas.models import Joya
from app.modules.categorias.models import Categoria


class ReporteService:

    # ==========================
    # REPORTE DE VENTAS
    # ==========================

    @staticmethod
    def reporte_ventas(fecha_inicio, fecha_fin):

        ventas = Venta.query.filter(
            Venta.estado == "COMPLETADA",
            func.date(Venta.fecha_venta) >= fecha_inicio,
            func.date(Venta.fecha_venta) <= fecha_fin
        ).order_by(Venta.fecha_venta.desc()).all()

        total_ventas = sum(float(v.total_venta) for v in ventas)

        return {
            "ventas": ventas,
            "total_ventas": total_ventas
        }

    # ==========================
    # REPORTE INVENTARIO
    # ==========================

    @staticmethod
    def reporte_inventario():

        joyas = Joya.query.filter_by(activo=True).order_by(Joya.nombre).all()

        total_inventario = 0

        for joya in joyas:
            total_inventario += float(joya.precio_compra) * joya.stock_actual

        return {
            "joyas": joyas,
            "total_inventario": total_inventario
        }

    # ==========================
    # REPORTE RENTABILIDAD
    # ==========================

    @staticmethod
    def reporte_rentabilidad(fecha_inicio, fecha_fin, id_categoria):

        categoria = Categoria.get_by_id(id_categoria)

        if not categoria:
            raise ValueError("Categoría no encontrada.")

        detalles = DetalleVenta.query.join(Venta).join(Joya).filter(
            Venta.estado == "COMPLETADA",
            Joya.id_categoria == id_categoria,
            func.date(Venta.fecha_venta) >= fecha_inicio,
            func.date(Venta.fecha_venta) <= fecha_fin
        ).all()

        datos = []

        utilidad_total = 0

        for detalle in detalles:

            costo_total = float(detalle.joya.precio_compra) * detalle.cantidad

            venta_total = float(detalle.subtotal)

            utilidad = venta_total - costo_total

            utilidad_total += utilidad

            datos.append({
                "joya": detalle.joya,
                "cantidad": detalle.cantidad,
                "costo_total": costo_total,
                "venta_total": venta_total,
                "utilidad": utilidad
            })

        return {
            "categoria": categoria,
            "datos": datos,
            "utilidad_total": utilidad_total
        }
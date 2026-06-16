from datetime import date, timedelta

from flask import Blueprint, render_template
from flask_login import login_required

from sqlalchemy import func, extract

from app.extensions import db

from app.modules.ventas.models import Venta, DetalleVenta
from app.modules.compras.models import Compra
from app.modules.joyas.models import Joya
from app.modules.clientes.models import Cliente
from app.modules.proveedores.models import Proveedor

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/"
)


def _pct_change(actual, anterior):
    """None = sin dato anterior (division by zero).
       Se distingue del caso anterior==0 en el caller."""
    if anterior == 0:
        return None
    return round(((actual - anterior) / anterior) * 100, 1)


@dashboard_bp.route("/")
@login_required
def index():

    hoy = date.today()
    ayer = hoy - timedelta(days=1)

    mes_actual  = hoy.month
    anio_actual = hoy.year

    if mes_actual == 1:
        mes_anterior  = 12
        anio_anterior = anio_actual - 1
    else:
        mes_anterior  = mes_actual - 1
        anio_anterior = anio_actual

    # ==========================
    # Ventas del día vs ayer
    # ==========================

    ventas_dia = (
        db.session.query(
            func.coalesce(func.sum(Venta.total_venta), 0)
        )
        .filter(
            func.date(Venta.fecha_venta) == hoy,
            Venta.estado == "COMPLETADA"
        )
        .scalar()
    )

    ventas_ayer = (
        db.session.query(
            func.coalesce(func.sum(Venta.total_venta), 0)
        )
        .filter(
            func.date(Venta.fecha_venta) == ayer,
            Venta.estado == "COMPLETADA"
        )
        .scalar()
    )

    ventas_ayer_cero = (ventas_ayer==0)
    ventas_dia_pct = _pct_change(ventas_dia, ventas_ayer)

    # ==========================
    # Compras del mes vs anterior
    # ==========================

    compras_mes = (
        db.session.query(
            func.coalesce(func.sum(Compra.total_compra), 0)
        )
        .filter(
            extract("month", Compra.fecha_compra) == mes_actual,
            extract("year",  Compra.fecha_compra) == anio_actual,
            Compra.estado == "COMPLETADA"
        )
        .scalar()
    )

    compras_mes_anterior = (
        db.session.query(
            func.coalesce(func.sum(Compra.total_compra), 0)
        )
        .filter(
            extract("month", Compra.fecha_compra) == mes_anterior,
            extract("year",  Compra.fecha_compra) == anio_anterior,
            Compra.estado == "COMPLETADA"
        )
        .scalar()
    )

    compras_mes_pct = _pct_change(compras_mes, compras_mes_anterior)

    # ==========================
    # Total clientes + altas mes
    # ==========================

    total_clientes = Cliente.query.count()

    clientes_nuevos_mes = (
        Cliente.query
        .filter(
            extract("month", Cliente.fecha_registro) == mes_actual,
            extract("year",  Cliente.fecha_registro) == anio_actual,
        )
        .count()
    )

    # ==========================
    # Stock bajo
    # ==========================

    stock_bajo_count = (
        Joya.query
        .filter(
            Joya.stock_actual <= Joya.stock_minimo,
            Joya.activo == True
        )
        .count()
    )

    # ==========================
    # Joya más vendida del mes
    # via detalle_venta → joya
    # ==========================

    joya_top = (
        db.session.query(
            Joya.nombre,
            Joya.codigo,
            func.sum(DetalleVenta.cantidad).label("total_vendido")
        )
        .join(DetalleVenta, DetalleVenta.id_joya == Joya.id_joya)
        .join(Venta, Venta.id_venta == DetalleVenta.id_venta)
        .filter(
            extract("month", Venta.fecha_venta) == mes_actual,
            extract("year",  Venta.fecha_venta) == anio_actual,
            Venta.estado == "COMPLETADA"
        )
        .group_by(Joya.id_joya, Joya.nombre, Joya.codigo)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .first()
    )

    if joya_top:
        joya_top_nombre  = joya_top.nombre
        joya_top_codigo  = joya_top.codigo
        joya_top_vendido = int(joya_top.total_vendido)
    else:
        joya_top_nombre  = None
        joya_top_codigo  = None
        joya_top_vendido = 0

    # ==========================
    # Ventas mensuales (barras)
    # ==========================

    ventas_mensuales = [0] * 12

    res_ventas = (
        db.session.query(
            extract("month", Venta.fecha_venta),
            func.sum(Venta.total_venta)
        )
        .filter(
            extract("year", Venta.fecha_venta) == anio_actual,
            Venta.estado == "COMPLETADA"
        )
        .group_by(extract("month", Venta.fecha_venta))
        .all()
    )

    for mes, total in res_ventas:
        ventas_mensuales[int(mes) - 1] = float(total)

    # ==========================
    # Compras mensuales (línea)
    # ==========================

    compras_mensuales = [0] * 12

    res_compras = (
        db.session.query(
            extract("month", Compra.fecha_compra),
            func.sum(Compra.total_compra)
        )
        .filter(
            extract("year", Compra.fecha_compra) == anio_actual,
            Compra.estado == "COMPLETADA"
        )
        .group_by(extract("month", Compra.fecha_compra))
        .all()
    )

    for mes, total in res_compras:
        compras_mensuales[int(mes) - 1] = float(total)

    meses_labels = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]

    # ==========================
    # Últimas ventas
    # ==========================

    ventas = (
        Venta.query
        .order_by(Venta.fecha_venta.desc())
        .limit(5)
        .all()
    )

    ultimas_ventas = []

    for venta in ventas:
        ultimas_ventas.append({
            "cliente_nombre":
                venta.cliente.nombre
                if venta.cliente
                else "Cliente Directo",
            "fecha":  venta.fecha_venta,
            "total":  float(venta.total_venta),
            "estado": venta.estado.lower()
        })

    return render_template(
        "dashboard/index.html",

        # KPI ventas
        ventas_dia=float(ventas_dia),
        ventas_dia_pct=ventas_dia_pct,

        # KPI compras
        compras_mes=float(compras_mes),
        compras_mes_pct=compras_mes_pct,

        # KPI clientes
        total_clientes=total_clientes,
        clientes_nuevos_mes=clientes_nuevos_mes,

        # KPI stock
        stock_bajo_count=stock_bajo_count,

        # KPI joya top
        joya_top_nombre=joya_top_nombre,
        joya_top_codigo=joya_top_codigo,
        joya_top_vendido=joya_top_vendido,

        # Gráfico dual
        meses_labels=meses_labels,
        ventas_mensuales=ventas_mensuales,
        compras_mensuales=compras_mensuales,

        # Tabla
        ultimas_ventas=ultimas_ventas,
        ventas_ayer_cero=ventas_ayer_cero
    )

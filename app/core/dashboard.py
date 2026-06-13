from datetime import date, datetime

from flask import Blueprint, render_template
from flask_login import login_required

from sqlalchemy import func, extract

from app.extensions import db

from app.modules.ventas.models import Venta
from app.modules.compras.models import Compra
from app.modules.joyas.models import Joya
from app.modules.clientes.models import Cliente
from app.modules.proveedores.models import Proveedor

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/"
)


@dashboard_bp.route("/")
@login_required
def index():

    hoy = date.today()

    # ==========================
    # Ventas del día
    # ==========================

    ventas_dia = (
        db.session.query(
            func.coalesce(
                func.sum(Venta.total_venta),
                0
            )
        )
        .filter(
            func.date(Venta.fecha_venta) == hoy,
            Venta.estado == "COMPLETADA"
        )
        .scalar()
    )

    # ==========================
    # Compras del mes
    # ==========================

    compras_mes = (
        db.session.query(
            func.coalesce(
                func.sum(Compra.total_compra),
                0
            )
        )
        .filter(
            extract(
                "month",
                Compra.fecha_compra
            ) == hoy.month,
            extract(
                "year",
                Compra.fecha_compra
            ) == hoy.year,
            Compra.estado == "COMPLETADA"
        )
        .scalar()
    )

    # ==========================
    # Total clientes
    # ==========================

    total_clientes = Cliente.query.count()

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
    # Ventas mensuales
    # ==========================

    ventas_mensuales = [0] * 12

    resultados = (
        db.session.query(
            extract(
                "month",
                Venta.fecha_venta
            ),
            func.sum(
                Venta.total_venta
            )
        )
        .filter(
            extract(
                "year",
                Venta.fecha_venta
            ) == hoy.year,
            Venta.estado == "COMPLETADA"
        )
        .group_by(
            extract(
                "month",
                Venta.fecha_venta
            )
        )
        .all()
    )

    for mes, total in resultados:

        ventas_mensuales[
            int(mes) - 1
        ] = float(total)

    meses_labels = [
        "Ene",
        "Feb",
        "Mar",
        "Abr",
        "May",
        "Jun",
        "Jul",
        "Ago",
        "Sep",
        "Oct",
        "Nov",
        "Dic"
    ]

    # ==========================
    # Últimas ventas
    # ==========================

    ventas = (
        Venta.query
        .order_by(
            Venta.fecha_venta.desc()
        )
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

            "fecha":
                venta.fecha_venta,

            "total":
                float(
                    venta.total_venta
                ),

            "estado":
                venta.estado.lower()
        })

    return render_template(
        "dashboard/index.html",

        ventas_dia=float(ventas_dia),

        compras_mes=float(compras_mes),

        total_clientes=total_clientes,

        stock_bajo_count=stock_bajo_count,

        meses_labels=meses_labels,

        ventas_mensuales=ventas_mensuales,

        ultimas_ventas=ultimas_ventas
    )
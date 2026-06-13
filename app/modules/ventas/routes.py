from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from decimal import Decimal
from app.modules.ventas.services import VentaService
from app.modules.clientes.models import Cliente
from app.modules.joyas.models import Joya


venta_bp = Blueprint("venta", __name__, url_prefix="/ventas")


@venta_bp.route("/")
def index():

    ventas = VentaService.listar_ventas()
    return render_template(
        "ventas/index.html",
        ventas=ventas
    )


@venta_bp.route("/crear", methods=["GET", "POST"])
def crear():

    if request.method == "POST":
        try:
            items = []
            ids = request.form.getlist("id_joya[]")
            cantidades = request.form.getlist("cantidad[]")
            precios = request.form.getlist("precio[]")

            for i in range(len(ids)):

                items.append({
                    "id_joya": int(ids[i]),
                    "cantidad": int(cantidades[i]),
                    "precio": Decimal(precios[i])
                })

            VentaService.crear_venta(
                id_usuario=current_user.id_usuario,
                id_cliente=int(request.form.get("id_cliente")),
                items=items
            )
            flash("Venta registrada correctamente", "success")
            return redirect(url_for("venta.index"))

        except ValueError as e:
            flash(str(e), "danger")

    clientes = Cliente.query.all()
    joyas = Joya.query.filter_by(activo=True).all()

    return render_template(
        "ventas/crear.html",
        clientes=clientes,
        joyas=joyas
    )


@venta_bp.route("/detalle/<int:id_venta>")
def detalle(id_venta):

    try:
        venta = VentaService.obtener_venta(id_venta)
    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("venta.index"))

    return render_template(
        "ventas/detalle.html",
        venta=venta
    )


@venta_bp.route("/anular/<int:id_venta>")
def anular(id_venta):

    try:
        VentaService.anular_venta(id_venta)
        flash("Venta anulada correctamente", "warning")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("venta.index"))






from flask import jsonify
from app import db

@venta_bp.route("/buscar-joya")
def buscar_joya():

    q = request.args.get("q", "")

    joyas = Joya.query.filter(
        db.or_(
            Joya.codigo.ilike(f"%{q}%"),
            Joya.nombre.ilike(f"%{q}%")
        )
    ).limit(10).all()

    return jsonify([
        {
            "id": j.id_joya,
            "codigo": j.codigo,
            "nombre": j.nombre,
            "stock": j.stock_actual,
            "precio": float(j.precio_venta)
        }
        for j in joyas
    ])
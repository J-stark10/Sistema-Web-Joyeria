from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

from app.modules.compras.services import CompraService
from app.modules.proveedores.models import Proveedor
from app.modules.joyas.models import Joya

compra_bp = Blueprint('compra', __name__, url_prefix='/compras')

@compra_bp.route("/")
def index():
    compras = CompraService.listar_compras()
    return render_template("compras/index.html", compras=compras)

@compra_bp.route("/crear", methods=["GET", "POST"])
def crear():
    proveedores = Proveedor.get_all()
    joyas = Joya.get_activos()

    if request.method == "POST":
        try:
            id_proveedor = request.form["id_proveedor"]

            ids_joya = request.form.getlist("id_joya[]")
            cantidades = request.form.getlist("cantidad[]")
            precios = request.form.getlist("precio[]")

            detalles = []

            for i in range(len(ids_joya)):
                detalles.append({
                    "id_joya": ids_joya[i],
                    "cantidad": cantidades[i],
                    "precio_unit_compra": precios[i]
                })

            compra = CompraService.crear_compra(
                id_proveedor=id_proveedor,
                id_usuario=current_user.id_usuario,
                detalles=detalles
            )
            flash("Compra registrada correctamente.", "success")
            return redirect(url_for("compra.detalle", id_compra=compra.id_compra))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "compras/crear.html",
        proveedores=proveedores,
        joyas=joyas
    )

@compra_bp.route("/detalle/<int:id_compra>")
def detalle(id_compra):
    try:
        compra = CompraService.obtener_compra(id_compra)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("compra.index"))

    return render_template(
        "compras/detalle.html",
        compra=compra
    )

@compra_bp.route("/anular/<int:id_compra>")
def anular(id_compra):
    try:
        CompraService.anular_compra(id_compra)
        flash("Compra anulada correctamente.", "warning")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("compra.index"))
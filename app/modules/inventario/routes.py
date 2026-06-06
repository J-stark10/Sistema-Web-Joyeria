from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user

from app.modules.inventario.services import InventarioService
from app.modules.joyas.services import JoyaService

inventario_bp = Blueprint("inventario", __name__, url_prefix="/inventario")

@inventario_bp.route("/")
def index():

    ajustes = InventarioService.listar_ajustes()

    return render_template(
        "inventario/index.html",
        ajustes=ajustes
    )

@inventario_bp.route("/stock-bajo")
def stock_bajo():

    joyas = InventarioService.listar_stock_bajo()

    return render_template(
        "inventario/stock_bajo.html",
        joyas=joyas
    )

@inventario_bp.route("/ajustar", methods=["GET", "POST"])
def ajustar():

    joyas = JoyaService.listar_joyas_activas()

    if request.method == "POST":

        try:

            InventarioService.registrar_ajuste(
                request.form["id_joya"],
                current_user.id_usuario,
                request.form["cantidad"],
                request.form["motivo"],
                request.form["tipo_ajuste"]
            )

            flash(
                "Ajuste de inventario registrado correctamente.",
                "success"
            )

            return redirect(url_for("inventario.index"))

        except ValueError as e:

            flash(str(e), "danger")

    return render_template(
        "inventario/ajustar.html",
        joyas=joyas
    )

@inventario_bp.route("/joya/<int:id_joya>")
def historial(id_joya):

    try:

        joya = JoyaService.obtener_joya(id_joya)

    except ValueError as e:

        flash(str(e), "danger")

        return redirect(url_for("inventario.index"))

    ajustes = joya.ajustes

    return render_template(
        "inventario/historial.html",
        joya=joya,
        ajustes=ajustes
    )
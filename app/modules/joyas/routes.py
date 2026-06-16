from flask import Blueprint, render_template, redirect, url_for, flash, request

from app.modules.joyas.services import JoyaService
from app.modules.categorias.models import Categoria
from app.modules.materiales.models import Material

joya_bp = Blueprint('joya', __name__, url_prefix='/joyas')

@joya_bp.route("/")
def index():

    joyas = JoyaService.listar_joyas()

    return render_template("joyas/index.html", joyas=joyas)

@joya_bp.route("/crear", methods=["GET", "POST"])
def crear():

    categorias = Categoria.get_all()
    materiales = Material.get_all()

    if request.method == "POST":
        try:
            JoyaService.crear_joya(
                codigo=request.form["codigo"],
                nombre=request.form["nombre"],
                id_categoria=request.form["id_categoria"],
                id_material=request.form["id_material"],
                precio_compra=request.form["precio_compra"],
                precio_venta=request.form["precio_venta"],
                stock_minimo=request.form["stock_minimo"]
            )
            flash("Joya creada correctamente.", "success")

            return redirect(url_for("joya.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "joyas/crear.html",
        categorias=categorias,
        materiales=materiales
    )

@joya_bp.route("/editar/<int:id_joya>", methods=["GET", "POST"])
def editar(id_joya):

    try:
        joya = JoyaService.obtener_joya(id_joya)

    except ValueError as e:
        flash(str(e), "danger")

        return redirect(url_for("joya.index"))

    categorias = Categoria.get_all()
    materiales = Material.get_all()

    if request.method == "POST":
        try:
            JoyaService.actualizar_joya(
                id_joya=id_joya,
                codigo=request.form["codigo"],
                nombre=request.form["nombre"],
                id_categoria=request.form["id_categoria"],
                id_material=request.form["id_material"],
                precio_compra=request.form["precio_compra"],
                precio_venta=request.form["precio_venta"],
                stock_minimo=request.form["stock_minimo"],
                activo="activo" in request.form
            )

            flash("Joya actualizada correctamente.", "success")
            return redirect(url_for("joya.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "joyas/editar.html",
        joya=joya,
        categorias=categorias,
        materiales=materiales
    )


@joya_bp.route("/desactivar/<int:id_joya>")
def desactivar(id_joya):
    try:
        JoyaService.desactivar_joya(id_joya)
        flash("Joya desactivada correctamente.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("joya.index"))

@joya_bp.route("/activar/<int:id_joya>")
def activar(id_joya):
    try:
        JoyaService.activar_joya(id_joya)
        flash("Joya activada correctamente.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("joya.index"))
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.modules.categorias.services import CategoriaService

categoria_bp = Blueprint('categoria', __name__, url_prefix='/categorias')

@categoria_bp.route("/")
def index():
    categorias = CategoriaService.listar_categorias()
    return render_template("categorias/index.html", categorias=categorias)

@categoria_bp.route("/crear", methods=["GET", "POST"])
def crear():

    if request.method == "POST":
        try:
            CategoriaService.crear_categoria(
                nombre_categoria=request.form["nombre_categoria"]
            )

            flash("Categoria registrada correctamente.", "success")
            return redirect(url_for("categoria.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("categorias/crear.html")

@categoria_bp.route("/editar/<int:id_categoria>", methods=["GET", "POST"])
def editar(id_categoria):

    try:
        categoria = CategoriaService.obtener_categoria(id_categoria)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("categoria.index"))

    if request.method == "POST":
        try:
            CategoriaService.actualizar_categoria(
                id_categoria=id_categoria,
                nombre_categoria=request.form["nombre_categoria"]
            )
            flash("Categoria actualizada correctamente.", "success")
            return redirect(url_for("categoria.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("categorias/editar.html", categoria=categoria)

@categoria_bp.route("/eliminar/<int:id_categoria>")
def eliminar(id_categoria):
    try:
        CategoriaService.eliminar_categoria(id_categoria)
        flash("Categoria eliminada correctamente.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("categoria.index"))
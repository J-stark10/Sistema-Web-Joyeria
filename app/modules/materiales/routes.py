from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.auth.decorators import roles_required
from app.modules.materiales.services import MaterialService

material_bp = Blueprint('material', __name__, url_prefix='/materiales')

@material_bp.route("/")
@login_required
@roles_required('ADMIN')
def index():
    materiales = MaterialService.listar_materiales()
    return render_template("materiales/index.html", materiales=materiales)

@material_bp.route("/crear", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def crear():

    if request.method == "POST":

        try:
            MaterialService.crear_material(
                nombre_material=request.form["nombre_material"]
            )
            flash("Material creado correctamente.", "success")
            return redirect(url_for("material.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("materiales/crear.html")

@material_bp.route("/editar/<int:id_material>", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def editar(id_material):

    try:
        material = MaterialService.obtener_material(id_material)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("material.index"))

    if request.method == "POST":

        try:
            MaterialService.actualizar_material(
                id_material=id_material,
                nombre_material=request.form["nombre_material"]
            )
            flash("Material actualizado correctamente.", "success")
            return redirect(url_for("material.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("materiales/editar.html", material=material)

@material_bp.route("/eliminar/<int:id_material>")
@login_required
@roles_required('ADMIN')
def eliminar(id_material):

    try:
        MaterialService.eliminar_material(id_material)
        flash("Material eliminado correctamente.", "warning")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("material.index"))
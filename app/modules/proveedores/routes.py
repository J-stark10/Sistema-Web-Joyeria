from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.auth.decorators import roles_required

from app.modules.proveedores.services import ProveedorService

proveedor_bp = Blueprint('proveedor', __name__, url_prefix='/proveedores')

@proveedor_bp.route("/")
@login_required
@roles_required('ADMIN')
def index():
    proveedores = ProveedorService.listar_proveedores()
    return render_template("proveedores/index.html", proveedores=proveedores)

@proveedor_bp.route("/crear", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def crear():

    if request.method == "POST":
        try:
            ProveedorService.crear_proveedor(
                nombre_razon_social=request.form["nombre_razon_social"],
                nit=request.form["nit"],
                telefono=request.form["telefono"],
                correo=request.form.get("correo")
            )
            flash("Proveedor creado correctamente.", "success")
            return redirect(url_for("proveedor.index"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("proveedores/crear.html")

@proveedor_bp.route("/editar/<int:id_proveedor>", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def editar(id_proveedor):

    try:
        proveedor = ProveedorService.obtener_proveedor(id_proveedor)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("proveedor.index"))

    if request.method == "POST":
        try:
            ProveedorService.actualizar_proveedor(
                id_proveedor=id_proveedor,
                nombre_razon_social=request.form["nombre_razon_social"],
                nit=request.form["nit"],
                telefono=request.form["telefono"],
                correo=request.form.get("correo"),
                activo="activo" in request.form
            )
            flash("Proveedor actualizado correctamente.", "success")
            return redirect(url_for("proveedor.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("proveedores/editar.html", proveedor=proveedor)

@proveedor_bp.route("/desactivar/<int:id_proveedor>")
@login_required
@roles_required('ADMIN')
def desactivar(id_proveedor):
    try:
        ProveedorService.desactivar_proveedor(id_proveedor)
        flash("Proveedor desactivado correctamente.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("proveedor.index"))

@proveedor_bp.route("/activar/<int:id_proveedor>")
@login_required
@roles_required('ADMIN')
def activar(id_proveedor):
    try:
        ProveedorService.activar_proveedor(id_proveedor)
        flash("Proveedor activado correctamente.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("proveedor.index"))
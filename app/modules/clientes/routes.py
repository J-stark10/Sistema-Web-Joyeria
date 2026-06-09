from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.modules.clientes.services import ClienteService

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route("/")
def index():
    clientes = ClienteService.listar_clientes()
    return render_template("clientes/index.html", clientes=clientes)


@cliente_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        try:
            ClienteService.crear_cliente(
                nombre=request.form["nombre"],
                ci_nit=request.form["ci_nit"],
                telefono=request.form.get("telefono"),
                direccion=request.form.get("direccion")
            )
            flash("Cliente creado correctamente.", "success")
            return redirect(url_for("cliente.index"))
        
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("clientes/crear.html")


@cliente_bp.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar(id_cliente):

    cliente = ClienteService.obtener_cliente(id_cliente)

    if not cliente:
        flash("Cliente no encontrado.", "danger")
        return redirect(url_for("cliente.index"))

    if request.method == "POST":
        try:
            ClienteService.actualizar_cliente(
                id_cliente=id_cliente,
                nombre=request.form["nombre"],
                ci_nit=request.form["ci_nit"],
                telefono=request.form.get("telefono"),
                direccion=request.form.get("direccion"),
                activo="activo" in request.form
            )
            flash("Cliente actualizado correctamente.", "success")
            return redirect(url_for("cliente.index"))

        except ValueError as e:
            flash(str(e), "danger")

    return render_template("clientes/editar.html", cliente=cliente)


@cliente_bp.route("/desactivar/<int:id_cliente>")
def desactivar(id_cliente):

    try:
        ClienteService.desactivar_cliente(id_cliente)
        flash("Cliente desactivado.", "warning")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("cliente.index"))


@cliente_bp.route("/activar/<int:id_cliente>")
def activar(id_cliente):

    try:
        ClienteService.activar_cliente(id_cliente)
        flash("Cliente activado.", "success")

    except ValueError as e:
        flash(str(e), "danger")

    return redirect(url_for("cliente.index"))
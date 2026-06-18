from decimal import Decimal

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)
from flask_login import login_required, current_user

from app import db
from app.auth.decorators import roles_required

from app.modules.ventas.services import VentaService
from app.modules.clientes.services import ClienteService
from app.modules.joyas.services import JoyaService
from app.modules.joyas.models import Joya


venta_bp = Blueprint("venta",__name__, url_prefix="/ventas")

# LISTADO
@venta_bp.route("/")
@login_required
@roles_required('ADMIN','VENDEDOR')
def index():
    ventas = VentaService.listar_ventas()

    return render_template( "ventas/index.html",ventas=ventas)

# CREAR VENTA
@venta_bp.route("/crear", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN','VENDEDOR')
def crear():

    if request.method == "POST":
        try:
            items = []

            ids = request.form.getlist("id_joya[]")
            cantidades = request.form.getlist("cantidad[]")
            precios = request.form.getlist("precio[]")

            if not ids:
                raise ValueError("Debe agregar al menos una joya.")

            for i in range(len(ids)):

                items.append({
                    "id_joya": int(ids[i]),
                    "cantidad": int(cantidades[i]),
                    "precio": Decimal(precios[i])
                })

            id_cliente = request.form.get(
                "id_cliente"
            )

            id_cliente = (
                int(id_cliente)
                if id_cliente
                else None
            )

            venta = VentaService.crear_venta(id_usuario=current_user.id_usuario,id_cliente=id_cliente,items=items
            )

            flash("Venta registrada correctamente.","success")

            return redirect(url_for("venta.detalle",id_venta=venta.id_venta))

        except ValueError as e:
            flash(str(e),"danger")

    clientes = ClienteService.listar_clientes_activos()

    joyas = JoyaService.listar_joyas_activas()

    return render_template("ventas/crear.html",clientes=clientes,joyas=joyas)

# DETALLE
@venta_bp.route("/detalle/<int:id_venta>")
@login_required
@roles_required('ADMIN','VENDEDOR')
def detalle(id_venta):
    try:
        venta = VentaService.obtener_venta(id_venta)
    except ValueError as e:
        flash( str(e),"danger")

        return redirect(url_for("venta.index"))

    return render_template("ventas/detalle.html",venta=venta)

# ANULAR
@venta_bp.route("/anular/<int:id_venta>")
@login_required
@roles_required('ADMIN','VENDEDOR')
def anular(id_venta):
    try:
        VentaService.anular_venta(id_venta)
        flash( "Venta anulada correctamente.","warning")

    except ValueError as e:
        flash(str(e),"danger")

    return redirect( url_for("venta.index"))

# BUSCADOR AJAX
@venta_bp.route("/buscar-joya")
@login_required
@roles_required('ADMIN','VENDEDOR')
def buscar_joya():

    q = request.args.get("q","").strip()

    joyas = Joya.query.filter(
        db.or_(
            Joya.codigo.ilike(f"%{q}%"),
            Joya.nombre.ilike(f"%{q}%")
        ),
        Joya.activo == True
    ).limit(10).all()

    return jsonify([
        {
            "id": joya.id_joya,
            "codigo": joya.codigo,
            "nombre": joya.nombre,
            "stock": joya.stock_actual,
            "precio": float(
                joya.precio_venta
            )
        }
        for joya in joyas
    ])

@venta_bp.route("/factura/<int:id_venta>")
@login_required
@roles_required('ADMIN','VENDEDOR')
def factura(id_venta):

    try:
        venta = VentaService.obtener_venta(id_venta)

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for("venta.index"))

    return render_template(
        "ventas/factura.html",
        venta=venta
    )
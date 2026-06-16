from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for
from flask_login import login_required
from app.auth.decorators import roles_required

from app.modules.reportes.services import ReporteService
from app.modules.categorias.models import Categoria

from io import BytesIO
from app.modules.reportes.pdf_generator import PDFGenerator

reporte_bp = Blueprint('reporte', __name__, url_prefix='/reportes')


@reporte_bp.route("/")
def index():

    return render_template("reportes/index.html")


# ==========================
# REPORTE VENTAS
# ==========================

@reporte_bp.route("/ventas", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN','VENDEDOR')
def ventas():

    ventas = []
    total_ventas = 0

    fecha_inicio = None
    fecha_fin = None

    if request.method == "POST":

        try:

            fecha_inicio = request.form["fecha_inicio"]
            fecha_fin = request.form["fecha_fin"]

            resultado = ReporteService.reporte_ventas(fecha_inicio, fecha_fin)

            ventas = resultado["ventas"]
            total_ventas = resultado["total_ventas"]

        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "reportes/ventas.html",
        ventas=ventas,
        total_ventas=total_ventas,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

# ==========================
# PDF REPORTE VENTAS
# ==========================

@reporte_bp.route("/ventas/pdf")
@login_required
@roles_required('ADMIN','VENDEDOR')
def ventas_pdf():

    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")

    if not fecha_inicio or not fecha_fin:
        flash("Debe seleccionar un rango de fechas.", "danger")
        return redirect(url_for("reporte.ventas"))

    try:

        resultado = ReporteService.reporte_ventas(fecha_inicio, fecha_fin)

        pdf = PDFGenerator.reporte_ventas(
            resultado["ventas"],
            resultado["total_ventas"]
        )

        return send_file(
            BytesIO(pdf),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="reporte_ventas.pdf"
        )

    except ValueError as e:

        flash(str(e), "danger")

        return redirect(url_for("reporte.ventas"))

# ==========================
# REPORTE INVENTARIO
# ==========================

@reporte_bp.route("/inventario")
@login_required
@roles_required('ADMIN')
def inventario():

    resultado = ReporteService.reporte_inventario()

    return render_template(
        "reportes/inventario.html",
        joyas=resultado["joyas"],
        total_inventario=resultado["total_inventario"]
    )

# ==========================
# PDF INVENTARIO
# ==========================

@reporte_bp.route("/inventario/pdf")
@login_required
@roles_required('ADMIN')
def inventario_pdf():

    resultado = ReporteService.reporte_inventario()

    pdf = PDFGenerator.reporte_inventario(
        resultado["joyas"],
        resultado["total_inventario"]
    )

    return send_file(
        BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="reporte_inventario.pdf"
    )


# ==========================
# REPORTE RENTABILIDAD
# ==========================

@reporte_bp.route("/rentabilidad", methods=["GET", "POST"])
@login_required
@roles_required('ADMIN')
def rentabilidad():

    categorias = Categoria.get_all()

    datos = []
    utilidad_total = 0
    categoria = None

    fecha_inicio = None
    fecha_fin = None
    id_categoria = None

    if request.method == "POST":

        try:

            fecha_inicio = request.form["fecha_inicio"]
            fecha_fin = request.form["fecha_fin"]
            id_categoria = request.form["id_categoria"]

            resultado = ReporteService.reporte_rentabilidad(
                fecha_inicio,
                fecha_fin,
                id_categoria
            )

            datos = resultado["datos"]
            utilidad_total = resultado["utilidad_total"]
            categoria = resultado["categoria"]

        except ValueError as e:
            flash(str(e), "danger")

    return render_template(
        "reportes/rentabilidad.html",
        categorias=categorias,
        datos=datos,
        utilidad_total=utilidad_total,
        categoria=categoria,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        id_categoria=id_categoria
    )

# ==========================
# PDF RENTABILIDAD
# ==========================

@reporte_bp.route("/rentabilidad/pdf")
@login_required
@roles_required('ADMIN')
def rentabilidad_pdf():

    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    id_categoria = request.args.get("id_categoria")

    if not fecha_inicio or not fecha_fin or not id_categoria:

        flash("Debe generar primero el reporte.", "danger")

        return redirect(url_for("reporte.rentabilidad"))

    try:

        resultado = ReporteService.reporte_rentabilidad(
            fecha_inicio,
            fecha_fin,
            id_categoria
        )

        pdf = PDFGenerator.reporte_rentabilidad(
            resultado["datos"],
            resultado["utilidad_total"],
            resultado["categoria"]
        )

        return send_file(
            BytesIO(pdf),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="reporte_rentabilidad.pdf"
        )

    except ValueError as e:

        flash(str(e), "danger")

        return redirect(url_for("reporte.rentabilidad"))
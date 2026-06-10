from flask import render_template, Blueprint
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')

@dashboard_bp.route("/")
@login_required
def index():
    return render_template(
        "dashboard/index.html",
        fecha_actual="Jueves, 4 de junio de 2026",
        ventas_hoy=1240,
        stock_total=47,
        stock_bajo=3,
        proveedores=8,
        stock_bajo_count=0,
        meses_labels=[
            "Ene","Feb","Mar","Abr","May","Jun",
            "Jul","Ago","Sep","Oct","Nov","Dic"
        ],
        ventas_mes=[0] * 12,
        ventas_mensuales=[
            0,0,0,0,0,0,
            0,0,0,0,0,0
        ]
    )
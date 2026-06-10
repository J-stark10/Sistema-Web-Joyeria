from flask import render_template, request, flash, Blueprint
#from . import reportes_bp
from .services import ReporteInventarioService

reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')

@reportes_bp.route('/inventario', methods=['GET', 'POST'])
def reporte_inventario():
    """
    GET: muestra el formulario con filtros.
    POST: aplica filtros y muestra la tabla de resultados.
    """
    # Obtener opciones para selects
    categorias, materiales = ReporteInventarioService.get_filtros_opciones()

    # Variables para los resultados
    resultados = None
    total_valor = None
    alertas = None

    if request.method == 'POST':
        # Recoger filtros del formulario
        id_categoria = request.form.get('id_categoria')
        id_material = request.form.get('id_material')

        # Validar (si se envían vacíos, convertimos a None)
        if id_categoria == '':
            id_categoria = None
        else:
            id_categoria = int(id_categoria)

        if id_material == '':
            id_material = None
        else:
            id_material = int(id_material)

        # Consultar datos
        data = ReporteInventarioService.consultar_inventario_valorizado(
            id_categoria=id_categoria,
            id_material=id_material
        )
        resultados = data['joyas']
        total_valor = data['total_valor_stock']
        alertas = data['alertas_stock_bajo']

        if not resultados:
            flash('No se encontraron joyas con los filtros seleccionados.', 'info')

    # Renderizar la misma plantilla, pasando resultados si existen
    return render_template(
        'reportes/inventario_form.html',
        categorias=categorias,
        materiales=materiales,
        resultados=resultados,
        total_valor=total_valor,
        alertas=alertas
    )
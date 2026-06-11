from flask import render_template, request, flash, send_file, session, Blueprint
from weasyprint import HTML
import io
from datetime import datetime
#from . import reportes_bp
from .services import ReporteInventarioService


reportes_bp = Blueprint('reportes', __name__, url_prefix='/reportes')
@reportes_bp.route('/inventario', methods=['GET', 'POST'])
def reporte_inventario():
    categorias, materiales = ReporteInventarioService.get_filtros_opciones()
    
    resultados = None
    total_valor = None
    total_stock_unidades = None
    alertas = None
    filtros_actuales = {'id_categoria': '', 'id_material': ''}
    
    if request.method == 'POST':
        id_categoria = request.form.get('id_categoria')
        id_material = request.form.get('id_material')
        
        filtros_actuales = {
            'id_categoria': id_categoria or '',
            'id_material': id_material or ''
        }
        
        if id_categoria == '':
            id_categoria = None
        else:
            id_categoria = int(id_categoria)
        
        if id_material == '':
            id_material = None
        else:
            id_material = int(id_material)
        
        data = ReporteInventarioService.consultar_inventario_valorizado(
            id_categoria=id_categoria,
            id_material=id_material
        )
        resultados = data['joyas']
        total_valor = data['total_valor_stock']
        total_stock_unidades = data['total_stock_unidades']
        alertas = data['alertas_stock_bajo']
        
        if not resultados:
            flash('No se encontraron joyas con los filtros seleccionados.', 'info')
    
    return render_template(
        'reportes/inventario_form.html',
        categorias=categorias,
        materiales=materiales,
        resultados=resultados,
        total_valor=total_valor,
        total_stock_unidades=total_stock_unidades,
        alertas=alertas,
        filtros_actuales=filtros_actuales
    )


@reportes_bp.route('/inventario/pdf', methods=['POST'])
def reporte_inventario_pdf():
    # Obtener filtros del formulario
    id_categoria = request.form.get('id_categoria')
    id_material = request.form.get('id_material')
    
    # Convertir a None si está vacío
    if id_categoria == '':
        id_categoria = None
    else:
        id_categoria = int(id_categoria) if id_categoria else None
    
    if id_material == '':
        id_material = None
    else:
        id_material = int(id_material) if id_material else None
    
    # Consultar datos
    data = ReporteInventarioService.consultar_inventario_valorizado(
        id_categoria=id_categoria,
        id_material=id_material
    )
    
    # Obtener nombres de los filtros
    categoria_nombre, material_nombre = ReporteInventarioService.get_nombre_filtro(
        id_categoria, id_material
    )
    
    # Información del usuario (ajusta según cómo manejes sesión)
    usuario_nombre = session.get('usuario_nombre', 'Administrador')
    fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha_generacion = datetime.now().strftime("%d/%m/%Y")
    
    # Renderizar plantilla PDF
    html_content = render_template(
        'reportes/inventario_pdf.html',
        resultados=data['joyas'],
        total_valor=data['total_valor_stock'],
        total_stock_unidades=data['total_stock_unidades'],
        alertas=data['alertas_stock_bajo'],
        categoria_nombre=categoria_nombre,
        material_nombre=material_nombre,
        usuario_nombre=usuario_nombre,
        fecha_hora=fecha_hora,
        fecha_generacion=fecha_generacion
    )
    
    # Generar PDF
    pdf_file = HTML(string=html_content).write_pdf()
    
    # Enviar como descarga
    return send_file(
        io.BytesIO(pdf_file),
        as_attachment=True,
        download_name=f'inventario_valorizado_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )
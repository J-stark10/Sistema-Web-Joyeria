from app.modules.joyas.models import Joya
from app.modules.categorias.models import Categoria
from app.modules.materiales.models import Material

class ReporteInventarioService:
    """Servicio para el reporte de inventario valorizado (R-02)"""

    @staticmethod
    def get_filtros_opciones():
        """Obtiene listas de categorías y materiales activos para los selects"""
        categorias = Categoria.get_all()
        materiales = Material.get_all()
        return categorias, materiales

    @staticmethod
    def get_nombre_filtro(id_categoria=None, id_material=None):
        """Devuelve el nombre de la categoría y material según sus IDs"""
        categoria_nombre = None
        material_nombre = None
        if id_categoria:
            cat = Categoria.get_by_id(id_categoria)
            categoria_nombre = cat.nombre_categoria if cat else None
        if id_material:
            mat = Material.get_by_id(id_material)
            material_nombre = mat.nombre_material if mat else None
        return categoria_nombre, material_nombre

    @staticmethod
    def consultar_inventario_valorizado(id_categoria=None, id_material=None):
        """
        Retorna:
        - joyas: lista de diccionarios
        - total_valor_stock: suma total valor inventario
        - total_stock_unidades: suma total de unidades en stock
        - alertas_stock_bajo: lista de joyas con stock bajo
        """
        query = Joya.query.filter(Joya.activo == True)

        if id_categoria:
            query = query.filter(Joya.id_categoria == id_categoria)
        if id_material:
            query = query.filter(Joya.id_material == id_material)

        joyas_db = query.order_by(Joya.nombre).all()

        joyas_data = []
        total_valor = 0.0
        total_stock_unidades = 0

        for j in joyas_db:
            valor_stock = float(j.precio_compra) * j.stock_actual
            total_valor += valor_stock
            total_stock_unidades += j.stock_actual
            joyas_data.append({
                'codigo': j.codigo,
                'nombre': j.nombre,
                'categoria': j.categoria.nombre_categoria if j.categoria else 'N/A',
                'material': j.material.nombre_material if j.material else 'N/A',
                'stock_actual': j.stock_actual,
                'stock_minimo': j.stock_minimo,
                'precio_compra': float(j.precio_compra),
                'valor_total_stock': valor_stock,
                'stock_bajo': j.stock_bajo
            })

        alertas = [j for j in joyas_data if j['stock_bajo']]

        return {
            'joyas': joyas_data,
            'total_valor_stock': total_valor,
            'total_stock_unidades': total_stock_unidades,
            'alertas_stock_bajo': alertas
        }
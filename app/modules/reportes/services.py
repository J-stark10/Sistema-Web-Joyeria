from app.modules.joyas.models import Joya
from app.modules.categorias.models import Categoria
from app.modules.materiales.models import Material

class ReporteInventarioService:
    """Servicio para el reporte de inventario valorizado (R-02)"""

    @staticmethod
    def get_filtros_opciones():
        """Obtiene listas de categorías y materiales activos para los selects"""
        categorias = Categoria.get_all()       # asume método get_all()
        materiales = Material.get_all()        # asume método get_all()
        return categorias, materiales

    @staticmethod
    def consultar_inventario_valorizado(id_categoria=None, id_material=None):
        """
        Retorna:
        - joyas: lista de diccionarios con datos para la tabla
        - total_valor_stock: suma de (stock_actual * precio_compra)
        - alertas_stock_bajo: lista de joyas con stock bajo (opcional, luego se usa)
        """
        query = Joya.query.filter(Joya.activo == True)

        if id_categoria:
            query = query.filter(Joya.id_categoria == id_categoria)
        if id_material:
            query = query.filter(Joya.id_material == id_material)

        joyas_db = query.order_by(Joya.nombre).all()

        joyas_data = []
        total_valor = 0.0

        for j in joyas_db:
            valor_stock = float(j.precio_compra) * j.stock_actual
            total_valor += valor_stock
            joyas_data.append({
                'codigo': j.codigo,
                'nombre': j.nombre,
                'categoria': j.categoria.nombre_categoria if j.categoria else 'N/A',  # asume relación
                'material': j.material.nombre_material if j.material else 'N/A',
                'stock_actual': j.stock_actual,
                'precio_compra': float(j.precio_compra),
                'valor_total_stock': valor_stock,
                'stock_bajo': j.stock_bajo   # propiedad del modelo
            })

        # Alertas: joyas con stock bajo (ya filtradas)
        alertas = [j for j in joyas_data if j['stock_bajo']]

        return {
            'joyas': joyas_data,
            'total_valor_stock': total_valor,
            'alertas_stock_bajo': alertas
        }
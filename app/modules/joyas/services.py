from app.modules.joyas.models import Joya
from app.modules.categorias.models import Categoria
from app.modules.materiales.models import Material

class JoyaService:

    @staticmethod
    def listar_joyas():
        return Joya.get_all()

    @staticmethod
    def listar_joyas_activas():
        return Joya.get_activos()

    @staticmethod
    def listar_stock_bajo():
        return Joya.get_stock_bajo()

    @staticmethod
    def obtener_joya(id_joya):

        joya = Joya.get_by_id(id_joya)
        if not joya:
            raise ValueError("Joya no encontrada.")

        return joya

    # ==========================
    # CREAR
    # ==========================

    @staticmethod
    def crear_joya(
        codigo,
        nombre,
        id_categoria,
        id_material,
        precio_compra,
        precio_venta,
        stock_minimo
    ):

        existente = Joya.get_by_codigo(codigo.strip())
        if existente:
            raise ValueError("Ya existe una joya con ese código.")

        categoria = Categoria.get_by_id(id_categoria)
        if not categoria:
            raise ValueError("La categoría seleccionada no existe.")

        material = Material.get_by_id(id_material)
        if not material:
            raise ValueError("El material seleccionado no existe.")

        if float(precio_compra) < 0:
            raise ValueError("El precio de compra no puede ser negativo.")

        if float(precio_venta) < 0:
            raise ValueError("El precio de venta no puede ser negativo.")

        if int(stock_minimo) < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")

        joya = Joya(
            codigo=codigo.strip(),
            nombre=nombre.strip(),
            id_categoria=id_categoria,
            id_material=id_material,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock_actual=0,
            stock_minimo=stock_minimo,
            activo=True
        )

        joya.save()

        return joya

    # ==========================
    # ACTUALIZAR
    # ==========================

    @staticmethod
    def actualizar_joya(
        id_joya,
        codigo,
        nombre,
        id_categoria,
        id_material,
        precio_compra,
        precio_venta,
        stock_minimo,
        activo=True
    ):

        joya = Joya.get_by_id(id_joya)

        if not joya:
            raise ValueError("Joya no encontrada.")

        existente = Joya.get_by_codigo(codigo.strip())

        if existente and existente.id_joya != joya.id_joya:
            raise ValueError("Ya existe otra joya con ese código.")

        categoria = Categoria.get_by_id(id_categoria)

        if not categoria:
            raise ValueError("La categoría seleccionada no existe.")

        material = Material.get_by_id(id_material)

        if not material:
            raise ValueError("El material seleccionado no existe.")

        if float(precio_compra) < 0:
            raise ValueError("El precio de compra no puede ser negativo.")

        if float(precio_venta) < 0:
            raise ValueError("El precio de venta no puede ser negativo.")

        if int(stock_minimo) < 0:
            raise ValueError("El stock mínimo no puede ser negativo.")

        joya.update(
            codigo=codigo.strip(),
            nombre=nombre.strip(),
            id_categoria=id_categoria,
            id_material=id_material,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock_minimo=stock_minimo,
            activo=activo
        )

        return joya

    # ==========================
    # DESACTIVAR
    # ==========================

    @staticmethod
    def desactivar_joya(id_joya):

        joya = Joya.get_by_id(id_joya)
        if not joya:
            raise ValueError("Joya no encontrada.")

        joya.delete()

    # ==========================
    # ACTIVAR
    # ==========================

    @staticmethod
    def activar_joya(id_joya):

        joya = Joya.get_by_id(id_joya)
        if not joya:
            raise ValueError("Joya no encontrada.")

        joya.restore()
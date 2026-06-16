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

    # CREAR
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

        codigo = codigo.strip()
        if not codigo:
            raise ValueError("El código de la joya es obligatorio.")
        if len(codigo) > 50:
            raise ValueError("El código no puede superar los 50 caracteres.")
        
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la joya es obligatorio.")
        if len(nombre) > 150:
            raise ValueError("El nombre no puede superar los 150 caracteres.")
        
        existente = Joya.get_by_codigo(codigo.strip())
        if existente:
            raise ValueError("Ya existe una joya con ese código.")

        categoria = Categoria.get_by_id(id_categoria)
        if not categoria:
            raise ValueError("La categoría seleccionada no existe.")

        material = Material.get_by_id(id_material)
        if not material:
            raise ValueError("El material seleccionado no existe.")

        precio_compra = float(precio_compra)
        if precio_compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a cero.")

        precio_venta = float(precio_venta)
        if precio_venta <= 0:
            raise ValueError("El precio de venta debe ser mayor a cero.")
        
        if precio_venta < precio_compra:
            raise ValueError("El precio de venta no puede ser menor al precio de compra.")

        stock_minimo = int(stock_minimo)
        if stock_minimo < 0:
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

    # ACTUALIZAR
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

        joya = JoyaService.obtener_joya(id_joya)

        if not joya:
            raise ValueError("Joya no encontrada.")

        codigo = codigo.strip()
        if not codigo:
            raise ValueError("El código de la joya es obligatorio.")
        if len(codigo) > 50:
            raise ValueError("El código no puede superar los 50 caracteres.")
        
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la joya es obligatorio.")
        if len(nombre) > 150:
            raise ValueError("El nombre no puede superar los 150 caracteres.")
        
        existente = Joya.get_by_codigo(codigo.strip())
        if existente and existente.id_joya != joya.id_joya:
            raise ValueError("Ya existe una joya con ese código.")

        categoria = Categoria.get_by_id(id_categoria)
        if not categoria:
            raise ValueError("La categoría seleccionada no existe.")

        material = Material.get_by_id(id_material)
        if not material:
            raise ValueError("El material seleccionado no existe.")

        precio_compra = float(precio_compra)
        if precio_compra <= 0:
            raise ValueError("El precio de compra debe ser mayor a cero.")

        precio_venta = float(precio_venta)
        if precio_venta <= 0:
            raise ValueError("El precio de venta debe ser mayor a cero.")
        
        if precio_venta < precio_compra:
            raise ValueError("El precio de venta no puede ser menor al precio de compra.")

        stock_minimo = int(stock_minimo)
        if stock_minimo < 0:
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

    # DESACTIVAR
    @staticmethod
    def desactivar_joya(id_joya):

        joya = Joya.get_by_id(id_joya)

        if not joya:
            raise ValueError("Joya no encontrada.")
        if not joya.activo:
            raise ValueError("La joya ya se encuentra desactivada.")

        joya.delete()

    # ACTIVAR
    @staticmethod
    def activar_joya(id_joya):

        joya = Joya.get_by_id(id_joya)

        if not joya:
            raise ValueError("Joya no encontrada.")
        if joya.activo:
            raise ValueError("La joya ya se encuentra activa.")

        joya.restore()

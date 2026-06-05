from app.modules.categorias.models import Categoria

class CategoriaService:

    @staticmethod
    def listar_categorias():
        return Categoria.get_all()

    @staticmethod
    def obtener_categoria(id_categoria):

        categoria = Categoria.get_by_id(id_categoria)
        if not categoria:
            raise ValueError("Categoría no encontrada.")

        return categoria

    # ==========================
    # CREAR
    # ==========================

    @staticmethod
    def crear_categoria(nombre_categoria):

        existente = Categoria.get_by_nombre(nombre_categoria.strip())

        if existente:
            raise ValueError("Ya existe una categoría con ese nombre.")
        categoria = Categoria(nombre_categoria=nombre_categoria.strip())
        categoria.save()

        return categoria

    # ==========================
    # ACTUALIZAR
    # ==========================

    @staticmethod
    def actualizar_categoria(id_categoria,nombre_categoria):

        categoria = Categoria.get_by_id( id_categoria)
        if not categoria:
            raise ValueError("Categoría no encontrada.")

        existente = Categoria.get_by_nombre( nombre_categoria.strip())

        if existente and existente.id_categoria != categoria.id_categoria:
            raise ValueError("Ya existe otra categoría con ese nombre.")

        categoria.update(nombre_categoria=nombre_categoria.strip())

        return categoria

    # ==========================
    # ELIMINAR
    # ==========================

    @staticmethod
    def eliminar_categoria(id_categoria):

        categoria = Categoria.get_by_id(id_categoria)
        if not categoria:
            raise ValueError("Categoría no encontrada." )

        categoria.delete()
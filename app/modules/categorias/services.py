from app.modules.categorias.models import Categoria

class CategoriaService:

    @staticmethod
    def listar_categorias():
        return Categoria.get_all()

    @staticmethod
    def obtener_categoria(id_categoria):

        categoria = Categoria.get_by_id(id_categoria)
        if not categoria:
            raise ValueError("Categoria no encontrada.")

        return categoria

    # CREAR    
    @staticmethod
    def crear_categoria(nombre_categoria):

        nombre_categoria = nombre_categoria.strip()

        if not nombre_categoria:
            raise ValueError("El nombre de la categoría es obligatorio.")

        if len(nombre_categoria) > 100:
            raise ValueError("El nombre de la categoría no puede superar los 100 caracteres.")

        existente = Categoria.get_by_nombre(nombre_categoria)

        if existente:
            raise ValueError("Ya existe una categoría con ese nombre.")

        categoria = Categoria(nombre_categoria=nombre_categoria)
        categoria.save()

        return categoria

    # ACTUALIZAR
    @staticmethod
    def actualizar_categoria(id_categoria, nombre_categoria):

        categoria = CategoriaService.obtener_categoria(id_categoria)
        nombre_categoria = nombre_categoria.strip()

        if not nombre_categoria:
            raise ValueError("El nombre de la categoría es obligatorio.")

        if len(nombre_categoria) > 100:
            raise ValueError("El nombre de la categoría no puede superar los 100 caracteres.")

        existente = Categoria.get_by_nombre(nombre_categoria)

        if existente and existente.id_categoria != categoria.id_categoria:
            raise ValueError("Ya existe otra categoría con ese nombre.")

        categoria.update(nombre_categoria=nombre_categoria)

        return categoria

    # ELIMINAR
    @staticmethod
    def eliminar_categoria(id_categoria):

        categoria = CategoriaService.obtener_categoria(id_categoria)

        if categoria.joyas:
            raise ValueError("No es posible eliminar la categoría porque tiene joyas asociadas.")

        categoria.delete()
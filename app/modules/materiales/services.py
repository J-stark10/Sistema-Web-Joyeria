from app.modules.materiales.models import Material

class MaterialService:

    @staticmethod
    def listar_materiales():
        return Material.get_all()

    @staticmethod
    def obtener_material(id_material):

        material = Material.get_by_id(id_material)

        if not material:
            raise ValueError("Material no encontrado.")

        return material

    # ==========================
    # CREAR
    # ==========================

    @staticmethod
    def crear_material(nombre_material):

        existente = Material.get_by_nombre(nombre_material.strip())

        if existente:
            raise ValueError("Ya existe un material con ese nombre.")

        material = Material(
            nombre_material=nombre_material.strip()
        )

        material.save()

        return material

    # ==========================
    # ACTUALIZAR
    # ==========================

    @staticmethod
    def actualizar_material(id_material, nombre_material):

        material = Material.get_by_id(id_material)

        if not material:
            raise ValueError("Material no encontrado.")

        existente = Material.get_by_nombre(nombre_material.strip())

        if existente and existente.id_material != material.id_material:
            raise ValueError("Ya existe otro material con ese nombre.")

        material.update(
            nombre_material=nombre_material.strip()
        )

        return material

    # ==========================
    # ELIMINAR
    # ==========================

    @staticmethod
    def eliminar_material(id_material):

        material = Material.get_by_id(id_material)

        if not material:
            raise ValueError("Material no encontrado.")

        material.delete()
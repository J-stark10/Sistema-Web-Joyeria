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

    # CREAR
    @staticmethod
    def crear_material(nombre_material):

        nombre_material = nombre_material.strip()

        if not nombre_material:
            raise ValueError("El nombre del material es obligatorio.")
        
        if len(nombre_material) > 100:
            raise ValueError("El nombre del material no puede superar los 100 caracteres.")

        existente = Material.get_by_nombre(nombre_material)

        if existente:
            raise ValueError("Ya existe un material con ese nombre.")

        material = Material(nombre_material=nombre_material)
        material.save()

        return material

    # ACTUALIZAR
    @staticmethod
    def actualizar_material(id_material, nombre_material):

        material = MaterialService.obtener_material(id_material)
        nombre_material = nombre_material.strip()

        if not nombre_material:
            raise ValueError("El nombre del material es obligatorio.")
        
        if len(nombre_material) > 100:
            raise ValueError("El nombre del material no puede superar los 100 caracteres.")

        existente = Material.get_by_nombre(nombre_material.strip())

        if existente and existente.id_material != material.id_material:
            raise ValueError("Ya existe otro material con ese nombre.")

        material.update(nombre_material=nombre_material)

        return material

    # ELIMINAR
    @staticmethod
    def eliminar_material(id_material):

        material = MaterialService.obtener_material(id_material)

        if material.joyas:
            raise ValueError("No es posible eliminar el material porque tiene joyas asociadas.")

        material.delete()
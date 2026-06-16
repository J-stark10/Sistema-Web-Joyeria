from app.modules.inventario.models import AjusteInventario
from app.modules.joyas.services import JoyaService
from app.modules.usuarios.services import UsuarioService


class InventarioService:

    @staticmethod
    def listar_ajustes():
        return AjusteInventario.get_all()

    @staticmethod
    def obtener_ajuste(id_ajuste):

        ajuste = AjusteInventario.get_by_id(id_ajuste)
        if not ajuste:
            raise ValueError("Ajuste de inventario no encontrado.")

        return ajuste

    @staticmethod
    def listar_stock_bajo():
        return JoyaService.listar_stock_bajo()

    @staticmethod
    def registrar_ajuste(
        id_joya,
        id_usuario,
        cantidad,
        motivo,
        tipo_ajuste
    ):

        joya = JoyaService.obtener_joya(id_joya)

        if not joya.activo:
            raise ValueError("No es posible realizar ajustes sobre una joya inactiva.")

        usuario = UsuarioService.obtener_usuario(id_usuario)

        if not usuario.activo:
            raise ValueError("No es posible registrar ajustes con un usuario inactivo.")

        try:
            cantidad = int(cantidad)

        except (ValueError, TypeError):
            raise ValueError("La cantidad ingresada no es válida.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        tipo_ajuste = tipo_ajuste.strip().upper()

        if tipo_ajuste not in ["ENTRADA", "SALIDA"]:
            raise ValueError("El tipo de ajuste seleccionado no es válido.")

        motivo = motivo.strip()

        if not motivo:
            raise ValueError("Debe ingresar el motivo del ajuste.")

        if tipo_ajuste == "SALIDA" and cantidad > joya.stock_actual:
            raise ValueError(f"No existe stock suficiente para realizar la salida. Stock disponible: {joya.stock_actual}.")

        if tipo_ajuste == "ENTRADA":
            joya.aumentar_stock(cantidad)

        if tipo_ajuste == "SALIDA":
            joya.disminuir_stock(cantidad)

        ajuste = AjusteInventario(
            id_joya=joya.id_joya,
            id_usuario=usuario.id_usuario,
            cantidad_ajuste=cantidad,
            motivo=motivo,
            tipo_ajuste=tipo_ajuste
        )

        ajuste.save()

        return ajuste
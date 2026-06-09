from app.modules.inventario.models import AjusteInventario
from app.modules.joyas.models import Joya

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
        return Joya.get_stock_bajo()

    @staticmethod
    def registrar_ajuste(id_joya,id_usuario,cantidad,motivo,tipo_ajuste):

        joya = Joya.get_by_id(id_joya)

        if not joya:
            raise ValueError("La joya seleccionada no existe.")

        if int(cantidad) <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        tipo_ajuste = tipo_ajuste.upper()

        if tipo_ajuste not in ["ENTRADA","SALIDA"]:
            raise ValueError("Tipo de ajuste inválido.")

        if tipo_ajuste == "SALIDA" and int(cantidad) > joya.stock_actual:
            raise ValueError("Stock insuficiente para realizar la salida.")

        if tipo_ajuste == "ENTRADA":
            joya.aumentar_stock(int(cantidad))

        if tipo_ajuste == "SALIDA":
            joya.disminuir_stock(int(cantidad))

        ajuste = AjusteInventario(
            id_joya=id_joya,
            id_usuario=id_usuario,
            cantidad_ajuste=cantidad,
            motivo=motivo.strip(),
            tipo_ajuste=tipo_ajuste
        )

        ajuste.save()

        return ajuste
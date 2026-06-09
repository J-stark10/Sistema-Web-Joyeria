from app.modules.clientes.models import Cliente

class ClienteService:

    @staticmethod
    def listar_clientes():
        return Cliente.get_all()
    
    @staticmethod
    def listar_clientes_activos():
        return Cliente.get_activos()
    
    @staticmethod
    def obtener_cliente(id_cliente):
        cliente = Cliente.get_by_id(id_cliente)

        if not cliente:
            raise ValueError("Cliente no encontrado")
        
        return cliente
    
    # ==========================
    # CREAR
    # ==========================

    @staticmethod
    def crear_cliente(nombre, ci_nit, telefono=None, direccion=None):

        existente = Cliente.get_by_ci_nit( ci_nit )

        if existente:
            raise ValueError("Ya existe un cliente con ese CI/NIT.")

        cliente = Cliente(
            nombre=nombre.strip(),
            ci_nit=ci_nit.strip(),
            telefono=telefono.strip() if telefono else None,
            direccion=direccion.strip() if direccion else None
        )
        cliente.save()

        return cliente

    # ==========================
    # ACTUALIZAR
    # ==========================

    @staticmethod
    def actualizar_cliente( id_cliente, nombre, ci_nit, telefono=None, direccion=None, activo=True):

        cliente = Cliente.get_by_id(id_cliente)

        if not cliente:
            raise ValueError("Cliente no encontrado.")

        otro_cliente = Cliente.get_by_ci_nit(ci_nit)

        if (otro_cliente and otro_cliente.id_cliente != cliente.id_cliente ):
            raise ValueError( "Ya existe otro cliente con ese CI/NIT." )

        cliente.update(
            nombre=nombre.strip(),
            ci_nit=ci_nit.strip(),
            telefono=telefono.strip() if telefono else None,
            direccion=direccion.strip() if direccion else None,
            activo=activo
        )

        return cliente

    # ==========================
    # DESACTIVAR
    # ==========================

    @staticmethod
    def desactivar_cliente( id_cliente):

        cliente = Cliente.get_by_id( id_cliente)

        if not cliente:
            raise ValueError( "Cliente no encontrado." )
        cliente.deactivate()

    # ==========================
    # REACTIVAR 
    # ==========================

    @staticmethod
    def activar_cliente( id_cliente ):

        cliente = Cliente.get_by_id(id_cliente )
        if not cliente:
            raise ValueError( "Cliente no encontrado." )

        cliente.restore()
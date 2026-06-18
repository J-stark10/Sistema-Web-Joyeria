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
            raise ValueError("Cliente no encontrado.")
        
        return cliente
    
    # CREAR
    @staticmethod
    def crear_cliente(nombre, ci_nit, telefono=None, direccion=None):

        nombre = nombre.strip()

        if not nombre:
            raise ValueError("El nombre del cliente es obligatorio.")
        
        if len(nombre) > 100:
            raise ValueError("El nombre del cliente no puede exceder los 100 caracteres.")
        
        if len(ci_nit) > 30:
            raise ValueError("El CI/NIT no puede superar los 30 caracteres.")
        
        if telefono and len(telefono.strip()) > 8:
            raise ValueError("El teléfono no puede superar los 8 caracteres.") 
        
        if direccion and len(direccion.strip()) > 200:
            raise ValueError("La dirección no puede superar los 200 caracteres.")

        ci_nit = ci_nit.strip()

        if not ci_nit:
            raise ValueError("El CI/NIT del cliente es obligatorio.")

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

    # ACTUALIZAR
    @staticmethod
    def actualizar_cliente( id_cliente, nombre, ci_nit, telefono=None, direccion=None, activo=True):

        cliente = ClienteService.obtener_cliente(id_cliente)

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

    # DESACTIVAR
    @staticmethod
    def desactivar_cliente( id_cliente):

        cliente = ClienteService.obtener_cliente(id_cliente)

        if not cliente.activo:
            raise ValueError("El cliente ya se encuentra desactivado.")

        if not cliente:
            raise ValueError( "Cliente no encontrado." )
        cliente.deactivate()

    # REACTIVAR 
    @staticmethod
    def activar_cliente( id_cliente ):

        cliente = ClienteService.obtener_cliente(id_cliente )

        if cliente.activo:
            raise ValueError("El cliente ya se encuentra activo.")

        if not cliente:
            raise ValueError( "Cliente no encontrado." )

        cliente.restore()

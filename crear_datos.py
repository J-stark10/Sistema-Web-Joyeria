from decimal import Decimal

from app import create_app, db
from app.modules.categorias.models import Categoria
from app.modules.clientes.models import Cliente
from app.modules.compras.models import Compra, DetalleCompra
from app.modules.inventario.models import AjusteInventario
from app.modules.joyas.models import Joya
from app.modules.materiales.models import Material
from app.modules.proveedores.models import Proveedor
from app.modules.usuarios.models import Usuario
from app.modules.ventas.models import Venta, DetalleVenta


app = create_app("development")

CATEGORIAS = [
    "Anillos",
    "Collares",
    "Pulseras",
    "Aretes",
    "Dijes",
    "Relojes",
    "Cadenas",
    "Brazaletes",
    "Tobilleras",
    "Juegos",
]

MATERIALES = [
    "Oro 18K",
    "Plata 925",
    "Acero inoxidable",
    "Oro blanco",
    "Perlas",
    "Rodio",
    "Titanio",
    "Piedras naturales",
    "Cristal",
    "Cuero",
]

CLIENTES = [
    {"nombre": "Maria Fernanda Rojas", "ci_nit": "1001001", "telefono": "70123456", "direccion": "Av. America #123"},
    {"nombre": "Carlos Mendoza", "ci_nit": "1001002", "telefono": "71234567", "direccion": "Calle Bolivar #45"},
    {"nombre": "Lucia Vargas", "ci_nit": "1001003", "telefono": "72345678", "direccion": "Zona Norte, pasaje Los Pinos"},
    {"nombre": "Jorge Salazar", "ci_nit": "1001004", "telefono": "73456789", "direccion": "Av. Blanco Galindo km 4"},
    {"nombre": "Ana Sofia Quiroga", "ci_nit": "1001005", "telefono": "74567890", "direccion": "Calle Sucre #88"},
    {"nombre": "Diego Arce", "ci_nit": "1001006", "telefono": "75678901", "direccion": "Av. Heroinas #210"},
    {"nombre": "Patricia Lopez", "ci_nit": "1001007", "telefono": "76789012", "direccion": "Zona Cala Cala, calle 7"},
    {"nombre": "Roberto Camacho", "ci_nit": "1001008", "telefono": "77890123", "direccion": "Av. Circunvalacion #300"},
    {"nombre": "Valeria Torres", "ci_nit": "1001009", "telefono": "78901234", "direccion": "Barrio Profesional, bloque B"},
]

PROVEEDORES = [
    {"nombre_razon_social": "Brillos Andinos SRL", "nit": "2002001", "telefono": "44112233", "correo": "ventas@brillosandinos.bo"},
    {"nombre_razon_social": "Metales Finos Bolivia", "nit": "2002002", "telefono": "44223344", "correo": "contacto@metalesfinos.bo"},
    {"nombre_razon_social": "Perlas del Sur Import", "nit": "2002003", "telefono": "44334455", "correo": "info@perlasdelsur.bo"},
    {"nombre_razon_social": "Joyas Aurora Ltda", "nit": "2002004", "telefono": "44445566", "correo": "pedidos@joyasaurora.bo"},
    {"nombre_razon_social": "Cristales Premium SRL", "nit": "2002005", "telefono": "44556677", "correo": "ventas@cristalespremium.bo"},
    {"nombre_razon_social": "Titanio Store Bolivia", "nit": "2002006", "telefono": "44667788", "correo": "contacto@titaniostore.bo"},
    {"nombre_razon_social": "Importadora Luz de Luna", "nit": "2002007", "telefono": "44778899", "correo": "info@luzdeluna.bo"},
    {"nombre_razon_social": "Artesanos del Valle", "nit": "2002008", "telefono": "44889900", "correo": "ventas@artesanosvalle.bo"},
]

JOYAS = [
    {"codigo": "JOY-001", "nombre": "Anillo solitario oro 18K", "categoria": "Anillos", "material": "Oro 18K", "precio_compra": "850.00", "precio_venta": "1250.00", "stock_actual": 8, "stock_minimo": 2},
    {"codigo": "JOY-002", "nombre": "Collar plata luna", "categoria": "Collares", "material": "Plata 925", "precio_compra": "180.00", "precio_venta": "320.00", "stock_actual": 15, "stock_minimo": 4},
    {"codigo": "JOY-003", "nombre": "Pulsera acero trenzada", "categoria": "Pulseras", "material": "Acero inoxidable", "precio_compra": "65.00", "precio_venta": "120.00", "stock_actual": 20, "stock_minimo": 5},
    {"codigo": "JOY-004", "nombre": "Aretes perla clasicos", "categoria": "Aretes", "material": "Perlas", "precio_compra": "210.00", "precio_venta": "380.00", "stock_actual": 10, "stock_minimo": 3},
    {"codigo": "JOY-005", "nombre": "Dije corazon oro blanco", "categoria": "Dijes", "material": "Oro blanco", "precio_compra": "430.00", "precio_venta": "690.00", "stock_actual": 7, "stock_minimo": 2},
    {"codigo": "JOY-006", "nombre": "Cadena rolo rodiada", "categoria": "Cadenas", "material": "Rodio", "precio_compra": "145.00", "precio_venta": "260.00", "stock_actual": 18, "stock_minimo": 4},
    {"codigo": "JOY-007", "nombre": "Brazalete titanio mate", "categoria": "Brazaletes", "material": "Titanio", "precio_compra": "95.00", "precio_venta": "180.00", "stock_actual": 16, "stock_minimo": 4},
    {"codigo": "JOY-008", "nombre": "Tobillera cristal azul", "categoria": "Tobilleras", "material": "Cristal", "precio_compra": "55.00", "precio_venta": "110.00", "stock_actual": 22, "stock_minimo": 6},
    {"codigo": "JOY-009", "nombre": "Juego collar y aretes amatista", "categoria": "Juegos", "material": "Piedras naturales", "precio_compra": "310.00", "precio_venta": "520.00", "stock_actual": 9, "stock_minimo": 2},
    {"codigo": "JOY-010", "nombre": "Pulsera cuero dije plata", "categoria": "Pulseras", "material": "Cuero", "precio_compra": "70.00", "precio_venta": "135.00", "stock_actual": 19, "stock_minimo": 5},
]

COMPRAS = [
    {"proveedor_nit": "2002001", "detalles": [{"codigo_joya": "JOY-001", "cantidad": 5, "precio_unit_compra": "850.00"}, {"codigo_joya": "JOY-002", "cantidad": 8, "precio_unit_compra": "180.00"}]},
    {"proveedor_nit": "2002002", "detalles": [{"codigo_joya": "JOY-003", "cantidad": 10, "precio_unit_compra": "65.00"}, {"codigo_joya": "JOY-005", "cantidad": 4, "precio_unit_compra": "430.00"}]},
    {"proveedor_nit": "2002003", "detalles": [{"codigo_joya": "JOY-004", "cantidad": 6, "precio_unit_compra": "210.00"}, {"codigo_joya": "JOY-002", "cantidad": 5, "precio_unit_compra": "178.00"}]},
    {"proveedor_nit": "2002001", "detalles": [{"codigo_joya": "JOY-005", "cantidad": 3, "precio_unit_compra": "425.00"}, {"codigo_joya": "JOY-001", "cantidad": 2, "precio_unit_compra": "840.00"}]},
    {"proveedor_nit": "2002002", "detalles": [{"codigo_joya": "JOY-003", "cantidad": 12, "precio_unit_compra": "63.00"}, {"codigo_joya": "JOY-004", "cantidad": 4, "precio_unit_compra": "205.00"}]},
    {"proveedor_nit": "2002004", "detalles": [{"codigo_joya": "JOY-006", "cantidad": 9, "precio_unit_compra": "145.00"}, {"codigo_joya": "JOY-009", "cantidad": 3, "precio_unit_compra": "310.00"}]},
    {"proveedor_nit": "2002005", "detalles": [{"codigo_joya": "JOY-008", "cantidad": 14, "precio_unit_compra": "55.00"}, {"codigo_joya": "JOY-004", "cantidad": 5, "precio_unit_compra": "208.00"}]},
    {"proveedor_nit": "2002006", "detalles": [{"codigo_joya": "JOY-007", "cantidad": 8, "precio_unit_compra": "95.00"}, {"codigo_joya": "JOY-003", "cantidad": 6, "precio_unit_compra": "64.00"}]},
    {"proveedor_nit": "2002007", "detalles": [{"codigo_joya": "JOY-010", "cantidad": 11, "precio_unit_compra": "70.00"}, {"codigo_joya": "JOY-006", "cantidad": 6, "precio_unit_compra": "142.00"}]},
    {"proveedor_nit": "2002008", "detalles": [{"codigo_joya": "JOY-009", "cantidad": 4, "precio_unit_compra": "305.00"}, {"codigo_joya": "JOY-008", "cantidad": 10, "precio_unit_compra": "53.00"}]},
]

VENTAS = [
    {"cliente_ci_nit": "1001001", "detalles": [{"codigo_joya": "JOY-001", "cantidad": 1, "precio_unit_venta": "1250.00"}, {"codigo_joya": "JOY-002", "cantidad": 2, "precio_unit_venta": "320.00"}]},
    {"cliente_ci_nit": "1001002", "detalles": [{"codigo_joya": "JOY-003", "cantidad": 3, "precio_unit_venta": "120.00"}, {"codigo_joya": "JOY-004", "cantidad": 1, "precio_unit_venta": "380.00"}]},
    {"cliente_ci_nit": "1001003", "detalles": [{"codigo_joya": "JOY-005", "cantidad": 1, "precio_unit_venta": "690.00"}]},
    {"cliente_ci_nit": "1001004", "detalles": [{"codigo_joya": "JOY-002", "cantidad": 1, "precio_unit_venta": "320.00"}, {"codigo_joya": "JOY-003", "cantidad": 2, "precio_unit_venta": "120.00"}]},
    {"cliente_ci_nit": "1001001", "detalles": [{"codigo_joya": "JOY-004", "cantidad": 2, "precio_unit_venta": "380.00"}, {"codigo_joya": "JOY-005", "cantidad": 1, "precio_unit_venta": "690.00"}]},
    {"cliente_ci_nit": "1001005", "detalles": [{"codigo_joya": "JOY-006", "cantidad": 2, "precio_unit_venta": "260.00"}, {"codigo_joya": "JOY-008", "cantidad": 1, "precio_unit_venta": "110.00"}]},
    {"cliente_ci_nit": "1001006", "detalles": [{"codigo_joya": "JOY-007", "cantidad": 1, "precio_unit_venta": "180.00"}, {"codigo_joya": "JOY-010", "cantidad": 2, "precio_unit_venta": "135.00"}]},
    {"cliente_ci_nit": "1001007", "detalles": [{"codigo_joya": "JOY-009", "cantidad": 1, "precio_unit_venta": "520.00"}]},
    {"cliente_ci_nit": "1001008", "detalles": [{"codigo_joya": "JOY-001", "cantidad": 1, "precio_unit_venta": "1250.00"}, {"codigo_joya": "JOY-006", "cantidad": 1, "precio_unit_venta": "260.00"}]},
    {"cliente_ci_nit": "1001009", "detalles": [{"codigo_joya": "JOY-002", "cantidad": 3, "precio_unit_venta": "320.00"}, {"codigo_joya": "JOY-008", "cantidad": 2, "precio_unit_venta": "110.00"}]},
    {"cliente_ci_nit": "1001002", "detalles": [{"codigo_joya": "JOY-010", "cantidad": 1, "precio_unit_venta": "135.00"}, {"codigo_joya": "JOY-004", "cantidad": 1, "precio_unit_venta": "380.00"}]},
    {"cliente_ci_nit": "1001003", "detalles": [{"codigo_joya": "JOY-007", "cantidad": 2, "precio_unit_venta": "180.00"}, {"codigo_joya": "JOY-005", "cantidad": 1, "precio_unit_venta": "690.00"}]},
]

AJUSTES_INVENTARIO = [
    {"codigo_joya": "JOY-001", "cantidad_ajuste": 2, "tipo_ajuste": "ENTRADA", "motivo": "Reposicion por conteo fisico"},
    {"codigo_joya": "JOY-002", "cantidad_ajuste": 1, "tipo_ajuste": "SALIDA", "motivo": "Merma por exhibicion"},
    {"codigo_joya": "JOY-003", "cantidad_ajuste": 3, "tipo_ajuste": "ENTRADA", "motivo": "Ajuste positivo de inventario"},
    {"codigo_joya": "JOY-004", "cantidad_ajuste": 1, "tipo_ajuste": "SALIDA", "motivo": "Producto danado"},
    {"codigo_joya": "JOY-005", "cantidad_ajuste": 2, "tipo_ajuste": "ENTRADA", "motivo": "Devolucion a stock"},
    {"codigo_joya": "JOY-006", "cantidad_ajuste": 2, "tipo_ajuste": "SALIDA", "motivo": "Correccion de stock"},
    {"codigo_joya": "JOY-007", "cantidad_ajuste": 4, "tipo_ajuste": "ENTRADA", "motivo": "Ingreso adicional"},
    {"codigo_joya": "JOY-008", "cantidad_ajuste": 1, "tipo_ajuste": "SALIDA", "motivo": "Muestra entregada"},
]


def decimal_centavos(valor):
    return Decimal(str(valor)).quantize(Decimal("0.01"))


def get_or_create(model, defaults=None, **filters):
    instance = model.query.filter_by(**filters).first()
    if instance is not None:
        return instance, False

    params = dict(filters)
    params.update(defaults or {})
    instance = model(**params)
    db.session.add(instance)
    return instance, True


def buscar_usuario_existente():
    return Usuario.query.filter_by(activo=True).order_by(Usuario.id_usuario.asc()).first()


def crear_catalogos():
    creados = 0
    for nombre_categoria in CATEGORIAS:
        _, created = get_or_create(Categoria, nombre_categoria=nombre_categoria)
        creados += int(created)
    for nombre_material in MATERIALES:
        _, created = get_or_create(Material, nombre_material=nombre_material)
        creados += int(created)
    db.session.commit()
    return creados


def crear_clientes():
    creados = 0
    for data in CLIENTES:
        _, created = get_or_create(
            Cliente,
            defaults={
                "nombre": data["nombre"],
                "telefono": data["telefono"],
                "direccion": data["direccion"],
                "activo": True,
            },
            ci_nit=data["ci_nit"],
        )
        creados += int(created)
    db.session.commit()
    return creados


def crear_proveedores():
    creados = 0
    for data in PROVEEDORES:
        _, created = get_or_create(
            Proveedor,
            defaults={
                "nombre_razon_social": data["nombre_razon_social"],
                "telefono": data["telefono"],
                "correo": data["correo"],
                "activo": True,
            },
            nit=data["nit"],
        )
        creados += int(created)
    db.session.commit()
    return creados


def crear_joyas():
    creados = 0
    for data in JOYAS:
        categoria = Categoria.get_by_nombre(data["categoria"])
        material = Material.get_by_nombre(data["material"])
        _, created = get_or_create(
            Joya,
            defaults={
                "nombre": data["nombre"],
                "id_categoria": categoria.id_categoria,
                "id_material": material.id_material,
                "precio_compra": decimal_centavos(data["precio_compra"]),
                "precio_venta": decimal_centavos(data["precio_venta"]),
                "stock_actual": data["stock_actual"],
                "stock_minimo": data["stock_minimo"],
                "activo": True,
            },
            codigo=data["codigo"],
        )
        creados += int(created)
    db.session.commit()
    return creados


def firma_detalle_compra(detalle):
    return (detalle.joya.codigo, int(detalle.cantidad), decimal_centavos(detalle.precio_unit_compra))


def firma_detalle_venta(detalle):
    return (detalle.joya.codigo, int(detalle.cantidad), decimal_centavos(detalle.precio_unit_venta))


def firma_items_compra(items):
    return sorted((item["codigo_joya"], int(item["cantidad"]), decimal_centavos(item["precio_unit_compra"])) for item in items)


def firma_items_venta(items):
    return sorted((item["codigo_joya"], int(item["cantidad"]), decimal_centavos(item["precio_unit_venta"])) for item in items)


def existe_compra_semilla(proveedor, detalles):
    firma_esperada = firma_items_compra(detalles)
    compras = Compra.query.filter_by(id_proveedor=proveedor.id_proveedor, estado="COMPLETADA").all()
    return any(sorted(firma_detalle_compra(detalle) for detalle in compra.detalles) == firma_esperada for compra in compras)


def existe_venta_semilla(cliente, detalles):
    firma_esperada = firma_items_venta(detalles)
    ventas = Venta.query.filter_by(id_cliente=cliente.id_cliente, estado="COMPLETADA").all()
    return any(sorted(firma_detalle_venta(detalle) for detalle in venta.detalles) == firma_esperada for venta in ventas)


def existe_ajuste_semilla(joya, data):
    return AjusteInventario.query.filter_by(
        id_joya=joya.id_joya,
        cantidad_ajuste=int(data["cantidad_ajuste"]),
        motivo=data["motivo"],
        tipo_ajuste=data["tipo_ajuste"],
    ).first() is not None


def crear_compras(usuario):
    creadas = 0
    for data in COMPRAS:
        proveedor = Proveedor.get_by_nit(data["proveedor_nit"])
        if existe_compra_semilla(proveedor, data["detalles"]):
            continue

        compra = Compra(id_proveedor=proveedor.id_proveedor, id_usuario=usuario.id_usuario, total_compra=Decimal("0.00"), estado="COMPLETADA")
        db.session.add(compra)
        db.session.flush()

        total = Decimal("0.00")
        for item in data["detalles"]:
            joya = Joya.get_by_codigo(item["codigo_joya"])
            cantidad = int(item["cantidad"])
            precio = decimal_centavos(item["precio_unit_compra"])
            subtotal = precio * cantidad
            total += subtotal
            db.session.add(DetalleCompra(id_compra=compra.id_compra, id_joya=joya.id_joya, cantidad=cantidad, precio_unit_compra=precio, subtotal=subtotal))
            joya.stock_actual += cantidad
            joya.precio_compra = precio

        compra.total_compra = total
        creadas += 1
    db.session.commit()
    return creadas


def crear_ventas(usuario):
    creadas = 0
    for data in VENTAS:
        cliente = Cliente.get_by_ci_nit(data["cliente_ci_nit"])
        if existe_venta_semilla(cliente, data["detalles"]):
            continue

        venta = Venta(id_usuario=usuario.id_usuario, id_cliente=cliente.id_cliente, total_venta=Decimal("0.00"), estado="COMPLETADA")
        db.session.add(venta)
        db.session.flush()

        total = Decimal("0.00")
        for item in data["detalles"]:
            joya = Joya.get_by_codigo(item["codigo_joya"])
            cantidad = int(item["cantidad"])
            precio = decimal_centavos(item["precio_unit_venta"])
            subtotal = precio * cantidad
            if joya.stock_actual < cantidad:
                raise ValueError(f"Stock insuficiente para {joya.codigo} - {joya.nombre}")

            total += subtotal
            db.session.add(DetalleVenta(id_venta=venta.id_venta, id_joya=joya.id_joya, cantidad=cantidad, precio_unit_venta=precio, subtotal=subtotal))
            joya.stock_actual -= cantidad

        venta.total_venta = total
        creadas += 1
    db.session.commit()
    return creadas


def crear_ajustes_inventario(usuario):
    creados = 0
    for data in AJUSTES_INVENTARIO:
        joya = Joya.get_by_codigo(data["codigo_joya"])
        if existe_ajuste_semilla(joya, data):
            continue

        cantidad = int(data["cantidad_ajuste"])
        if data["tipo_ajuste"] == "SALIDA" and joya.stock_actual < cantidad:
            raise ValueError(f"Stock insuficiente para ajuste de salida en {joya.codigo} - {joya.nombre}")

        ajuste = AjusteInventario(
            id_joya=joya.id_joya,
            id_usuario=usuario.id_usuario,
            cantidad_ajuste=cantidad,
            motivo=data["motivo"],
            tipo_ajuste=data["tipo_ajuste"],
        )
        db.session.add(ajuste)

        if data["tipo_ajuste"] == "ENTRADA":
            joya.stock_actual += cantidad
        else:
            joya.stock_actual -= cantidad

        creados += 1
    db.session.commit()
    return creados


with app.app_context():
    usuario = buscar_usuario_existente()
    if usuario is None:
        print("No existe un usuario activo. Ejecuta primero crear_admin.py o crea un usuario desde el sistema.")
    else:
        resumen = {
            "catalogos": crear_catalogos(),
            "clientes": crear_clientes(),
            "proveedores": crear_proveedores(),
            "joyas": crear_joyas(),
            "compras": crear_compras(usuario),
            "ventas": crear_ventas(usuario),
            "ajustes_inventario": crear_ajustes_inventario(usuario),
        }

        print("Datos de prueba creados sin generar usuarios ni admins:")
        for tabla, cantidad in resumen.items():
            print(f"- {tabla}: {cantidad}")


# Actualización completa del proyecto (estado actual)

## Resumen del estado

- Aplicación web en Python construida con Flask.
- Estructura modular creada con carpetas para autenticación, formularios, módulos, rutas, plantillas, recursos estáticos y utilidades.
- Migraciones gestionadas con Alembic en `migrations/`.
- Dependencias declaradas en `requirements.txt`.
- Scripts de utilidad: `run.py` (arranque), `crear_admin.py` (crear administrador), `config.py` (configuración).

## Nuevas carpetas creadas

- `app/auth/` — gestión de login y autenticación.
- `app/forms/` — formularios con Flask-WTF.
- `app/modules/` — módulos por área funcional (`categorias`, `clientes`, `compras`, `inventario`, `joyas`, `materiales`, `proveedores`, `usuarios`, `ventas`).
- `app/routes/` — rutas principales de la aplicación.
- `app/static/` — recursos estáticos CSS, JS e imágenes.
- `app/templates/` — plantillas HTML y subcarpetas por sección.
- `app/utils/` — utilidades de la aplicación.

## Inventario de archivos y ubicación

Raíz del proyecto:

```
Actualizacion.md
README.md
Organizacion.md
config.py
crear_admin.py
run.py
requirements.txt
.env.example
.gitignore
```

Carpeta `app/` (principal):

```
app/__init__.py

app/auth/
	__init__.py
	login_manager.py

app/forms/
	auth_forms.py

app/modules/
	categorias/
	clientes/
	compras/
	inventario/
	joyas/
	materiales/
	proveedores/
	usuarios/
	ventas/

app/routes/
	auth.py
	dashboard.py
	usuarios.py
	ventas.py

app/static/
	css/
	img/
	js/

app/templates/
	base.html
	auth/
	components/
	dashboard/
	usuarios/
	ventas/

app/utils/
```

Carpeta `migrations/` (Alembic):

```
migrations/alembic.ini
migrations/env.py
migrations/README
migrations/script.py.mako
migrations/versions/
	8cec25f773cf_modelos_db_coregidos.py
	d26dcaa34ba2_migracion_de_auth_usuarios.py
	fb4501a982e1_modelos_de_la_db_definidos.py
```

Fin del inventario actualizado.



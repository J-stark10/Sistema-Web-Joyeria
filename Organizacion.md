# División del Proyecto

## Javier - Seguridad y Administración

Responsable de:

* Login
* Logout
* Usuarios
* Roles
* Dashboard
* Integración final del proyecto

---

## Caleb - Inventario

Responsable de:

* Categorías
* Materiales
* Joyas
* Control de stock

---

## Carlos - Ventas

Responsable de:

* Clientes
* Ventas
* Detalle de ventas
* Historial de ventas

---

## Alejandro - Compras y Reportes

Responsable de:

* Proveedores
* Compras
* Detalle de compras
* Reportes

---

# Reglas de Trabajo con Git

## No trabajar directamente en la rama `main`

La rama `main` debe mantenerse estable y funcionando correctamente.

Ningún integrante debe realizar cambios directamente sobre `main`.

---

## Cada integrante debe tener su propia rama

Ejemplo:

```bash
feature-auth
feature-inventario
feature-ventas
feature-compras
```

Cada integrante trabajará únicamente en su rama.

---

## Antes de empezar a programar

Actualizar siempre el proyecto:

```bash
git checkout main
git pull origin main
```

Luego actualizar la rama personal:

```bash
git checkout nombre-rama
git merge main
```

---

## Después de realizar cambios

Guardar y subir los cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push origin nombre-rama
```

---

## Importante

Antes de trabajar:

1. Actualizar `main`.
2. Actualizar tu rama.
3. Realizar cambios.
4. Hacer commit.
5. Hacer push.

Esto ayudará a evitar conflictos y mantener el proyecto organizado.

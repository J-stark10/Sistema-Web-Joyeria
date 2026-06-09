# Configuración Inicial del Proyecto

## 0. Si estas en linux
`python3` en ves de `python`

---

## 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd joyeria_illimani
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Copiar:

```bash
.env.example
```

como:

```bash
.env
```

y configurar las variables necesarias.

Ejemplo:

```env
SECRET_KEY=mi_clave_secreta
DATABASE_URL=sqlite:///db_joyeria.db
```

---

## 5. Ejecutar migraciones

La primera vez:

```bash
flask db upgrade
```

Si existen nuevos cambios en modelos:

```bash
flask db migrate -m "descripcion"
flask db upgrade
```

---

## 6. Crear usuario administrador

Ejecutar:

```bash
python crear_admin.py
```

Datos sugeridos:

Usuario:

```text
admin
```

Contraseña:

```text
admin123
```

Rol:

```text
ADMIN
```

---

## 7. Ejecutar la aplicación

```bash
python run.py
```

Abrir:

```text
http://127.0.0.1:5000
```

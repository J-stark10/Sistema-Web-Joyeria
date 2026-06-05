from app import create_app, db
from app.modules.usuarios.models import Usuario

from werkzeug.security import generate_password_hash

app = create_app('development')

with app.app_context():
    existe = Usuario.query.filter_by(nombre_usuario='admin').first()

    if existe:
        print("El usuario admin ya existe")
    else:
        usuario = Usuario(nombre_usuario='admin', contrasena_hash=generate_password_hash('admin123'),rol='ADMIN',activo=True)
        db.session.add(usuario)
        db.session.commit()

        print("Usuario admin creado")
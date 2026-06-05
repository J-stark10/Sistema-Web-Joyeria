from app import create_app, db, bcrypt
from app.models.usuario import Usuario

app = create_app('development')

with app.app_context():

    existe = Usuario.query.filter_by(
        nombre_usuario='admin'
    ).first()

    if existe:
        print("El usuario admin ya existe")
    else:
        usuario = Usuario(
            nombre_usuario='admin',
            contrasena_hash=bcrypt.generate_password_hash(
                'admin123'
            ).decode('utf-8'),
            rol='ADMIN',
            activo=True
        )

        db.session.add(usuario)
        db.session.commit()

        print("Usuario admin creado")
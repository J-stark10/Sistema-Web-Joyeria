from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app.extensions import db

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_hash = db.Column(db.Text, nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    ventas = db.relationship('Venta', backref='usuario', lazy=True)
    compras = db.relationship('Compra', back_populates='usuario', lazy=True)
    ajustes_inventario = db.relationship('AjusteInventario', backref='usuario', lazy=True)

    # ==========================
    # Flask-Login
    # ==========================

    def get_id(self):
        return str(self.id_usuario)

    # ==========================
    # Propiedades
    # ==========================

    @property
    def es_admin(self):
        return self.rol == 'ADMIN'

    @property
    def es_vendedor(self):
        return self.rol == 'VENDEDOR'

    # ==========================
    # Contraseña
    # ==========================

    def set_password(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena_hash, password)

    def update_password(self, password):
        self.set_password(password)
        db.session.commit()

    # ==========================
    # CRUD
    # ==========================

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_by_id(id_usuario):
        return Usuario.query.get(id_usuario)

    @staticmethod
    def get_by_username(nombre_usuario):
        return Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    def update(self, nombre_usuario=None, rol=None, activo=None):
        if nombre_usuario is not None:
            self.nombre_usuario = nombre_usuario

        if rol is not None:
            self.rol = rol

        if activo is not None:
            self.activo = activo

        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # ==========================
    # Representación
    # ==========================

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"